"""Execute in an isolated directory, validate regenerated artifacts, then export."""
from pathlib import Path
import csv
import json
import math
import shutil
import tempfile
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter


def validate_notebook(notebook, expected_cells, expected_figures):
    nbformat.validate(notebook)
    cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    if len(cells) != expected_cells or [c.execution_count for c in cells] != list(range(1, expected_cells+1)):
        raise ValueError("not all expected cells executed in fresh-kernel order")
    if any(output.output_type == "error" for cell in cells for output in cell.outputs):
        raise ValueError("notebook contains an error output")
    figures = sum("image/png" in output.get("data", {}) for cell in cells for output in cell.outputs)
    if figures != expected_figures:
        raise ValueError(f"expected {expected_figures} embedded figures, got {figures}")


def validate_result_files(directory, manifest):
    for filename in manifest["figures"]:
        path = directory / filename
        if not path.is_file() or path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"missing or invalid PNG: {filename}")
    for filename, schema in manifest["tables"].items():
        with (directory / filename).open(newline="") as stream:
            reader = csv.DictReader(stream)
            fields = reader.fieldnames or []
            rows = list(reader)
        if len(rows) != schema["rows"] or not set(schema["numeric"]).issubset(fields):
            raise ValueError(f"wrong table shape or columns: {filename}")
        for row in rows:
            for column in schema["numeric"]:
                value = row[column]
                if value in ("not reached", "not applicable"):
                    if filename not in ("tolerance_budgets.csv", "domain_boundaries.csv"):
                        raise ValueError(f"unexpected censored value: {filename}")
                    continue
                if not math.isfinite(float(value)):
                    raise ValueError(f"non-finite table value: {filename}:{column}")
    summary = directory / "measured_orders.md"
    if not summary.is_file() or "Richardson" not in summary.read_text():
        raise ValueError("missing convergence summary")


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "verification_manifest.json").read_text())
    path = root / "numerical_calculus.ipynb"
    notebook = nbformat.read(path, as_version=4)
    with tempfile.TemporaryDirectory(prefix="numerical-calculus-") as scratch:
        work = Path(scratch)
        for module in ("numerical_methods.py", "analysis_tools.py"):
            shutil.copy2(root / module, work / module)
        NotebookClient(notebook, timeout=180, kernel_name="python3",
                       resources={"metadata": {"path": str(work)}}).execute()
        validate_notebook(notebook, manifest["code_cells"], len(manifest["figures"]))
        validate_result_files(work / "results", manifest)
        html, _ = HTMLExporter().from_notebook_node(notebook)
        # Publish only successfully regenerated and validated results.
        (root / "results").mkdir(exist_ok=True)
        for artifact in (work / "results").iterdir():
            shutil.copy2(artifact, root / "results" / artifact.name)
        nbformat.write(notebook, path)
        (root / "numerical_calculus.html").write_text(html)
    print(f"Verified {manifest['code_cells']} code cells, {len(manifest['figures'])} figures, "
          f"and {len(manifest['tables'])} CSV tables; HTML updated.")


if __name__ == "__main__":
    main()
