# Efficiency analysis report (generated)

Records: 420 (model x problem x protocol), 42 problems, 10 models; 174 records come from the earlier package. Problems are a flat set; no categories are used. Score tolerance for 'same quality': 3 points.

## 0. Coverage and data audit

| model | protocol | records | problems | finished | scored | tokens_ok | tokens_partial | hit_time_limit | multi_attempt | checker_failed | needs_review |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DeepSeek V4 Flash | v2_no_screenshot_direct | 42 | 42 | 36 | 23 | 12 | 24 | 22 | 16 | 12 | 34 |
| Fable 5.1 | v1_screenshot_cc | 29 | 29 | 29 | 29 | 28 | 1 | 0 | 0 | 0 | 0 |
| Fable 5.1 | v2_no_screenshot_direct | 13 | 13 | 13 | 13 | 10 | 3 | 2 | 4 | 0 | 9 |
| GLM-5.3 Flash | v1_screenshot_cc | 29 | 29 | 29 | 29 | 29 | 0 | 1 | 0 | 0 | 0 |
| GLM-5.3 Flash | v2_no_screenshot_direct | 13 | 13 | 13 | 12 | 11 | 2 | 1 | 6 | 0 | 7 |
| GPT 6.1 Sol | v2_no_screenshot_direct | 42 | 42 | 42 | 40 | 38 | 4 | 0 | 7 | 12 | 15 |
| Gemini 3.5 Flash | v1_screenshot_cc | 29 | 29 | 29 | 29 | 29 | 0 | 0 | 0 | 0 | 0 |
| Gemini 3.5 Flash | v2_no_screenshot_direct | 13 | 13 | 13 | 13 | 12 | 1 | 0 | 10 | 0 | 12 |
| Kimi K3 | v1_screenshot_cc | 29 | 29 | 29 | 29 | 24 | 5 | 1 | 0 | 0 | 0 |
| Kimi K3 | v2_no_screenshot_direct | 13 | 13 | 13 | 13 | 10 | 3 | 3 | 6 | 0 | 6 |
| Opus 5.5（三方A） | v1_screenshot_cc | 29 | 29 | 29 | 29 | 26 | 3 | 0 | 0 | 0 | 0 |
| Opus 5.5（三方A） | v2_no_screenshot_direct | 13 | 13 | 13 | 12 | 11 | 2 | 0 | 3 | 0 | 2 |
| Qwen 3.8 Max | v2_no_screenshot_direct | 42 | 42 | 37 | 34 | 16 | 21 | 14 | 15 | 11 | 27 |
| Sonnet 5.5 | v2_no_screenshot_direct | 42 | 42 | 42 | 39 | 41 | 1 | 0 | 3 | 16 | 9 |
| gpt-6-astra | v1_screenshot_cc | 29 | 29 | 29 | 28 | 29 | 0 | 0 | 0 | 0 | 0 |
| gpt-6-astra | v2_no_screenshot_direct | 13 | 13 | 13 | 13 | 13 | 0 | 0 | 0 | 0 | 2 |

Inclusion sets (records with usable quality / tokens / time): **primary** 382/409/406; **all_measurable** 385/415/406; **strict_clean** 382/308/320

Restarts that ran on a different Figma file than the judged one: 30 runs; in those runs a median 39% of the reported tokens were spent on the non-judged file (max 97%). The primary token cost excludes that share.

Requested reasoning effort recorded in the trajectories of the judged attempts (`not_set` = no effort control was sent; `not_set|low` = attempts of the same run differ):

| model | low | low|not_set | no trajectory | not_set |
|---|---|---|---|---|
| DeepSeek V4 Flash | 26 | 5 | 0 | 5 |
| Fable 5.1 | 6 | 1 | 0 | 6 |
| GLM-5.3 Flash | 8 | 1 | 0 | 4 |
| GPT 6.1 Sol | 39 | 0 | 1 | 2 |
| Gemini 3.5 Flash | 7 | 3 | 0 | 3 |
| Kimi K3 | 8 | 2 | 0 | 3 |
| Opus 5.5（三方A） | 2 | 1 | 0 | 10 |
| Qwen 3.8 Max | 35 | 2 | 0 | 0 |
| Sonnet 5.5 | 26 | 2 | 0 | 14 |
| gpt-6-astra | 0 | 0 | 1 | 12 |

