# Construction-strategy hypotheses (fixed before looking at any result)

Written 2026-11-12, before design_ops.py was run on scores. Each hypothesis names one strategy
measure, the rubric item(s) it should move, and the expected sign. Only these 11 pairs are tested;
p-values are Holm-corrected across the 11. Everything else is reported as descriptive.

Strategy measures are computed per run from the code of its write calls (build / revise / wire):

| measure | definition |
|---|---|
| reuse_ratio | instance creations / (instance creations + primitive shapes + new frames) |
| own_components | the run creates its own components or variant sets (createComponent / combineAsVariants) |
| clone_ratio | node duplications (.clone) / all creation operations |
| autolayout_ratio | auto-layout assignments (layoutMode = HORIZONTAL/VERTICAL/GRID) / new frames |
| naming_ratio | explicit layer-name assignments (.name =) / all creation operations |
| primitive_share | primitive shapes (rectangle, ellipse, line, vector, polygon, star, SVG import) / all creation operations |

| id | measure | rubric item | expected | why |
|---|---|---|---|---|
| H1a | reuse_ratio | E1 same-function controls consistent | + | instances of one component cannot drift apart |
| H1b | reuse_ratio | E2 pages share navigation and visual language | + | shared bars and shells come from the same component |
| H1c | reuse_ratio | B4 icons clear | + | the file's icon components replace hand-drawn placeholders |
| H2 | own_components | E1 same-function controls consistent | + | a self-built component system enforces consistency |
| H3 | clone_ratio | E2 pages share navigation and visual language | + | duplicating a finished screen carries its frame across pages |
| H4a | autolayout_ratio | D1 alignment inside a control | + | auto-layout fixes padding and alignment |
| H4b | autolayout_ratio | D2 spacing inside a component | + | auto-layout fixes item spacing |
| H4c | autolayout_ratio | G2 layer hierarchy matches regions | + | auto-layout forces content into its container |
| H5 | naming_ratio | G1 frames and layers named by function | + | names are only meaningful if set |
| H6a | primitive_share | B4 icons clear | − | icons drawn from shapes tend to be crude |
| H6b | primitive_share | F5 overall polish | − | hand-drawn elements look less finished |

Test: partial Spearman correlation between the measure and the item score after removing model,
problem and protocol means (same model, same problem), with 95% intervals from resampling problems.
Runs that failed the G0 gate are excluded (their item scores are not a rating of the design).

---

# Product-layer hypotheses (fixed before looking at any result)

Written 2026-11-12, after confirming that the judge scores G1 and G2 **only** from the layer-structure
summary in `benchmark-layers.json` (rubric fixed-v4, section 4). Snapshot fields therefore cannot be
tested against G1/G2 without circularity; those pairs are reported only as a consistency check.
The tests below use rubric items the judge scores from the screenshots.

Measures per run, from the final file's layer snapshot (one record per screen, then the run median):

| measure | definition |
|---|---|
| instance_node_share | instances / nodes |
| nodes_per_screen | nodes |
| images_per_screen | images |

| id | measure | rubric item | expected | why |
|---|---|---|---|---|
| P1a | instance_node_share | E1 same-function controls consistent | + | reused instances cannot drift apart |
| P1b | instance_node_share | E2 pages share navigation and visual language | + | shared bars come from one component |
| P1c | instance_node_share | B4 icons clear | + | the file's icons are components; drawn icons are not |
| P2 | images_per_screen | F5 overall polish | + | the supplied media make screens look finished |
| P3 | nodes_per_screen | D4 no meaningless empty space | + | sparse screens leave blank areas |

Same test as the process layer: within model, problem and protocol; 95% intervals from resampling
problems; one-sided p in the predicted direction; Holm correction across these 5. G0-failed runs excluded.
