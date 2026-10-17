---
name: comsol-agent-research-workflow
description: "Plan, build, run, and interpret COMSOL simulations through the official Java API and local command line. Use for inspecting existing models, designing controlled parameter studies, extracting fields and observables, or preparing simulation result reports."
---

# COMSOL Agent Research Workflow

Turn a research question into explicit model conditions, a manageable calculation, and an interpretable result. Use COMSOL's native Java API and command-line tools; a new MCP server is not required.

## Establish the task

Identify the requested observable before choosing a solver or producing plots. Record the geometry, dimensionality, physics, material laws, sources, boundary conditions, parameter ranges, and output units that matter to this task. Distinguish supplied conditions from assumptions. Ask only about missing choices that materially change the result; otherwise make and state a reasonable assumption.

For an existing model, first inspect available Java exports, model notes, and previous execution records. An MPH file is not self-explanatory source code: inspect a working copy through COMSOL when needed. Do not claim to have understood a model from its filename or a screenshot.

Preserve original models and results. Use separate outputs for changed conditions and retain the relationship between the input, generated code, command, and result. Continue within the user's existing execution authorization; do not introduce repeated approval steps for routine work.

## Build or modify the model

Read [model-and-api.md](references/model-and-api.md) when loading an existing model, creating physics features, changing selections, or interpreting dimensional conventions.

- Locate the actual installation and version, required physics modules, and usable compiler or launcher. Treat old paths and exported feature tags as clues to verify.
- Prefer installed official documentation and Java exported by the relevant COMSOL version for unfamiliar APIs. Enumerate the loaded model's tags and feature types before changing a presumed default feature.
- Use named or geometry-based selections where practical; verify their entity counts and locations after geometry changes.
- Keep physical sources, imposed boundary conditions, and measurement definitions distinct. Do not transfer a source law or material assumption from the bundled example to an unrelated problem.

## Execute a bounded study

Read [execution-and-analysis.md](references/execution-and-analysis.md) for batch execution, recovery, result extraction, and reporting.

Start an unfamiliar or expensive setup with a representative pilot: a small model, a short time interval, or a few parameter points. Use its solve time, memory behavior, and outputs to choose a batch size and concurrency that fit the available machine and license. A known lightweight continuation does not need a new pilot at every step.

Before scaling, verify the quantities that determine whether this task is meaningful: for example, contact selection and current sign, a conservation balance, a limiting case, or sensitivity to mesh/time resolution. Choose checks and tolerances for the requested claim; avoid reproducing an entire audit suite for every minor change.

Keep per-case logs and a checkpoint of completed, failed, and pending work. A successful process exit is not sufficient evidence of a solved case: confirm the expected model/result artifacts and usable numerical output. Resume verified completed work rather than restarting an entire sweep. Diagnose a repeated failure before expanding or retrying it.

## Interpret and deliver

Export the requested observables with coordinates, units, parameter values, and dataset/solution identity. Render representative plots and inspect them: distinguish the physical quantity being plotted from a derived or scanning-response map, and use consistent scales for comparisons.

Lead the report with the answer to the research question and explain which controlled comparison supports it. Keep numerical evidence proportionate and place detailed execution records after the main interpretation. Separate numerical completion, physical consistency, and agreement with an external experiment or paper. A qualitative spatial match does not establish a microscopic mechanism or absolute calibration.

For a literature example, state its source, adopted assumptions, and reconstruction limits. Use public inputs or independently constructed models for public deliverables; private research inputs remain private unless the user authorizes their release.

## Support and example

The initial project was exercised on Windows with COMSOL Multiphysics 6.4.0.293. Check API, launcher, module, and license differences in another environment; other platforms have not been validated by this release. COMSOL itself and appropriate licenses are external requirements.

This skill and its bundled references are self-contained. The optional [repository overview](https://github.com/LiX-Works/COMSOL-Agent-Research-Workflow) and [edge-current example](https://github.com/LiX-Works/COMSOL-Agent-Research-Workflow/tree/main/examples/edge-current) provide a separate runnable demonstration. `scripts/comsol-run.py` in that repository launches that example; it is not a general driver for arbitrary MPH files. Clone the repository separately when the demonstration is needed.