- `outcome_class`: delivered 349, delivered_checker_error 47, in_progress 6, not_run 5, checker_error_no_frames 4, timeout_partial 3, screen_count_mismatch 2, blank_output 2, failed_unknown 1, no_score 1
- `quality_validity`: ok 374, unusable:no_score 26, caveat:multiple_score_revisions 9, unusable:not_run 5, unusable:in_progress 4, caveat:scored_while_still_running 2
- `tokens_validity`: ok 339, caveat:partial_lower_bound 70, unusable:in_progress 6, unusable:missing 5
- `time_validity`: ok 320, caveat:censored_at_time_limit 36, caveat:includes_attempts_on_other_file 26, caveat:summed_over_attempts 24, unusable:in_progress 6, unusable:not_run 5, unusable:missing 3
- `trajectory_validity`: ok 410, unusable:no_trajectory 7, caveat:trajectory_incomplete 3

## 1. Per-model outcome and cost (primary set, unmatched — descriptive only)

| model | finished | delivered_or_checker_err | g0_fail | n_scored | score_mean | score_median | tokens_M_median | tokens_M_mean | tokens_M_p25 | tokens_M_p75 | max_over_min_tokens | all_attempt_tokens_M_median | minutes_median | tool_calls_median | tool_error_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GPT 6.1 Sol | 42 | 41 | 3 | 40 | 37.55 | 42.00 | 0.19 | 0.22 | 0.15 | 0.24 | 11.98 | 0.20 | 5.44 | 11.00 | 0.30 |
| gpt-6-astra | 42 | 41 | 0 | 41 | 43.76 | 45.00 | 0.26 | 0.27 | 0.19 | 0.31 | 7.94 | 0.26 | 6.42 | 20.00 | 0.17 |
| Sonnet 5.5 | 42 | 42 | 0 | 39 | 41.97 | 42.00 | 0.64 | 0.88 | 0.33 | 1.25 | 17.10 | 0.64 | 8.91 | 19.00 | 0.20 |
| Gemini 3.5 Flash | 42 | 42 | 10 | 42 | 26.07 | 30.50 | 1.23 | 1.61 | 0.72 | 2.00 | 45.00 | 1.33 | 11.20 | 29.00 | 0.20 |
| Opus 5.5（三方A） | 42 | 42 | 0 | 41 | 47.29 | 48.00 | 2.17 | 2.30 | 1.13 | 3.37 | 16.62 | 2.17 | 18.47 | 37.00 | 0.09 |
| GLM-5.3 Flash | 42 | 41 | 0 | 41 | 40.54 | 41.00 | 2.27 | 2.76 | 1.61 | 2.91 | 31.36 | 2.31 | 48.77 | 53.00 | 0.17 |
| Qwen 3.8 Max | 37 | 32 | 0 | 32 | 36.59 | 37.00 | 3.35 | 3.72 | 1.92 | 5.36 | 17.71 | 3.86 | 78.57 | 96.50 | 0.15 |
| Fable 5.1 | 42 | 42 | 1 | 42 | 39.67 | 40.50 | 3.96 | 5.39 | 2.51 | 7.64 | 36.12 | 4.06 | 34.80 | 71.50 | 0.12 |
| Kimi K3 | 42 | 42 | 0 | 42 | 39.05 | 40.00 | 4.08 | 4.93 | 1.71 | 6.58 | 29.52 | 4.16 | 40.72 | 67.50 | 0.19 |
| DeepSeek V4 Flash | 36 | 31 | 4 | 22 | 26.95 | 30.50 | 6.88 | 7.59 | 5.54 | 8.27 | 35.72 | 7.00 | 90.04 | 190.50 | 0.13 |

