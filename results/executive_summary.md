## Quantitative findings

### Lowest tested sampled-value budgets for exp on [0,1]

| Target absolute error | Method | Sampled values | Actual error |
|---:|---|---:|---:|
| 1e-03 | Left | 1024 | 8.389e-04 |
| 1e-03 | Trapezoid | 16 | 6.364e-04 |
| 1e-03 | Midpoint | 16 | 2.796e-04 |
| 1e-05 | Left | not reached | not reached |
| 1e-05 | Trapezoid | 128 | 8.878e-06 |
| 1e-05 | Midpoint | 128 | 4.370e-06 |
| 1e-07 | Left | not reached | not reached |
| 1e-07 | Trapezoid | 2048 | 3.417e-08 |
| 1e-07 | Midpoint | 1024 | 6.828e-08 |

Targets are checked against the analytical result; unreached targets are censored at the tested maximum budget.

### Endpoint singularity

- sqrt(x), Left: fitted order 1.006.
- sqrt(x), Trapezoid: fitted order 1.497.
- sqrt(x), Midpoint: fitted order 1.495.

Maximum Monte Carlo standard-deviation ratio deviation from the independent-noise model: 1.16%.
