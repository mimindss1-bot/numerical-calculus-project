# Development and verification record

The initial project and its repository-status update formed the first two commits. The owner then requested eight real improvements. These were developed and tested sequentially; no empty commits, artificial backdating, or cosmetic-only changes were used to reach the count.

| Commit stage | Actual change | Verification |
|---:|---|---|
| 1 | Initial English report, four methods, benchmark experiments, application, results | Fresh-kernel notebook execution |
| 2 | Repository setup and outstanding-submission documentation | Remote push and notebook-file presence |
| 3 | Reusable numerical module; finite-input, shape, and grid validation | 11 independent unit tests; full notebook |
| 4 | Fourth-order Richardson derivative; derivation, cancellation, and four-sample cost | 15 tests; fourth-order fit on exp/sin; full notebook |
| 5 | Composite midpoint rule; analytical error constant and benchmark comparison | 20 tests; smooth-function bounds; full notebook |
| 6 | Matched sampled-value costs and tested tolerance budgets | 23 tests; instrumented sample counts; full notebook |
| 7 | Analytical noise weights and 20,000-draw Monte Carlo validation | 26 tests; standard-deviation ratios within 5%; full notebook |
| 8 | Log domain boundaries and sqrt endpoint singularity | 30 tests; measured convergence near 1.5 for trapezoids/midpoints |
| 9 | Isolated artifact verifier and cross-version GitHub Actions | 34 tests; 14 code cells; seven figures; eleven CSVs; passing Python 3.12/3.14 CI |
| 10 | Final English report synthesis, quantitative summary, reproducibility and rubric mapping | Final unit tests, isolated rerun, artifact review, privacy scan, and final CI |

The final CI status and the actual immutable commit history can be inspected in GitHub. Source and results are committed together. The host environment may print a macOS process-inspection warning while a local kernel shuts down; this did not fail any cell, and independent Linux CI checks run without that host restriction.

The examiner retains discretion over which commits are meaningful. The work record does not assert that a student has already reviewed the report or that the exam was submitted. Public visibility was enabled after the local checks and passing cross-version CI, as authorized by the owner; anonymous repository access was verified.
