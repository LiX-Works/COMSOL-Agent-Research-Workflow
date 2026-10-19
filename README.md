# COMSOL Agent Research Workflow

**English** | [简体中文](README.zh-CN.md)

A Skill that lets a coding agent build, run, and check COMSOL Multiphysics studies through the native Java API and command line, without an MCP server. The checks are part of the workflow:

- The observable, boundary conditions, and assumptions are stated before a model is built or changed.
- A representative trial sets the scale of the full study; interrupted sweeps resume from checkpoints.
- Conservation, limiting cases, and mesh sensitivity are checked before results are interpreted.
- Numerical completion, physical consistency, and agreement with experiment are reported separately.

![Agent research loop led by an AI agent: build a model, run it in COMSOL, inspect the results, and refine the model; inspection can send cases back to rerun, and results leave the loop as plots and a report](assets/workflow.png)

## Example: edge-current collection

We applied the workflow to a reconstructed four-cross conductor using the edge-source collection model of Ma et al. [1]. The calculated response shows same-sign left/right shoulder hotspots, with polarity alternating between lower and upper shoulders along the channel.

![Calculated scanning-current response and longitudinal scan profiles](examples/edge-current/assets/example-results.png)

**Figure 1.** **(a)** Bottom-electrode current versus illumination-spot position. **(b)** Scan profiles at x = ±0.7 µm; grey bands indicate the cross arms. Both panels are normalized by the maximum absolute current of the complete scan. The geometry is approximate and the source strength illustrative; the comparison is qualitative, without experimental current calibration.

**[1]** Ma, Q. et al. *Giant intrinsic photoresponse in pristine graphene.* **Nature Nanotechnology 14**, 145–150 (2019). [doi:10.1038/s41565-018-0323-8](https://doi.org/10.1038/s41565-018-0323-8).

[Example methods, data, and code →](examples/edge-current/README.md)

## Try the workflow

Copy [`comsol-agent-research-workflow`](skills/comsol-agent-research-workflow/) into your agent's skill folder, then ask:

```text
Use $comsol-agent-research-workflow to inspect this model,
plan a comparison, run a representative case, and explain the results.
```

**[Setup and usage →](docs/getting-started.md)**

Requires a local coding agent and licensed COMSOL. Uses the native Java API and command line; no additional MCP server. The bundled example was checked on Windows with COMSOL 6.4.0.293. [Validation details](VALIDATION.md).

[MIT License](LICENSE) · [Attribution](NOTICE.md)