These rows mix different problem sets per model, so they are not a ranking. Use sections 2-3.

## 2. Problem-adjusted model effects (score and cost)

Additive model `y ~ model + problem`, fitted on all usable records, so a model that only ran 13 problems is compared on those problems' own difficulty. Cost effects are multiplicative (x geometric mean of models); 95% intervals resample problems.

| model | n_score | score_effect | score_lo | score_hi | tokens_x | tokens_x_lo | tokens_x_hi | time_x | time_x_lo | time_x_hi | tool_calls_x |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-6-astra | 41.00 | 5.12 | 3.55 | 6.56 | 0.13 | 0.11 | 0.15 | 0.25 | 0.22 | 0.28 | 0.43 |
| GPT 6.1 Sol | 40.00 | 1.11 | -4.02 | 5.38 | 0.20 | 0.17 | 0.23 | 0.35 | 0.28 | 0.42 | 0.37 |
| Gemini 3.5 Flash | 42.00 | -12.67 | -17.64 | -8.27 | 0.67 | 0.56 | 0.80 | 0.42 | 0.35 | 0.51 | 0.59 |
| Sonnet 5.5 | 39.00 | 5.03 | 2.51 | 7.45 | 0.72 | 0.58 | 0.88 | 0.57 | 0.48 | 0.72 | 0.60 |
| Opus 5.5（三方A） | 41.00 | 8.70 | 7.17 | 10.21 | 1.01 | 0.87 | 1.16 | 0.73 | 0.64 | 0.83 | 0.66 |
| GLM-5.3 Flash | 41.00 | 1.94 | 0.26 | 3.76 | 1.25 | 1.02 | 1.54 | 1.87 | 1.64 | 2.09 | 1.13 |
| Kimi K3 | 42.00 | 0.30 | -1.70 | 2.41 | 1.78 | 1.42 | 2.28 | 1.57 | 1.33 | 1.85 | 1.27 |
| Fable 5.1 | 42.00 | 0.92 | -1.80 | 3.19 | 2.24 | 1.84 | 2.72 | 1.25 | 1.08 | 1.43 | 1.43 |
| Qwen 3.8 Max | 32.00 | -0.23 | -2.70 | 2.39 | 2.97 | 2.36 | 3.77 | 3.62 | 2.57 | 4.68 | 2.68 |
| DeepSeek V4 Flash | 22.00 | -10.22 | -15.83 | -5.53 | 5.40 | 4.03 | 7.18 | 5.01 | 3.99 | 6.28 | 4.95 |

**Protocol shift** (earlier package: screenshot self-check required, Claude Code harness; this batch: screenshots forbidden, direct runner). Estimated as one common shift, identified because the four 42-problem models fix each problem's level under the new protocol and the six other models were run under both protocols on different problems. It assumes the shift is the same for every model and that models do not interact with problems:

- score: +2.9 points under the earlier protocol (95% -1.6 to +7.4)
- tokens: x2.77 (95% 2.18 to 3.48); time: x2.13 (95% 1.68 to 2.77)

## 3. Problem-matched pairwise comparison (primary set)

45 model pairs with >=5 common problems (full table: tables/3_pairwise_matched.csv). Largest cost gaps without a quality gain:

