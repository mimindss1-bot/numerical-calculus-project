# Self-assessment draft for student review

This maps the project to the supplied rubric. It is an assisted draft, not the student's confirmed assessment, an examiner's grade, or a guarantee of acceptance.

| Criterion | Maximum | Evidence | Provisional score |
|---|---:|---|---:|
| Problem formulation | 15 | Section 1: question, hypotheses, scope; Section 7: physical application | 13 |
| Writing and layout | 20 | Structured English report, labeled figures, generated result tables, linked navigation | 17 |
| Mathematics and research | 15 | Taylor cancellation through Richardson, quadrature bounds, variance propagation, references | 13 |
| Code quality | 15 | Reusable modules, input contracts, 34 tests, isolated verifier, CI | 13 |
| Methods and analysis | 20 | Six methods, multiple benchmarks, equal-cost comparisons, noise and domain/smoothness exceptions | 17 |
| Communication | 15 | Quantitative findings, conditional conclusions, limitations, runnable instructions | 13 |
| Total, provisional | 100 | Does not override minimum conditions | 86 |

## Minimum-condition evidence
- English Jupyter notebook, mathematics, Python, and a practical application: present.
- Functional code: 34 unit tests and 14 notebook code cells pass locally; GitHub Actions checks Python 3.12 and 3.14. Consult the Actions tab for the latest exact revision.
- GitHub repository: https://github.com/mimindss1-bot/numerical-calculus-project.
- Commit history: 10 actual commits, with substantive algorithm, experiment, validation, automation, and documentation work. The examiner determines meaningfulness.
- Examiner access: repository is public, with anonymous API access verified after the technical checks.
- Sources and assistance: Section 11 discloses substantial Codex assistance and credits course materials and external mathematical references. Additional course AI rules are not established by this document.

## Remaining human actions
- Review and explain the mathematics, experiments, and implementation personally.
- Adjust and confirm this self-assessment; check whether the course supplies a separate form.
- Confirm any additional course instructions and assistance policy.
- Submit the repository link before the deadline and retain the submission confirmation.

## Limitations
The benchmarks cover a small selection of mostly smooth scalar functions. Analytical references are evaluated in float64; there are no arbitrary-precision error references. The motion model and noise are synthetic, and independent Gaussian noise is only one possible measurement model. Function-value counts are not timing measurements. Empirical tolerance tables assume a known analytical answer and are not adaptive stopping rules. Public hosting alone does not constitute exam submission.
