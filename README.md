# Numerical Calculus: Accuracy, Resolution, and Computational Cost

[![Verification](https://github.com/mimindss1-bot/numerical-calculus-project/actions/workflows/verify.yml/badge.svg)](https://github.com/mimindss1-bot/numerical-calculus-project/actions/workflows/verify.yml)

An English-language mathematical report and executable Jupyter notebook for **Math Concepts for Developers**. It investigates accuracy and sampling cost in numerical differentiation and integration, then applies the methods to a synthetic motion model.

## Read the report
- [Executed Jupyter notebook](numerical_calculus.ipynb): main deliverable, with explanations, formulas, code, outputs, and figures.
- [HTML report](numerical_calculus.html): download and open in a browser; images are embedded, while mathematical typesetting may require Internet access for MathJax. GitHub does not render this HTML file as a hosted page.
- [Measured findings](results/executive_summary.md): tolerance budgets and limitations.
- [Self-assessment draft](SELF_ASSESSMENT.md) and [submission checklist](SUBMISSION_CHECKLIST.md).

## Question and methods
**How do method choice and sampling resolution affect numerical error and function-evaluation cost?**

| Task | Methods | Main tradeoffs studied |
|---|---|---|
| Derivatives | Forward, central, Richardson extrapolation | Truncation order, roundoff, domain boundaries, sample noise |
| Integrals | Left rectangles, trapezoids, midpoints | Convergence, equal sample budgets, tolerance targets, endpoint singularities |
| Application | Position → velocity; velocity → displacement | Independent analytical answer and physical units |

The report includes Taylor derivations, error bounds, three smooth benchmarks per task, a fourth-order comparison, matched-cost experiments, seeded Monte Carlo noise propagation, and counterexamples to overgeneralization. The scalar algorithms are implemented directly; library differentiation/quadrature is not used as a substitute.

## Reproduce
Use Python 3.12 or 3.14, the versions checked by GitHub Actions.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python verify_notebook.py
```

On Windows activate the virtual environment with `.venv\Scripts\activate` instead. Alternatively, open the notebook in Jupyter and select **Restart Kernel and Run All Cells** from the project directory so its two helper modules can be imported.

The verifier runs all cells in an isolated temporary directory and checks fresh execution order, embedded figures, table schemas, row counts, finite values, and generated summaries. Only validated outputs are copied back. Local Jupyter kernel ports must be permitted.

`tested-environment.txt` records the exact local environment; the broader dependency ranges do not imply every possible dependency combination was tested. CI installs dependencies independently on both supported Python versions. The Monte Carlo seed is fixed at 2026. Floating-point minima and last digits may vary across systems.

## Validation and results
- **34 standalone tests**, including exact known values, invalid inputs, sampled-value counts, convergence, variance propagation, and verifier failure cases.
- **14 executed notebook code cells**, **7 embedded figures**, **11 CSV tables**, and two generated Markdown summaries.
- Independent GitHub execution on Python **3.12 and 3.14**; see [the current run status](https://github.com/mimindss1-bot/numerical-calculus-project/actions).
- Near-first-, second-, and fourth-order derivative behavior on the declared smooth fitting ranges.
- For exp on [0,1], the first tested budgets meeting absolute error 10⁻⁷ are 1,024 midpoint samples and 2,048 trapezoid samples; left rectangles do not meet it within 8,192 tested samples.
- Equal sine endpoint values and a square-root endpoint singularity explain exceptions to a simple method ranking.

## Project layout
```text
numerical_calculus.ipynb       English report and executable experiments
numerical_calculus.html        Executed HTML export
numerical_methods.py           Six numerical algorithms and input validation
analysis_tools.py              Convergence, tolerance, and noise analysis helpers
tests/                        Independent regression tests
verify_notebook.py             Isolated execution and output validation
verification_manifest.json    Expected experiment artifact contract
results/                      Regenerated figures, CSVs, and measured summaries
.github/workflows/verify.yml   Cross-version CI with read-only repository permissions
SELF_ASSESSMENT.md             Rubric mapping for student review
SUBMISSION_CHECKLIST.md        Exact remaining submission obligations
DEVELOPMENT_LOG.md             Real development stages and verification evidence
```

## Course exercises

The [упражнения](упражнения/) folder contains the four supplied exercise notebooks and three GeoGebra resources. These study files are separate from the main project and its automated checks. See the folder README for the file list and attribution.

## Sources
Mathematical sources and course attribution are included in Section 11 of the notebook. The Taylor cancellations, midpoint bound, and variance calculations are explained in the report. The student must understand the work and confirm any additional course instructions. Course lecture files are not redistributed here.

## Submission
Repository: https://github.com/mimindss1-bot/numerical-calculus-project

The repository contains at least 10 actual development commits. Whether individual changes meet the course's definition of meaningful remains the examiner's judgment. The repository is public, as authorized by the owner; anonymous access was verified after the technical checks.

**Publication is not exam submission.** Submit the repository link through the course's designated channel **before 16:00 on 3 November 2026**. Student review, final self-assessment confirmation, and checking any additional course instructions remain necessary; see the checklist.