| model_a | model_b | n_common | median_score_diff_a_minus_b | a_higher_score | b_higher_score | median_token_ratio_a_over_b | a_cheaper_on | a_cheaper_and_not_worse | a_costlier_and_not_better |
|---|---|---|---|---|---|---|---|---|---|
| DeepSeek V4 Flash | GPT 6.1 Sol | 20 | -9.00 | 3 | 16 | 34.98 | 0 | 0 | 17 |
| DeepSeek V4 Flash | gpt-6-astra | 7 | -11.00 | 0 | 7 | 25.94 | 0 | 0 | 7 |
| Fable 5.1 | gpt-6-astra | 41 | -3.00 | 1 | 19 | 17.29 | 0 | 0 | 40 |
| GPT 6.1 Sol | Qwen 3.8 Max | 30 | 4.00 | 16 | 6 | 0.06 | 30 | 24 | 0 |
| Kimi K3 | gpt-6-astra | 41 | -4.00 | 0 | 22 | 15.41 | 0 | 0 | 41 |
| GLM-5.3 Flash | GPT 6.1 Sol | 12 | -2.50 | 4 | 5 | 13.46 | 0 | 0 | 8 |
| Qwen 3.8 Max | gpt-6-astra | 12 | -9.00 | 0 | 9 | 13.29 | 0 | 0 | 12 |
| Fable 5.1 | GPT 6.1 Sol | 12 | 1.50 | 4 | 2 | 10.92 | 1 | 1 | 7 |
| DeepSeek V4 Flash | Sonnet 5.5 | 22 | -12.00 | 2 | 18 | 9.75 | 1 | 0 | 19 |
| GLM-5.3 Flash | gpt-6-astra | 40 | -3.00 | 3 | 17 | 8.63 | 0 | 0 | 37 |
| Opus 5.5（三方A） | gpt-6-astra | 40 | 3.00 | 17 | 1 | 8.34 | 0 | 0 | 23 |
| DeepSeek V4 Flash | Gemini 3.5 Flash | 7 | 5.00 | 4 | 2 | 7.46 | 0 | 0 | 3 |

## 4. Per-problem cost-quality Pareto frontier

Share of problems on which each model is not dominated. `tol0` is strict dominance; `tol3` only counts domination by a model that is >=20% cheaper at no worse than -3 points, or cheaper and better by more than 3. A frontier is an observed set from single runs, not a guarantee.

| model | time_tol0 | time_tol3 | tokens_tol0 | tokens_tol3 | problems |
|---|---|---|---|---|---|
| gpt-6-astra | 1.00 | 1.00 | 0.98 | 0.98 | 41 |
| GPT 6.1 Sol | 0.66 | 0.63 | 0.91 | 0.97 | 35 |
| Opus 5.5（三方A） | 0.88 | 0.41 | 0.88 | 0.41 | 41 |
| Sonnet 5.5 | 0.51 | 0.35 | 0.35 | 0.22 | 37 |
| GLM-5.3 Flash | 0.00 | 0.00 | 0.10 | 0.05 | 41 |
| Gemini 3.5 Flash | 0.31 | 0.31 | 0.07 | 0.05 | 42 |
| Qwen 3.8 Max | 0.03 | 0.00 | 0.03 | 0.00 | 29 |
| Fable 5.1 | 0.02 | 0.00 | 0.02 | 0.00 | 42 |
| DeepSeek V4 Flash | 0.00 | 0.00 | 0.00 | 0.00 | 22 |
| Kimi K3 | 0.00 | 0.00 | 0.00 | 0.00 | 42 |

## 5. Cost vs quality relationship

Across models within the same problem (Spearman between cost and score), summarised over problems. Problems with only 4 models give very coarse correlations and are shown separately.

| cost | many | problems | median | share_negative | p25 | p75 |
|---|---|---|---|---|---|---|
| time | 4-7 models | 37 | -0.09 | 0.54 | -0.32 | 0.15 |
| time | >=8 models | 12 | -0.27 | 0.83 | -0.48 | -0.09 |
| tokens | 4-7 models | 37 | -0.09 | 0.65 | -0.37 | 0.20 |
| tokens | >=8 models | 12 | -0.15 | 0.75 | -0.32 | -0.02 |
| tool_calls | 4-7 models | 37 | -0.17 | 0.65 | -0.58 | 0.14 |
| tool_calls | >=8 models | 12 | -0.44 | 0.92 | -0.50 | -0.08 |

Within-model, within-problem association `score ~ model + problem + gamma*log(cost)`. gamma is an association, not the effect of spending more: runs that go badly also retry more.

