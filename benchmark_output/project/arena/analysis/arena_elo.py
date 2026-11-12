"""Reproduce the Arena preference analysis from the latest SQLite snapshot."""
import hashlib
import json
import math
import random
import sqlite3
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean

DB = Path(__file__).resolve().parents[3] / 'arena.sqlite3'
EXCLUDED = '6case-case-004'
EXPERTS = ('participant-88da474b00f1bfba176ba284',
           'participant-c387d1e86a8b70b0f54324a7')
BOOT = 4000


def fit(wins, models):
    # Finite unpenalized MLE requires a strongly connected directed win graph.
    for start in models:
        reachable = {start}
        for _ in models:
            reachable |= {b for (a, b), n in wins.items() if n and a in reachable}
        if len(reachable) != len(models):
            return None
    totals = {a: sum(wins[a, b] for b in models) for a in models}
    opponents = {a: [(b, wins[a, b] + wins[b, a]) for b in models if b != a]
                 for a in models}
    strength = dict.fromkeys(models, 1.0)
    for _ in range(3000):
        updated = {a: totals[a] / sum(n / (strength[a] + strength[b])
                                      for b, n in opponents[a]) for a in models}
        scale = mean(updated.values())
        updated = {a: v / scale for a, v in updated.items()}
        if max(abs(math.log(updated[a] / strength[a])) for a in models) < 1e-9:
            logs = {a: math.log10(updated[a]) for a in models}
            center = mean(logs.values())
            return {a: 1200 + 400 * (logs[a] - center) for a in models}
        strength = updated
    raise RuntimeError('Bradley–Terry fitting did not converge')


def interval(values):
    ordered = sorted(values)
    return [ordered[round(q * (len(ordered) - 1))] for q in (.025, .975)]


def summarize(rows, models):
    tasks = defaultdict(Counter)
    wins = Counter()
    for case, reviewer, winner, loser in rows:
        tasks[case][winner, loser] += 1
        wins[winner, loser] += 1
    ratings = fit(wins, models)
    if ratings is None:
        raise ValueError('No finite overall fit')
    rng = random.Random(20261109)
    draws = []
    for _ in range(BOOT):
        sample = Counter()
        for task in rng.choices(sorted(tasks), k=len(tasks)):
            sample.update(tasks[task])
        estimate = fit(sample, models)
        if estimate is not None:
            draws.append(estimate)
    order = sorted(models, key=ratings.get, reverse=True)
    return dict(tasks=len(tasks), votes=len(rows), reviewers=dict(Counter(r[1] for r in rows)),
                valid_bootstrap=len(draws),
                leaderboard=[dict(model=a, elo=ratings[a],
                                  ci95=interval([d[a] for d in draws]),
                                  wins=sum(wins[a, b] for b in models),
                                  losses=sum(wins[b, a] for b in models),
                                  top_share=mean(d[a] == max(d.values()) for d in draws))
                             for a in order],
                adjacent_gaps=[dict(higher=a, lower=b, gap=ratings[a]-ratings[b],
                                    ci95=interval([d[a]-d[b] for d in draws]))
                               for a, b in zip(order, order[1:])])


def tau(a, b, models):
    signs = [(a[x]-a[y], b[x]-b[y]) for x, y in combinations(models, 2)]
    denominator = math.sqrt(sum(x != 0 for x, y in signs) * sum(y != 0 for x, y in signs))
    return sum((x*y > 0) - (x*y < 0) for x, y in signs) / denominator if denominator else None


def main():
    db = sqlite3.connect(DB.as_uri() + '?mode=ro&immutable=1', uri=True)
    assert db.execute('pragma integrity_check').fetchone() == ('ok',)
    candidates = {(case, model): json.loads(body) for case, model, body in
                  db.execute('select case_id, model_id, body from candidates')}
    labels = {model: item['model_name'] for (_, model), item in candidates.items()}
    models = sorted(labels)
    scores = {(case, model): float(item['cc_score']) for (case, model), item in candidates.items()}
    sessions = {}
    for sid, case, reviewer, state, members in db.execute(
            'select id,case_id,reviewer_id,state,models from incremental_sort_sessions'):
        for member in json.loads(members):
            assert member['candidate_id'] == candidates[case, member['model_id']]['id']
        sessions[sid] = case, reviewer, json.loads(state)
    votes = {}
    audit = Counter()
    for sid, a, b, winner, outcome, active in db.execute(
            'select session_id,a,b,winner,outcome,active from incremental_sort_votes '
            'order by created_at,ballot_id'):
        case, reviewer, _ = sessions[sid]
        if not active or outcome != 'win' or case == EXCLUDED:
            audit['filtered'] += 1
            continue
        assert a != b and winner in (a, b)
        key = sid, tuple(sorted((a, b)))
        if key in votes:
            audit['duplicates'] += 1
            audit['conflicting_duplicates'] += votes[key][2] != winner
        votes[key] = case, reviewer, winner, b if winner == a else a
    rows = list(votes.values())
    ranks = defaultdict(dict)
    for case, reviewer, state in sessions.values():
        if case != EXCLUDED and state['status'] == 'complete':
            ranking = state['ranking']
            assert len(ranking) == len(models) and set(ranking) == set(models)
            assert case not in ranks[reviewer]
            ranks[reviewer][case] = {model: i+1 for i, model in enumerate(ranking)}
    result = dict(sha256=hashlib.sha256(DB.read_bytes()).hexdigest(), labels=labels,
                  excluded_case=EXCLUDED, bootstrap_replicates=BOOT, audit=dict(audit))
    result['expert_leaderboard'] = summarize([r for r in rows if r[1] in EXPERTS], models)
    result['all_reviewers_sensitivity'] = summarize(rows, models)
    result['expert_completed_sensitivity'] = summarize(
        [row for (sid, _), row in votes.items()
         if row[1] in EXPERTS and sessions[sid][2]['status'] == 'complete'], models)
    result['experts'] = {}
    for i, reviewer in enumerate(EXPERTS, 1):
        rankings = ranks[reviewer]
        taus = [tau(ranking, {m: -scores[case, m] for m in models}, models)
                for case, ranking in rankings.items()]
        margins = [scores[c, w] - scores[c, l] for c, r, w, l in rows if r == reviewer]
        result['experts'][f'R{i}'] = dict(
            completed_tasks=len(rankings),
            mean_ranks={m: mean(r[m] for r in rankings.values()) for m in models},
            rubric_mean_tau=mean(t for t in taus if t is not None),
            rubric_tau_tasks=sum(t is not None for t in taus),
            rubric_vote_agreement=sum(d > 0 for d in margins),
            rubric_vote_denominator=sum(d != 0 for d in margins),
            rubric_ties=sum(d == 0 for d in margins))
    a, b = (ranks[r] for r in EXPERTS)
    common = sorted(a.keys() & b.keys())
    result['expert_agreement'] = dict(
        tasks=len(common), mean_tau=mean(tau(a[c], b[c], models) for c in common),
        same_first=sum(next(iter(a[c])) == next(iter(b[c])) for c in common))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
