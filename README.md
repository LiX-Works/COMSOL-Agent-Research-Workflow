# COMSOL Agent Research Workflow

**Work with an AI agent to build COMSOL models, run studies, and explain the results.**

Describe your research task. The agent helps develop the model, organize calculations, and use the results to decide what to change next.

![Agent research loop: build a model, run in COMSOL, inspect results, and refine the model; produce plots and findings](assets/workflow.svg)

## Example: edge-current collection

We applied the workflow to a reconstructed four-cross conductor using the edge-source collection model of Ma et al. [1]. The calculated response shows same-sign left/right shoulder hotspots, with polarity alternating between lower and upper shoulders along the channel.

![Calculated scanning-current response and longitudinal scan profiles](examples/edge-current/assets/example-results.png)

**Figure 1.** **(A)** Bottom-electrode current versus illumination-spot position. **(B)** Scan profiles at x = ±0.7 µm; grey bands indicate the cross arms. Both panels are normalized by the maximum absolute current of the complete scan. The geometry is approximate and the source strength illustrative; the comparison is qualitative, without experimental current calibration.

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

[Chinese](README.zh-CN.md) · [MIT License](LICENSE) · [Attribution](NOTICE.md)
