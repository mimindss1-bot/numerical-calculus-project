import tempfile
import unittest
from pathlib import Path
import nbformat
from verify_notebook import validate_notebook, validate_result_files


class VerificationTests(unittest.TestCase):
    def test_missing_execution_is_rejected(self):
        notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("x=1")])
        with self.assertRaises(ValueError):
            validate_notebook(notebook, 1, 0)

    def test_error_outputs_are_rejected(self):
        cell = nbformat.v4.new_code_cell("1/0", execution_count=1,
             outputs=[nbformat.v4.new_output("error", ename="ZeroDivisionError", evalue="", traceback=[])])
        with self.assertRaises(ValueError):
            validate_notebook(nbformat.v4.new_notebook(cells=[cell]), 1, 0)

    def test_missing_embedded_figure_is_rejected(self):
        cell = nbformat.v4.new_code_cell("x=1", execution_count=1)
        with self.assertRaises(ValueError):
            validate_notebook(nbformat.v4.new_notebook(cells=[cell]), 1, 1)

    def test_bad_table_values_and_missing_files_are_rejected(self):
        manifest = {"figures": [], "tables": {"data.csv": {"rows": 1, "numeric": ["error"]}}}
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory/"data.csv").write_text("error\nnan\n")
            with self.assertRaises(ValueError):
                validate_result_files(directory, manifest)
            (directory/"data.csv").write_text("error\n0.1\n")
            (directory/"measured_orders.md").write_text("Richardson")
            validate_result_files(directory, manifest)
            with self.assertRaises(ValueError):
                validate_result_files(directory, {"figures": ["missing.png"], "tables": {}})
