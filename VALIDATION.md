# First-release validation

Checked on 2026-10-17 with Windows and COMSOL Multiphysics 6.4.0.293.

## Portable example

The committed Java model was compiled and executed through `scripts/comsol-run.py` in S0 smoke mode, using a fresh output directory outside the repository. It completed one auxiliary and two source-on steady solves, four isolated scan samples, an auxiliary MPH, field export, and representative-point audit.

| Check | Result |
|---|---:|
| Maximum direct versus auxiliary-integral scaled error | 0.145901% |
| Integration order 6 versus 10, local scaled error | 0.025925% |
| Terminal-current conservation / source probe peak | 1.36e-9 |
| Independent outward flux versus native terminal current / source probe peak | 4.02e-8 |

The source scale for these checks is EdgeNormal's own representative-point peak. A 1% peak floor is used near zero. The numerical checks passed their 1% tolerance; this is not a statement of agreement with experiment.

This smoke check establishes the short execution path, not a resolved spatial map or mesh-convergence study. New portable full S0/S1/S2 scans were not run for this release. The example's supplied illustration and historical summary are separately identified in its documentation.

## Offline and presentation checks

- Skill frontmatter and metadata validation passed.
- An independent, read-only skill exercise covered a changed model, stale completion markers, a license failure, and a proposed 50-position study.
- Python syntax, help, and dry-run behavior passed; dry-run did not create an output directory.
- Existing-output rejection and invalid thread-count handling passed.
- The optional plotting script generated a full scan plot from a separately identified historical demonstration CSV using isolated plotting dependencies. It rejected the sparse smoke output as a full map.
- Local documentation links, English publication content, and personal-path screening passed. README.zh-CN.md is the intentional Chinese translation.
- The workflow SVG and result plot were rendered and visually inspected.

An initial smoke attempt stopped before any solve because Java file-directory creation was disallowed by COMSOL's existing security preferences. The launcher now creates directories in Python and writes model outputs through COMSOL's own API. No global COMSOL security preference was changed.

Generated models, logs, local environments, and detailed private run records are excluded from this repository.