| cost | scores | n | gamma_points_per_log_cost | ci_lo | ci_hi | points_per_doubling |
|---|---|---|---|---|---|---|
| tokens | all scored | 382 | 0.10 | -1.11 | 1.40 | 0.07 |
| tokens | G0-pass only | 364 | 0.64 | -0.08 | 1.30 | 0.44 |
| time | all scored | 380 | -0.96 | -2.67 | 0.95 | -0.67 |
| time | G0-pass only | 362 | 0.48 | -0.40 | 1.35 | 0.33 |
| tool_calls | all scored | 380 | -1.15 | -3.29 | 0.93 | -0.80 |
| tool_calls | G0-pass only | 362 | 0.35 | -0.62 | 1.20 | 0.25 |

## 6. Execution behaviour (where resources go)

Tool-call mix and error behaviour per model (labels are descriptive; no category is 'waste' by itself):

`v1` = earlier package (screenshots required), `v2` = this batch (screenshots forbidden). `verify` = get_screenshot calls. Error shares are of failed calls; `intentional_throw` = the model threw an Error on purpose to print data.

| model | proto | runs | turns_med | calls_med | inspect_share | construct_share | modify_share | prototype_share | verify_share | error_rate | model_err_share | infra_err_share | unknown_err_share | intentional_throw_share | repeat_same_error_per_run | duplicate_calls_per_run | delete_calls_per_run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DeepSeek V4 Flash | v2 | 36 | 155.00 | 170.50 | 0.44 | 0.29 | 0.10 | 0.04 | 0.12 | 0.18 | 0.57 | 0.19 | 0.12 | 0.12 | 4.69 | 41.11 | 20.86 |
| Fable 5.1 | v1 | 29 | 40.00 | 81.00 | 0.14 | 0.25 | 0.15 | 0.05 | 0.40 | 0.13 | 0.89 | 0.05 | 0.01 | 0.03 | 0.41 | 10.66 | 11.62 |
| Fable 5.1 | v2 | 13 | 42.00 | 45.00 | 0.28 | 0.33 | 0.23 | 0.13 | 0.01 | 0.10 | 0.71 | 0.05 | 0.15 | 0.10 | 0.00 | 3.77 | 4.15 |
| GLM-5.3 Flash | v1 | 29 | 54.00 | 54.00 | 0.26 | 0.26 | 0.10 | 0.07 | 0.29 | 0.17 | 0.66 | 0.32 | 0.00 | 0.00 | 0.34 | 7.55 | 6.21 |
| GLM-5.3 Flash | v2 | 13 | 42.00 | 45.00 | 0.29 | 0.35 | 0.12 | 0.21 | 0.00 | 0.17 | 0.94 | 0.00 | 0.00 | 0.00 | 0.62 | 1.23 | 5.77 |
| GPT 6.1 Sol | v2 | 41 | 12.00 | 11.00 | 0.35 | 0.37 | 0.07 | 0.09 | 0.00 | 0.29 | 0.86 | 0.01 | 0.00 | 0.10 | 0.05 | 0.10 | 1.51 |
| Gemini 3.5 Flash | v1 | 29 | 32.00 | 30.00 | 0.44 | 0.30 | 0.06 | 0.07 | 0.09 | 0.23 | 0.52 | 0.19 | 0.05 | 0.23 | 0.31 | 0.97 | 4.76 |
| Gemini 3.5 Flash | v2 | 13 | 28.00 | 27.00 | 0.50 | 0.36 | 0.04 | 0.04 | 0.00 | 0.13 | 0.60 | 0.00 | 0.00 | 0.40 | 0.62 | 1.23 | 5.23 |
| Kimi K3 | v1 | 29 | 70.00 | 81.00 | 0.24 | 0.25 | 0.14 | 0.06 | 0.28 | 0.20 | 0.58 | 0.37 | 0.00 | 0.01 | 1.21 | 7.83 | 8.79 |
| Kimi K3 | v2 | 13 | 21.00 | 23.00 | 0.45 | 0.34 | 0.11 | 0.07 | 0.00 | 0.15 | 0.95 | 0.03 | 0.01 | 0.01 | 0.38 | 0.54 | 6.85 |
| Opus 5.5（三方A） | v1 | 29 | 37.00 | 43.00 | 0.11 | 0.26 | 0.18 | 0.05 | 0.37 | 0.09 | 0.51 | 0.40 | 0.00 | 0.09 | 0.21 | 1.86 | 2.76 |
| Opus 5.5（三方A） | v2 | 13 | 17.00 | 17.00 | 0.18 | 0.44 | 0.25 | 0.07 | 0.00 | 0.08 | 0.95 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.15 |
| Qwen 3.8 Max | v2 | 37 | 96.00 | 100.00 | 0.49 | 0.27 | 0.19 | 0.04 | 0.00 | 0.15 | 0.97 | 0.01 | 0.00 | 0.01 | 0.65 | 1.43 | 8.68 |
| Sonnet 5.5 | v2 | 42 | 18.00 | 19.00 | 0.24 | 0.45 | 0.18 | 0.07 | 0.00 | 0.21 | 0.90 | 0.00 | 0.00 | 0.07 | 0.02 | 0.21 | 3.17 |
| gpt-6-astra | v1 | 29 | 19.00 | 26.00 | 0.25 | 0.20 | 0.13 | 0.05 | 0.34 | 0.15 | 0.70 | 0.05 | 0.00 | 0.15 | 0.03 | 1.14 | 1.48 |
| gpt-6-astra | v2 | 12 | 13.00 | 12.00 | 0.39 | 0.34 | 0.08 | 0.10 | 0.00 | 0.25 | 0.68 | 0.00 | 0.00 | 0.24 | 0.00 | 0.25 | 1.92 |

