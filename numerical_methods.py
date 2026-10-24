"""Uniform-grid numerical calculus for finite real scalar data.

Derivative callables accept scalar floats. Integration callables must accept
NumPy arrays (scalar constants are broadcast). No analytical derivatives or
library quadrature algorithms are used internally.
"""
from collections.abc import Callable
import numpy as np


def _finite_scalar(value, name):
    array = np.asarray(value)
    if array.ndim != 0 or array.dtype.kind not in "biuf":
        raise ValueError(f"{name} must be a finite real scalar")
    try:
        result = float(array)
    except (OverflowError, ValueError) as error:
        raise ValueError(f"{name} must be a finite real scalar") from error
    if not np.isfinite(result):
        raise ValueError(f"{name} must be a finite real scalar")
    return result


def _step(point, step, symmetric=False):
    point = _finite_scalar(point, "point")
    step = _finite_scalar(step, "step")
    if step <= 0:
        raise ValueError("step must be positive")
    nodes = [point + step]
    if symmetric:
        nodes.append(point - step)
    if any(not np.isfinite(node) or node == point for node in nodes):
        raise ValueError("step produces an indistinguishable or non-finite sample")
    return point, step


def _scalar_sample(function, point):
    with np.errstate(all="ignore"):
        return _finite_scalar(function(point), "function value")


def forward_difference(function: Callable, point: float, step: float) -> float:
    """First-order difference using f(point) and f(point+step)."""
    point, step = _step(point, step)
    return _finite_scalar(
        (_scalar_sample(function, point + step) - _scalar_sample(function, point)) / step,
        "derivative estimate",
    )


def central_difference(function: Callable, point: float, step: float) -> float:
    """Second-order symmetric difference using two sampled values."""
    point, step = _step(point, step, symmetric=True)
    return _finite_scalar(
        (_scalar_sample(function, point + step) - _scalar_sample(function, point - step)) / (2 * step),
        "derivative estimate",
    )


def _grid(a, b, intervals):
    a, b = _finite_scalar(a, "a"), _finite_scalar(b, "b")
    if isinstance(intervals, (bool, np.bool_)) or not isinstance(intervals, (int, np.integer)) or intervals < 1:
        raise ValueError("intervals must be a positive integer")
    h = (b - a) / intervals
    if not np.isfinite(h) or (a != b and h == 0):
        raise ValueError("grid width must be finite and representable")
    return a, b, int(intervals), h


def _sample_values(function, nodes):
    with np.errstate(all="ignore"):
        values = np.asarray(function(nodes))
    if values.dtype.kind not in "biuf":
        raise ValueError("function samples must be real numeric values")
    try:
        values = np.broadcast_to(values.astype(float), nodes.shape)
    except ValueError as error:
        raise ValueError("function values must match the sampling grid") from error
    if not np.all(np.isfinite(values)):
        raise ValueError("function returned non-finite samples")
    return values


def _check_nodes(nodes):
    if not np.all(np.isfinite(nodes)) or np.any(np.diff(nodes) == 0):
        raise ValueError("sampling grid contains non-finite or indistinguishable nodes")


def left_rectangle(function: Callable, a: float, b: float, intervals: int) -> float:
    """Sum heights at traversal starts; reversed bounds reverse grid direction.

    At equal bounds return zero without evaluating the function. For reversed
    bounds this is a right-endpoint rule on the corresponding ascending grid.
    """
    a, b, intervals, h = _grid(a, b, intervals)
    if a == b:
        return 0.0
    nodes = a + h * np.arange(intervals)
    _check_nodes(nodes)
    return _finite_scalar(h * np.sum(_sample_values(function, nodes)), "integral estimate")


def trapezoid(function: Callable, a: float, b: float, intervals: int) -> float:
    """Second-order composite trapezoids with intervals+1 endpoint samples."""
    a, b, intervals, h = _grid(a, b, intervals)
    if a == b:
        return 0.0
    nodes = np.linspace(a, b, intervals + 1)
    _check_nodes(nodes)
    values = _sample_values(function, nodes)
    return _finite_scalar(
        h * (0.5 * values[0] + np.sum(values[1:-1]) + 0.5 * values[-1]),
        "integral estimate",
    )
