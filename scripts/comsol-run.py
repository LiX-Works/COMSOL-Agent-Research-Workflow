#!/usr/bin/env python3
"""Compile and run the bundled edge-current example using local COMSOL.

This is a launcher for one example, not a general model interpreter. The run
directory must be new. The launcher never opens a previously saved MPH file.
Only the Python standard library is needed for execution and numerical audit.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone
from uuid import uuid4


REPOSITORY = Path(__file__).resolve().parents[1]
EXAMPLE = REPOSITORY / "examples" / "edge-current"
SOURCE = EXAMPLE / "model" / "Ma2019Cross.java"
SOURCE_NAMES = ["BulkFixed", "EdgeFixed", "EdgeNormal", "EdgeX", "EdgeY"]


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def parser() -> argparse.ArgumentParser:
    arg = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    arg.add_argument("--comsol-home", type=Path, default=os.environ.get("COMSOL_HOME"),
                     help="COMSOL Multiphysics installation directory; or set COMSOL_HOME")
    arg.add_argument("--geometry", choices=("S0", "S1", "S2"), default="S0",
                     help="S0: single cross; S1: single cross with side grounds; S2: four crosses")
    arg.add_argument("--output", type=Path,
                     help="new run directory (default: runs/edge-current/<unique timestamp>)")
    arg.add_argument("--threads", type=int, default=4, help="COMSOL thread count (default: 4)")
    arg.add_argument("--smoke", action="store_true",
                     help="two direct points, four scan samples; proves execution only, not a spatial map")
    arg.add_argument("--dry-run", action="store_true",
                     help="print commands and expected work without creating files or starting COMSOL")
    return arg


def make_plan(args: argparse.Namespace) -> dict:
    if args.comsol_home is None:
        raise ValueError("Supply --comsol-home or set COMSOL_HOME to your licensed installation.")
    if args.threads < 1:
        raise ValueError("--threads must be positive.")
    home = args.comsol_home.expanduser().resolve()
    # These installation paths are for COMSOL 6.4 on Windows, the tested platform.
    javac = home / "java" / "win64" / "jre" / "bin" / "javac.exe"
    batch = home / "bin" / "win64" / "comsolbatch.exe"
    for file in (javac, batch, SOURCE):
        if not file.is_file():
            raise ValueError(f"Required file does not exist: {file}")
    output = args.output or REPOSITORY / "runs" / "edge-current" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8])
    output = output.expanduser().resolve()
    if output.exists():
        raise ValueError(f"Output already exists; choose a new directory: {output}")
    build = output / "build"
    wrapper = build / "EdgeCurrentMain.java"
    direct_points = 2 if args.smoke else (8 if args.geometry == "S2" else 6)
    return {
        "geometry": args.geometry,
        "mode": "smoke" if args.smoke else "full-example",
        "output": str(output),
        "source": str(SOURCE),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "expected_direct_points": direct_points,
        "expected_steady_solves": 1 + direct_points,
        "expected_scan_rows": 4 if args.smoke else (3956 if args.geometry == "S2" else 2346),
        "compile_command": [str(javac), "-proc:none", "-encoding", "UTF-8", "-cp",
                            str(home / "plugins" / "*"), "-d", str(build), str(SOURCE), str(wrapper)],
        "batch_command": [str(batch), "-inputfile", str(build / "EdgeCurrentMain.class"),
                          "-classpathadd", str(build), "-nosave", "-autosave", "off",
                          "-np", str(args.threads), "-batchlogout", "-batchlog",
                          str(output / "logs" / "batch.log")],
    }


def records_from_log(path: Path) -> dict:
    records = {key: [] for key in ("K", "D", "ORDER", "SOLVED", "COMPLETE")}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        fields = line.strip().split(",")
        if fields[0] in records:
            records[fields[0]].append(fields[1:])
    return records


def finite(values: list[str]) -> list[float]:
    numbers = [float(value) for value in values]
    if not all(math.isfinite(value) for value in numbers):
        raise ValueError("Non-finite result in COMSOL output.")
    return numbers


def audit_results(plan: dict) -> dict:
    """Use EdgeNormal's own point scale, never a mixed-source peak."""
    output = Path(plan["output"])
    data = output / "data"
    record = records_from_log(output / "logs" / "stdout.log")
    shape = plan["geometry"]
    label = shape + "_public"
    if [label] not in record["COMPLETE"]:
        raise ValueError("COMSOL completion marker missing; inspect the saved logs.")
    if len(record["SOLVED"]) != plan["expected_steady_solves"]:
        raise ValueError("Unexpected number of successful steady solves.")
    probes = []
    scans = []
    for row in record["K"]:
        values = finite(row[1:])
        if len(values) != 7:
            raise ValueError("Unexpected kernel result shape.")
        (scans if row[0] == shape + "_map" else probes).append(values)
    if len(scans) != plan["expected_scan_rows"] or len(probes) != plan["expected_direct_points"]:
        raise ValueError("Unexpected scan or probe row count.")
    headers = ["x_um", "y_um"] + [name + "_A" for name in SOURCE_NAMES]
    write_csv(data / "scan.csv", headers, scans)
    write_csv(data / "probe-kernels.csv", headers, probes)
    peak = max(abs(row[4]) for row in probes)  # x, y, Bulk, Fixed, Normal
    if peak <= 1e-20:
        raise ValueError("No resolved EdgeNormal representative response.")
    terminals = {"S0": 2, "S1": 3, "S2": 9}[shape]
    if len(record["D"]) != plan["expected_direct_points"]:
        raise ValueError("Incomplete source-on direct solve results.")
    rows = []
    direct_rows = []
    for row in record["D"]:
        if int(row[1]) != 2:
            raise ValueError("Unexpected direct-source index.")
        x, y, predicted, *values = finite(row[2:])
        if len(values) != 3 * terminals:
            raise ValueError("Unexpected terminal output shape.")
        native, potentials, flux = values[:terminals], values[terminals:2*terminals], values[2*terminals:]
        direct = -native[0]  # Fixed convention: outward bottom-contact sheet flux.
        rows.append({
            "x_um": x, "y_um": y, "kernel_A": predicted, "direct_A": direct,
            "scaled_direct_kernel_error": abs(direct-predicted) / max(abs(predicted), 0.01*peak),
            "native_conservation_over_source_peak": abs(sum(native)) / peak,
            "independent_flux_vs_negative_native_over_source_peak": max(abs(a+b) for a, b in zip(native, flux)) / peak,
            "independent_floating_flux_over_source_peak": max(map(abs, flux[1:7])) / peak if shape == "S2" else 0.0,
        })
        direct_rows.append([x, y, predicted, direct] + native + potentials + flux)
    write_csv(data / "direct-points.csv", ["x_um", "y_um", "kernel_A", "direct_A"] +
              [f"native_I{i+1}_A" for i in range(terminals)] +
              [f"terminal_V{i+1}_V" for i in range(terminals)] +
              [f"outward_sheet_flux_{i+1}_A" for i in range(terminals)], direct_rows)
    if len(record["ORDER"]) != plan["expected_direct_points"]:
        raise ValueError("Incomplete integration-order comparison.")
    order_errors = []
    for row in record["ORDER"]:
        point = int(row[1])
        differences = finite(row[2:])
        if len(differences) != 5:
            raise ValueError("Unexpected integration-order output shape.")
        order_errors.append(abs(differences[2]) / max(abs(probes[point][4]), 0.01*peak))
    if not (data / f"{shape}_fields_COMSOL.csv").is_file():
        raise ValueError("Auxiliary-field export missing.")
    if not (output / "models" / f"{shape}_weighting.mph").is_file():
        raise ValueError("New auxiliary model output missing.")
    metrics = {key: max(row[key] for row in rows) for key in rows[0] if key.endswith("error") or key.endswith("peak")}
    metrics["integration_order_6_vs_10_local_scaled_error"] = max(order_errors)
    passed = max(metrics.values()) <= 0.01
    result = {
        "geometry": shape, "mode": plan["mode"], "source": "EdgeNormal",
        "direct_points": len(rows), "scan_rows": len(scans),
        "edge_normal_probe_peak_A": peak, "native_to_outward_current_sign": -1,
        "relative_error_floor_fraction_of_source_probe_peak": 0.01,
        "tolerance": 0.01, "metrics": metrics, "pass": passed, "points": rows,
        "scope": "Representative-point consistency checks; no mesh-refinement study in this launcher.",
        "smoke_limitation": "Four isolated scan samples cannot establish spatial hotspot topology." if plan["mode"] == "smoke" else None,
    }
    write_json(data / "audit.json", result)
    if not passed:
        raise ValueError("Representative-point checks failed; preserve and inspect audit.json and logs.")
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        plan = make_plan(args)
    except ValueError as exc:
        parser().error(str(exc))
    if args.dry_run:
        print(json.dumps(plan, indent=2))
        return 0
    output = Path(plan["output"])
    output.mkdir(parents=True, exist_ok=False)
    for directory in ("build", "data", "models", "logs"):
        (output / directory).mkdir()
    status = {"state": "PREPARING", "started_utc": datetime.now(timezone.utc).isoformat(), "plan": plan}
    write_json(output / "run.json", status)
    # Bake the destination into a generated, run-local Java entry point; the
    # committed model source remains unchanged and contains no personal paths.
    wrapper = "public class EdgeCurrentMain { public static void main(String[] args) throws Exception { Ma2019Cross.execute(" + \
        json.dumps(args.geometry) + "," + json.dumps(output.as_posix()) + "," + str(args.smoke).lower() + "); } }\n"
    (output / "build" / "EdgeCurrentMain.java").write_text(wrapper, encoding="utf-8")
    started = time.monotonic()
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    try:
        compiled = subprocess.run(plan["compile_command"], cwd=output / "build", capture_output=True, creationflags=flags)
        (output / "logs" / "compile.log").write_bytes(compiled.stdout + compiled.stderr)
        if compiled.returncode:
            raise ValueError("Java compilation failed; inspect logs/compile.log.")
        status["state"] = "RUNNING"
        write_json(output / "run.json", status)
        print(f"Running {args.geometry} ({plan['mode']}); results: {output}", flush=True)
        with (output / "logs" / "stdout.log").open("wb") as out, (output / "logs" / "stderr.log").open("wb") as err:
            executed = subprocess.run(plan["batch_command"], cwd=output / "build", stdout=out, stderr=err, creationflags=flags)
        status["batch_exit_code"] = executed.returncode
        if executed.returncode:
            raise ValueError("COMSOL batch command failed; inspect logs.")
        audit = audit_results(plan)  # A zero process exit code alone is insufficient.
        status.update(state="COMPLETE", audit_pass=audit["pass"])
        print(f"Complete. Representative-point audit passed; read {output / 'data' / 'audit.json'}")
        return 0
    except (OSError, ValueError) as exc:
        status.update(state="FAILED", error=str(exc))
        print(f"Failed: {exc}\nRun outputs preserved: {output}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        status.update(state="INTERRUPTED", error="Interrupted by user; inspect any remaining COMSOL process before retrying.")
        raise
    finally:
        status.update(wall_seconds=round(time.monotonic()-started, 3), finished_utc=datetime.now(timezone.utc).isoformat())
        write_json(output / "run.json", status)


if __name__ == "__main__":
    sys.exit(main())
