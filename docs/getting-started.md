# Use the workflow

## Prepare your environment

Use a local coding agent with file and shell access, a licensed COMSOL installation with the physics modules your task requires, and its Java and command-line tools. The bundled example uses Python 3.10+ and the standard library; optional plotting dependencies are listed in `requirements.txt`.

The included example was developed on Windows with COMSOL 6.4.0.293. Other versions, operating systems, and physics interfaces need their own checks. The workflow guides work beyond this example, while the example is the concrete implementation exercised by the first release. The [validation record](../VALIDATION.md) separates the portable smoke test from the earlier full demonstration.

## Install the agent skill

Copy the complete [`skills/comsol-agent-research-workflow`](../skills/comsol-agent-research-workflow/) folder into a skill location supported by your agent. For a project-local Codex installation, use `.agents/skills/comsol-agent-research-workflow/`; see the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for other locations. Review an existing installation before replacing it.

Keep a checkout of this repository if you also want to run the example:

```sh
git clone https://github.com/LiX-Works/COMSOL-Agent-Research-Workflow.git
cd COMSOL-Agent-Research-Workflow
```

## Ask the agent

For an existing model:

```text
Use $comsol-agent-research-workflow to inspect this COMSOL model.
Explain its physics, parameters, boundary conditions, and current outputs.
Then help me plan a comparison of two source configurations.
```

For a new model:

```text
Use $comsol-agent-research-workflow to build a 2D conduction model
from these dimensions and boundary conditions. First run one
representative case, then export the potential and terminal currents.
```

These are task prompts for an agent, not commands that execute a solver by themselves. The skill guides the work; COMSOL performs the numerical solution.

## Run the bundled example

Follow the [edge-current example](../examples/edge-current/README.md) for the short check, full scan, optional plotting, and model assumptions. `scripts/comsol-run.py` is this example's launcher, not a general interpreter for arbitrary models.

Execution uses the native COMSOL Java API and command-line tools, with Python organizing the example's run. No additional MCP service is required.

Official references: [COMSOL API](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_intro.46.02.html) · [Batch and parameter sweeps](https://www.comsol.com/support/knowledgebase/1250).

## Project files

| Location | Purpose |
|---|---|
| [`skills/`](../skills/comsol-agent-research-workflow/) | Self-contained agent guidance |
| [`scripts/`](../scripts/) | Example launcher |
| [`examples/edge-current/`](../examples/edge-current/) | Model source, demonstration data, and interpretation |
| [`assets/source/`](../assets/source/) | Editable illustration builders |

This is an evolving first release. Keep copies of important models and interpret results with the task's assumptions in view.
