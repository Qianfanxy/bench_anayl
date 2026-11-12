"""Monetary cost per run, from token counts and a per-model price table.

Reads out/reliable_runs.csv (+ runs.csv / runs_old.csv for the cache breakdown) and prices.csv.
Writes out/reliable_runs_cost.csv and out/tables/R_4_*.csv.

Two cost definitions, both for the attempts that produced the judged file:
  cost_list   = input x input_price + output x output_price        (no cache discount; does not
                depend on whether the harness happened to enable prompt caching)
  cost_billed = uncached x input_price + cache_read x read_price + cache_write x write_price
                + output x output_price                             (only where the breakdown is known)

prices.csv columns: model, currency, input_per_M, output_per_M, cache_read_per_M, cache_write_per_M, source
Leave a price blank if unknown; the script then only reports the token composition.

Usage: .venv/bin/python cost.py out prices.csv
"""
import os
import sys

import numpy as np
import pandas as pd

OUT, PRICES = sys.argv[1], sys.argv[2]
TAB = os.path.join(OUT, "tables")
R = pd.read_csv(os.path.join(OUT, "reliable_runs.csv"), low_memory=False)
n = pd.read_csv(os.path.join(OUT, "runs.csv"), keep_default_na=False, na_values=[""], low_memory=False)
o = pd.read_csv(os.path.join(OUT, "runs_old.csv"), keep_default_na=False, na_values=[""])

R["out_tok"] = R.output_tokens_scored_file
R["in_tok"] = R.tokens_scored_file - R.out_tok
R["cache_read"], R["cache_write"], R["cache_source"] = np.nan, np.nan, "unknown"
# this batch: the metrics file has the breakdown, but only for the first attempt
nb = n.set_index("task_id")
for i, r in R[R.protocol == "v2"].iterrows():
    m = nb.loc[r.task_id]
    if pd.notna(m.mfile_cached_input_tokens) and abs(m.mfile_input_tokens - r.in_tok) <= 0.01 * r.in_tok:
        R.loc[i, ["cache_read", "cache_write", "cache_source"]] = [m.mfile_cached_input_tokens, m.mfile_cache_creation_tokens or 0, "metrics_file"]
ob = o.set_index("task_id")
for i, r in R[R.protocol == "v1"].iterrows():
    m = ob.loc[r.task_id]
    if m.cache_reporting in ("beside_input_tokens", "inside_input_tokens"):
        R.loc[i, ["cache_read", "cache_write", "cache_source"]] = [m.raw_cache_read, m.raw_cache_create, "per_request_trace"]

g = R.groupby(["model", "protocol"])
comp = pd.DataFrame({
    "runs": g.size(), "input_M_median": g.in_tok.median() / 1e6, "output_M_median": g.out_tok.median() / 1e6,
    "output_share_of_tokens": g.out_tok.sum() / (g.in_tok.sum() + g.out_tok.sum()),
    "runs_with_cache_breakdown": g.cache_read.count(),
    "cache_read_share_of_input": g.cache_read.sum() / g.apply(lambda d: d.loc[d.cache_read.notna(), "in_tok"].sum()),
    "cache_write_share_of_input": g.cache_write.sum() / g.apply(lambda d: d.loc[d.cache_read.notna(), "in_tok"].sum()),
}).reset_index()
comp.to_csv(os.path.join(TAB, "R_4_token_composition.csv"), index=False)
pd.set_option("display.width", 220)
print(comp.round(3).to_string(index=False))

P = pd.read_csv(PRICES).set_index("model")
for c in ["input_per_M", "output_per_M", "cache_read_per_M", "cache_write_per_M"]:
    P[c] = pd.to_numeric(P[c], errors="coerce")
missing = sorted(set(R.model) - set(P[P.input_per_M.notna() & P.output_per_M.notna()].index))
if missing:
    print("\nNo input/output price yet for:", missing, "\n-> fill prices.csv, then re-run. Token composition written; no costs computed.")
    sys.exit(0)
if P.loc[sorted(set(R.model)), "currency"].nunique() > 1:
    sys.exit("prices.csv mixes currencies; convert to one currency first.")
pi, po = R.model.map(P.input_per_M), R.model.map(P.output_per_M)
pr, pw = R.model.map(P.cache_read_per_M), R.model.map(P.cache_write_per_M).fillna(pi)
R["cost_list"] = (R.in_tok * pi + R.out_tok * po) / 1e6
R["cost_billed"] = ((R.in_tok - R.cache_read - R.cache_write) * pi + R.cache_read * pr + R.cache_write * pw + R.out_tok * po) / 1e6
R["output_share_of_cost"] = R.out_tok * po / 1e6 / R.cost_list
R.to_csv(os.path.join(OUT, "reliable_runs_cost.csv"), index=False)
s = R.groupby(["model", "protocol"]).agg(runs=("cost_list", "size"), cost_list_median=("cost_list", "median"),
                                         cost_list_mean=("cost_list", "mean"), cost_billed_median=("cost_billed", "median"),
                                         billed_n=("cost_billed", "count"), output_share_of_cost=("output_share_of_cost", "median")).reset_index()
s.to_csv(os.path.join(TAB, "R_4_cost_by_model.csv"), index=False)
print("\ncurrency:", P.currency.iloc[0])
print(s.round(3).to_string(index=False))
