# Execution, recovery, and result interpretation

Read this for a parameter sweep, a long solve, a rerun after failure, or preparation of numerical outputs and a report. Adapt the procedure to the cost and claim of the current task.

## Establish the native execution path

Find the actual COMSOL executable, installed version, compatible Java compiler/runtime, and required physics modules. Read the installed command-line help for the current platform before selecting flags. An available binary is not evidence that a license checkout or a specific physics solve will succeed.

The usual local path is generated or exported Java code followed by COMSOL's compiler/batch facilities. Depending on the installation, compilation may use the bundled Java compiler with COMSOL's libraries. Keep the classpath and working directory explicit; do not silently compile against a different COMSOL version. Use argument arrays when launching processes to avoid shell quoting errors.

When automation launches a background job, retain a process identifier and separate stdout/stderr or a batch log. On Windows, keep helper windows hidden unless an interactive window is needed. Avoid accidentally creating additional GUI sessions or competing solver processes when resuming an existing job.

## Pilot, then scale

Choose a pilot that exercises the risky part of the requested calculation: a representative material regime, difficult geometry, relevant source location, or short transient interval. Include the outputs needed to judge success. Record elapsed time and model size or resource use when available.

Define the planned case list, concurrency, and practical run budget before a large sweep. Estimate cost from the pilot, leaving room for initialization and slow cases. Increase parallelism only when memory, license availability, and solver threading permit it. More concurrent processes can reduce throughput on an oversubscribed machine.

Use a check suited to the result's intended interpretation. Examples include a conserved balance for a transport model, a known limit, representative direct solves of an accelerated method, or a modest resolution change at a critical point. Compare both absolute and relative error where a quantity can approach zero. Do not promote the bundled example's numeric tolerances to a universal acceptance standard.

## Checkpoints and failure handling

For each case, retain enough information to reconstruct its conditions: code/input identity, parameters, COMSOL version, command, timestamps, output locations, and completion state. Save checkpoints atomically when possible. A checkpoint must represent completed, usable output rather than merely a launched process.

On resume, compare the current code and parameters with the checkpoint's inputs before skipping a case. Preserve failed attempts and their logs. Distinguish launch/license failures, API/model setup errors, solver nonconvergence, and output/parsing failures; each needs a different correction. Repair the failed stage and continue unaffected verified cases within the task's existing scope.

Use a bounded retry only when the failure appears transient and retrying is appropriate. Repeatedly launching the same failing solver without changing the diagnosed cause wastes resources. Stop or isolate the failed case when the budget is exhausted; report which results remain usable and what is unresolved.

## Numerical output and figures

Confirm that expected outputs exist, required columns or fields are present, values are finite where expected, and the intended solution/dataset was selected. A CSV created by an older run or a solver exit code alone does not establish successful completion of the current case.

Export the observable with its units, coordinates, parameter values, and solution identity. Preserve numeric data alongside plotted results. For map comparisons, use matching axes, physical extents, and a shared color scale when amplitude matters. If each map is normalized separately, say so: similar normalized shapes do not imply equal signal strengths. Inspect a rendered plot for missing regions, misleading interpolation, and unreadable labels.

## Report the scientific result

Start with the question, the result, and the comparison that supports it. Explain the model assumptions needed to understand the conclusion. Keep run logs, detailed checks, and implementation diagnostics in a later section or linked output record.

Distinguish three levels of evidence:

- **Execution:** the requested cases ran and produced usable output.
- **Model consistency:** selected balances, limits, or numerical checks support the implementation within the tested conditions.
- **External agreement:** results reproduce a specified feature or measurement of a cited source under stated approximations.

Make the claim at the level supported by the evidence. In a public example, attribute the adopted physical model and distinguish it from the project's workflow, code, and analysis contributions. State qualitative agreement, quantitative calibration, and untested microscopic mechanisms separately when relevant.