Infrastructure-caused failed calls (quota circuit breaker, tool timeouts, transport). These are not the model's doing, and the retries they trigger inflate tokens and time:

| model | proto | runs | runs_with_infra_errors | infra_errors | calls | infra_errors_per_100_calls |
|---|---|---|---|---|---|---|
| DeepSeek V4 Flash | v2 | 36 | 11 | 215.00 | 6518.00 | 3.30 |
| Fable 5.1 | v1 | 29 | 11 | 15.00 | 2320.00 | 0.65 |
| Fable 5.1 | v2 | 13 | 1 | 4.00 | 819.00 | 0.49 |
| GLM-5.3 Flash | v1 | 29 | 15 | 93.00 | 1716.00 | 5.42 |
| GLM-5.3 Flash | v2 | 13 | 0 | 0.00 | 682.00 | 0.00 |
| GPT 6.1 Sol | v2 | 41 | 1 | 1.00 | 497.00 | 0.20 |
| Gemini 3.5 Flash | v1 | 29 | 4 | 41.00 | 934.00 | 4.39 |
| Gemini 3.5 Flash | v2 | 13 | 0 | 0.00 | 404.00 | 0.00 |
| Kimi K3 | v1 | 29 | 17 | 176.00 | 2376.00 | 7.41 |
| Kimi K3 | v2 | 13 | 1 | 3.00 | 657.00 | 0.46 |
| Opus 5.5（三方A） | v1 | 29 | 10 | 43.00 | 1220.00 | 3.52 |
| Opus 5.5（三方A） | v2 | 13 | 0 | 0.00 | 231.00 | 0.00 |
| Qwen 3.8 Max | v2 | 37 | 4 | 8.00 | 3802.00 | 0.21 |
| Sonnet 5.5 | v2 | 42 | 0 | 0.00 | 798.00 | 0.00 |
| gpt-6-astra | v1 | 29 | 5 | 6.00 | 769.00 | 0.78 |
| gpt-6-astra | v2 | 12 | 0 | 0.00 | 165.00 | 0.00 |

Context occupancy: every message is re-sent on each later model request, so its characters are weighted by the number of later requests that contain it. This is where *input* tokens come from (shares sum to 1). `fixed_prompt` is the system prompt + tool schemas, paid once per turn.

