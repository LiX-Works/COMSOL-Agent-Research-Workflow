# Model inspection and API choices

Read this when a task involves an existing MPH file, unfamiliar physics features, geometry changes, or dimensional conventions. Use the installed documentation for exact syntax and supported options.

## Recover the model conditions

For a supplied model, identify its components, geometry dimensions and units, materials, physics interfaces, studies, solver sequences, and datasets. Then trace the requested observable back to the expressions, solution, and selections that define it. A model may contain old studies or datasets unrelated to the latest result.

Useful evidence includes an exported Java model, the author's notes, logged parameter values, and information queried from a COMSOL-loaded copy. A Java export describes a model configuration; it does not by itself prove that the corresponding study was run or that a stored solution is current. Do not overwrite the original while inspecting or exporting it.

For a new model, make a compact specification before implementation:

| Item | What changes the calculation |
| --- | --- |
| Geometry | Dimensions, coordinate system, symmetry reductions, relevant small features |
| Physics | Governing interface, constitutive law, coupling, stationary/transient/frequency domain |
| Sources | Spatial support, direction, normalization, time or frequency dependence |
| Boundaries | Prescribed values or fluxes, insulation, contact conditions, initial conditions |
| Measurement | Observable, sign, integration region, units, selected solution |
| Comparison | Parameter varied, conditions held fixed, expected limiting behavior |

Reuse the task's existing notes rather than generating a separate document just to fill this table.

## Discover instead of guessing

Locate the installed API reference, Programming Reference Manual, and physics-specific documentation. A small Java model exported from the GUI can resolve uncertain feature types and property names more reliably than adapting a distant-version snippet.

For an existing model, collections expose tags that can be enumerated; for example, `model.component().tags()` and, for a known component and physics tag, `model.component(componentTag).physics(physicsTag).feature().tags()`. Inspect the discovered feature's type and supported properties before editing it. These queries reveal structure, not the physical correctness of its settings.

Do not assume tags such as `comp1`, `geom1`, `ec`, `cucn1`, or `sol1` exist. New geometry operations can also change entity numbering. After a rebuild, check the selection's dimension, entity count, and physical location; a nonempty selection can still select the wrong boundary. Distinguish independent floating contacts from contacts electrically tied together.

Compile or run a minimal model before adding a large sweep. If an API property fails, inspect that feature and the installed documentation; repeatedly substituting plausible property names is not a sound discovery method. Do not infer the method's validity solely from successful Java compilation: many model settings are checked during runtime or solve.

## Units and dimensional reduction

Track geometric units, constitutive coefficients, source densities, and output integration units separately. Explicit units in parameter expressions help reveal mistakes that bare numbers hide.

For a reduced-dimensional electrical model, determine how that physics interface represents thickness. A two-dimensional geometry does not automatically mean the source or conductivity uses sheet units. If a sheet formulation is implemented through a thickness-based bulk interface, verify the conversion of sheet conductance and source density together, as well as how terminal current and flux integrals include thickness. Changing an arbitrary effective thickness should not change the intended sheet problem when all conversions are consistent. This check is conditional on that formulation, not a requirement to add `d_eff` to every model.

Check the definition of fitted or quoted widths: Gaussian radius, diameter, full width at half maximum, and standard deviation are different parameters. Likewise, a fixed source component and a fixed total vector magnitude define different parameter studies.

## Sources, fields, and terminal readouts

An imposed source term, the total field/current, and an integrated terminal response are different quantities. State which is being plotted. For current signs, reconcile the chosen terminal convention with an explicitly oriented flux or another independent definition; do not choose the sign merely to match a reference image.

If a reciprocity or weighting-field shortcut is used, establish that its linearity and boundary assumptions apply, and compare a few representative direct solves. Source-dependent conductivity, nonlinear material response, or changed contact conditions can invalidate reuse of one auxiliary field. A shortcut validated for one model is not a general property of COMSOL.
