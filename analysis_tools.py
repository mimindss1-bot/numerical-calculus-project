"""Small analysis helpers with explicit treatment of invalid or censored data."""
import numpy as np


def observed_order(steps, errors):
    """Fit log(error) against log(step); caller selects the fitting range."""
    steps, errors = np.asarray(steps, dtype=float), np.asarray(errors, dtype=float)
    if (steps.ndim != 1 or errors.shape != steps.shape or steps.size < 2
            or not np.all(np.isfinite(steps)) or not np.all(np.isfinite(errors))
            or np.any(steps <= 0) or np.any(errors <= 0) or np.unique(steps).size < 2):
        raise ValueError("need at least two distinct positive finite steps and positive finite errors")
    return float(np.polyfit(np.log(steps), np.log(errors), 1)[0])


def first_budget_meeting(rows, target):
    """Return the cheapest tested estimate meeting target, or None.

    This searches recorded benchmark data; it is not an adaptive error estimator
    for a new function with an unknown analytical answer.
    """
    if not np.isscalar(target) or not np.isfinite(target) or target <= 0:
        raise ValueError("target must be positive and finite")
    eligible = [row for row in rows if row["absolute_error"] <= target]
    return min(eligible, key=lambda row: row["sampled_values"]) if eligible else None


def noise_standard_deviation(weights, sigma, step):
    """Std of sum(weights_i * independent_noise_i) / step.

    weights are dimensionless; independent sample noise has variance sigma**2.
    This models noise amplification, not truncation bias or reference error.
    """
    weights = np.asarray(weights, dtype=float)
    if weights.ndim != 1 or weights.size == 0 or not np.all(np.isfinite(weights)):
        raise ValueError("weights must be a nonempty finite vector")
    if not np.isfinite(sigma) or sigma < 0 or not np.isfinite(step) or step <= 0:
        raise ValueError("sigma must be nonnegative and step positive, both finite")
    return float(sigma * np.linalg.norm(weights) / step)
