# COMSOL Agent Research Workflow

[Chinese](README.zh-CN.md) · [Agent skill](skills/comsol-agent-research-workflow/SKILL.md) · [Worked example](examples/edge-current/README.md)

**Guide an AI agent through COMSOL modeling, simulation, and research analysis.**

Connect physical assumptions, Java API model code, batch runs, and result interpretation in a practical workflow. The repository provides an installable skill, a small runnable example, and a way to keep model choices and computational results understandable as a project develops.

![Research question to model, calculation, analysis, and interpretation](assets/workflow.svg)

## What the workflow helps you do

- **Understand and develop a model.** Turn a research question or an existing model into explicit geometry, materials, source terms, boundary conditions, and quantities to evaluate.
- **Run calculations with a clear purpose.** Use the native COMSOL Java API and command-line tools, starting with a small calculation before extending to a scan or a batch.
- **Connect results to an explanation.** Compare controlled cases, inspect fields and terminal quantities, and write conclusions that remain connected to the assumptions and exported data.

The skill guides an existing coding agent; COMSOL performs the numerical solution. You can discuss and revise the problem with the agent throughout the process.

## How a task progresses

| Stage | The work | A useful output |
|---|---|---|
| Define | Specify the physical question, assumptions, and observation | A concise model specification |
| Model | Create or inspect geometry, selections, physics, and solver setup | Java model code and a saved model when needed |
| Run | Try a representative case, then organize the requested calculations | Results, progress, and logs |
| Analyze | Compare cases and choose checks relevant to the physics | Plots, tables, and an explanation of differences |
| Explain | Relate the findings to the original question | A readable report with stated scope |

The sequence can be adapted to the task. A parameter edit does not need a new research plan; an unfamiliar model usually needs inspection before modification.

## Start with the agent skill

Copy the complete [`skills/comsol-agent-research-workflow`](skills/comsol-agent-research-workflow) folder into a skill location supported by your agent. For a project-local Codex installation, use `.agents/skills/comsol-agent-research-workflow/`; see the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery locations.

For example, from a checkout of this repository, copy the folder to your research project's `.agents/skills/` directory. Keep the checkout if you want to run the example as well. Existing skill installations should be reviewed before replacing them.

Then ask:

```text
Use $comsol-agent-research-workflow to inspect this COMSOL model.
Explain its physics, parameters, boundary conditions, and current outputs.
Then help me plan a comparison of two source configurations.
```

Or start from a model definition:

```text
Use $comsol-agent-research-workflow to build a 2D conduction model
from these dimensions and boundary conditions. First run one
representative case, then export the potential and terminal currents.
```

These are task prompts for an agent, not commands that execute a solver by themselves.

To get the runnable example, clone this repository:

```sh
git clone https://github.com/LiX-Works/COMSOL-Agent-Research-Workflow.git
cd COMSOL-Agent-Research-Workflow
```

## Execution and requirements

The native execution path is **Java model code → COMSOL batch → exported data and analysis**. Python can organize the run and its output. No additional MCP server is required.

You need a local coding agent with file and shell access, a licensed COMSOL installation with the physics modules your task requires, and its Java/command-line tools. The bundled example uses Python 3.10+ and the standard library; its exact commands and dependencies are documented separately.

The included example was developed with **Windows and COMSOL 6.4.0.293**. Other versions, operating systems, and physics interfaces need their own checks. The workflow can guide work beyond this example, but the example is the concrete tested implementation provided in this first release.

Official references: [COMSOL API](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_intro.46.02.html) · [Batch and parameter sweeps](https://www.comsol.com/support/knowledgebase/1250).

## A small worked example

[**Local current sources and electrode response**](examples/edge-current/README.md) demonstrates model construction, a small execution path, and spatial-response analysis in cross-shaped conducting sheets. It compares fixed-direction and edge-normal current sources using a model informed by Ma et al. (2019).

The example is one application of the workflow. Its documentation explains the source assumptions, approximate geometry, runnable commands, and the qualitative response features. It uses newly generated demonstration data; the source strength is an illustrative scale rather than an experimental fit. The paper is credited within the example.

## Repository guide

| Location | Contents |
|---|---|
| [`skills/`](skills/comsol-agent-research-workflow/) | Agent instructions and focused references |
| [`scripts/`](scripts/) | The bundled example launcher |
| [`examples/edge-current/`](examples/edge-current/) | Model source, commands, result illustration, and attribution |
| [`assets/workflow.svg`](assets/workflow.svg) | Editable workflow illustration |

## Project status

See [first-release validation](VALIDATION.md) for the exact checks and their limits.

This is a compact first release. The workflow guidance, documentation, and packaging will evolve with further use. Keep a copy of important models, review generated changes, and interpret numerical results with the assumptions of the task in view.

## License

[MIT](LICENSE). COMSOL and its documentation are separate products and are not included. This is an independent project; see [NOTICE](NOTICE.md) for attribution and names used in the repository.