| model | proto | setup | inspect | construct | modify | prototype | verify | other_tool | assistant_text | fixed_prompt | harness_reminders |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DeepSeek V4 Flash | v2 | 0.00 | 0.58 | 0.28 | 0.03 | 0.01 | 0.02 | 0.00 | 0.03 | 0.05 | 0.00 |
| Fable 5.1 | v1 | 0.00 | 0.22 | 0.46 | 0.08 | 0.02 | 0.06 | 0.00 | 0.02 | 0.13 | 0.01 |
| Fable 5.1 | v2 | 0.00 | 0.41 | 0.26 | 0.22 | 0.02 | 0.00 | 0.00 | 0.01 | 0.07 | 0.00 |
| GLM-5.3 Flash | v1 | 0.00 | 0.30 | 0.27 | 0.05 | 0.05 | 0.04 | 0.00 | 0.02 | 0.26 | 0.00 |
| GLM-5.3 Flash | v2 | 0.00 | 0.37 | 0.44 | 0.03 | 0.06 | 0.00 | 0.00 | 0.01 | 0.09 | 0.00 |
| GPT 6.1 Sol | v2 | 0.01 | 0.31 | 0.31 | 0.10 | 0.01 | 0.00 | 0.00 | 0.00 | 0.26 | 0.00 |
| Gemini 3.5 Flash | v1 | 0.00 | 0.27 | 0.42 | 0.03 | 0.02 | 0.00 | 0.00 | 0.00 | 0.26 | 0.00 |
| Gemini 3.5 Flash | v2 | 0.01 | 0.36 | 0.47 | 0.02 | 0.01 | 0.00 | 0.00 | 0.00 | 0.13 | 0.00 |
| Kimi K3 | v1 | 0.00 | 0.26 | 0.38 | 0.05 | 0.03 | 0.04 | 0.00 | 0.00 | 0.22 | 0.00 |
| Kimi K3 | v2 | 0.00 | 0.44 | 0.41 | 0.05 | 0.02 | 0.00 | 0.00 | 0.00 | 0.08 | 0.00 |
| Opus 5.5（三方A） | v1 | 0.01 | 0.05 | 0.39 | 0.30 | 0.01 | 0.05 | 0.00 | 0.00 | 0.18 | 0.02 |
| Opus 5.5（三方A） | v2 | 0.01 | 0.06 | 0.40 | 0.34 | 0.01 | 0.00 | 0.00 | 0.00 | 0.18 | 0.00 |
| Qwen 3.8 Max | v2 | 0.00 | 0.35 | 0.47 | 0.10 | 0.01 | 0.00 | 0.00 | 0.01 | 0.07 | 0.00 |
| Sonnet 5.5 | v2 | 0.01 | 0.19 | 0.42 | 0.18 | 0.01 | 0.00 | 0.00 | 0.00 | 0.20 | 0.00 |
| gpt-6-astra | v1 | 0.01 | 0.27 | 0.23 | 0.29 | 0.02 | 0.03 | 0.00 | 0.00 | 0.16 | 0.00 |
| gpt-6-astra | v2 | 0.01 | 0.38 | 0.32 | 0.08 | 0.01 | 0.00 | 0.00 | 0.00 | 0.21 | 0.00 |

Validation of that attribution: Spearman between trajectory-implied context size and reported input tokens = **0.92** over 407 runs. Per-model characters per reported input token (a stable ratio means the token counts and the trajectory agree; outliers are flagged in the review queue):

