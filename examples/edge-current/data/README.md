# Supplied example results

These small files summarize an independent, public-source reconstruction calculated on 2026-10-17 with COMSOL 6.4.0.293. They are simulated values, not experimental measurements and not the original authors' data.

- `representative-points.csv`: 20 edge-normal source positions (6 S0, 6 S1, 8 S2), with auxiliary-integral and direct-solve currents. `error_scaled_to_source` is `abs(direct-kernel) / max(abs(kernel), 0.01*source_probe_peak)`; the peak is calculated separately for each geometry's edge-normal source.
- `historical-summary.json`: numerical summaries and their scope. The S0 mesh result does not imply that S1 and S2 underwent separate refinement studies.

Positions are in µm; currents are in A. Positive current is outward through the bottom readout contact. Source amplitude is an arbitrary demonstration parameter, $q_0=0.01$ A/m; absolute currents are not calibrated to the paper's experiment.

The original calculation checked several source definitions. The initial online acceptance scale mixed their amplitudes; the values supplied here come from a subsequent source-specific audit of the saved output. This was an offline recalculation of error metrics, without new solves. The new public launcher directly uses source-specific scales and exports its own `audit.json` into each run directory.

The two PNGs in `../assets/` are figures from the historical calculation. A new `--smoke` run generates only four isolated scan samples and cannot reproduce those full maps. No experimental data, paper PDFs, COMSOL binaries, or precomputed MPH models are included.
