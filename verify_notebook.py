"""Run from the project directory with the documented dependencies installed."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter


def main():
    root = Path(__file__).resolve().parent
    path = root / "numerical_calculus.ipynb"
    notebook = nbformat.read(path, as_version=4)
    NotebookClient(notebook, timeout=120, kernel_name="python3",
                   resources={"metadata": {"path": str(root)}}).execute()
    nbformat.validate(notebook)
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert all(cell.execution_count is not None for cell in code_cells)
    assert not any(output.output_type == "error" for cell in code_cells for output in cell.outputs)
    figures = sum("image/png" in output.get("data", {}) for cell in code_cells for output in cell.outputs)
    assert figures == 5, f"Expected five figures, got {figures}"
    nbformat.write(notebook, path)
    html, _ = HTMLExporter().from_notebook_node(notebook)
    (root / "numerical_calculus.html").write_text(html)
    print(f"Verified {len(code_cells)} code cells and {figures} figures; HTML updated.")


if __name__ == "__main__":
    main()