| model | proto | chars_per_input_token_median | min | max | runs |
|---|---|---|---|---|---|
| DeepSeek V4 Flash | v2 | 6.40 | 1.59 | 23.49 | 36 |
| Fable 5.1 | v1 | 1.66 | 1.29 | 1.91 | 29 |
| Fable 5.1 | v2 | 3.24 | 1.38 | 4.86 | 13 |
| GLM-5.3 Flash | v1 | 3.82 | 2.79 | 4.82 | 29 |
| GLM-5.3 Flash | v2 | 2.07 | 0.61 | 2.68 | 13 |
| GPT 6.1 Sol | v2 | 3.86 | 2.06 | 4.70 | 41 |
| Gemini 3.5 Flash | v1 | 3.08 | 2.52 | 3.35 | 29 |
| Gemini 3.5 Flash | v2 | 2.01 | 0.42 | 7.01 | 13 |
| Kimi K3 | v1 | 2.69 | 0.53 | 2.97 | 29 |
| Kimi K3 | v2 | 2.51 | 0.08 | 4.69 | 13 |
| Opus 5.5（三方A） | v1 | 1.54 | 1.36 | 1.83 | 29 |
| Opus 5.5（三方A） | v2 | 1.41 | 1.22 | 1.82 | 13 |
| Qwen 3.8 Max | v2 | 5.58 | 0.97 | 9.58 | 37 |
| Sonnet 5.5 | v2 | 1.93 | 1.32 | 2.47 | 42 |
| gpt-6-astra | v1 | 6.65 | 4.02 | 12.52 | 29 |
| gpt-6-astra | v2 | 4.00 | 3.52 | 5.11 | 12 |

What moves with token use after removing model and problem averages:

| feature | partial_spearman_with_log_tokens | n |
|---|---|---|
| turns | 0.90 | 407 |
| construct calls | 0.75 | 407 |
| modify calls | 0.60 | 407 |
| tool errors | 0.57 | 407 |
| inspect calls | 0.55 | 407 |
| calls that delete | 0.47 | 407 |
| duplicate calls | 0.42 | 407 |
| screenshot calls | 0.30 | 407 |
| same error repeated | 0.19 | 407 |
| largest tool result | 0.06 | 407 |

## 7. Robustness of the conclusions

Model effects re-estimated under each inclusion set (for `score` the last column is the largest change in points; for costs it is the largest change in log2 units, i.e. 1.0 = a factor of two):

| cost | set | models | rank_corr_with_primary | max_abs_log2_change |
|---|---|---|---|---|
| tokens | primary | 10 | 1.00 | 0.00 |
| tokens | all_measurable | 10 | 1.00 | 0.08 |
| tokens | strict_clean | 10 | 0.99 | 0.51 |
| time | primary | 10 | 1.00 | 0.00 |
| time | all_measurable | 10 | 1.00 | 0.00 |
| time | strict_clean | 10 | 0.99 | 0.40 |
| score | primary | 10 | 1.00 | 0.00 |
| score | all_measurable | 10 | 1.00 | 0.12 |
| score | strict_clean | 10 | 1.00 | 0.00 |

Cost-quality slope (gamma) under each set and cost measure:

| set | cost | n | points_per_doubling | lo_per_doubling | hi_per_doubling |
|---|---|---|---|---|---|
| primary | tokens | 382 | 0.07 | -0.77 | 0.97 |
| primary | time | 380 | -0.67 | -1.85 | 0.66 |
| primary | tool_calls | 380 | -0.80 | -2.28 | 0.64 |
| all_measurable | tokens | 385 | 0.09 | -0.81 | 0.92 |
| all_measurable | time | 381 | -0.65 | -2.16 | 0.56 |
| all_measurable | tool_calls | 383 | -0.71 | -2.21 | 0.76 |
| strict_clean | tokens | 292 | 0.75 | -0.70 | 2.11 |
| strict_clean | time | 304 | 0.24 | -1.78 | 2.08 |
| strict_clean | tool_calls | 290 | 0.18 | -2.23 | 2.49 |

Tokens vs wall-clock time across runs: Spearman 0.86 (n=406); they are related but not interchangeable, so both are reported.

## 8. Open items the data cannot settle

- Single run per model x problem: run-to-run variance is unobserved, so small differences are not evidence.
- Judge noise is not estimated here; the 3-point tolerance is a placeholder until repeat judgings or human ratings exist.
- Progress curves (cost vs verified progress) need intermediate file states or the trace database; trajectories alone only support call-level proxies.
