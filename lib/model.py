"""Core forecasting and quantile estimation model for Twitch launch CCU."""

import math
import statistics
from typing import Any

LEVELS = [0.05, 0.25, 0.5, 0.75, 0.95]
Z = [-1.645, -0.674, 0.0, 0.674, 1.645]

# Prior diurnal log-normal ratios derived from empirical console rolling launches
DEFAULT_RATIOS = [
    1.000, 0.887, 0.756, 0.735, 0.794, 0.914, 0.952, 0.942, 0.898, 0.925,
    0.928, 0.978, 1.059, 1.181, 1.360, 1.489, 1.569, 1.636, 1.912, 2.132,
    2.246, 2.165, 2.017, 1.746
]

DEFAULT_SPREADS = [
    0.000, 0.150, 0.270, 0.299, 0.300, 0.467, 0.639, 0.723, 0.709, 0.785,
    0.803, 0.786, 0.798, 0.716, 0.785, 0.784, 0.720, 0.648, 0.636, 0.714,
    0.837, 0.848, 0.812, 0.719
]


def round2(x: float) -> float | int:
    """Round to 2 decimal places half-up matching JavaScript Math.round."""
    scaled = x * 100
    whole = math.floor(scaled)
    if scaled - whole >= 0.5:
        whole += 1
    val = whole / 100
    return int(val) if val.is_integer() else val


def extract_comparable_stats(case: dict[str, Any]) -> tuple[list[float], list[float]]:
    """Extract fitted ratios and spreads from comparables in the case.
    
    Robustly computes log-normal empirical median ratios and spreads
    across historical launch days.
    """
    comparables = case.get("comparables", [])
    log_ratios_by_hour: list[list[float]] = [[] for _ in range(24)]

    for comp in comparables:
        day_start = comp.get("day_start")
        if not day_start:
            continue
        prefix = day_start[:10]
        hourly = comp.get("hourly", [])
        day_hours = [h for h in hourly if h.get("from", "").startswith(prefix)]
        if len(day_hours) >= 24:
            p1 = day_hours[0].get("viewers", 0)
            if p1 >= 500:
                unlock = comp.get("unlock", "").lower()
                weight = 1
                if "rolling" in unlock or "midnight" in unlock:
                    weight += 2
                for h_idx in range(24):
                    v = max(1, day_hours[h_idx].get("viewers", 1))
                    lr = math.log(v / p1)
                    for _ in range(weight):
                        log_ratios_by_hour[h_idx].append(lr)

    ratios = list(DEFAULT_RATIOS)
    spreads = list(DEFAULT_SPREADS)

    for h in range(1, 24):
        sample = log_ratios_by_hour[h]
        if len(sample) >= 5:
            med_lr = statistics.median(sample)
            mads = statistics.median([abs(x - med_lr) for x in sample]) * 1.4826
            base_spread = 0.15 * math.sqrt(h)
            spread = max(base_spread, min(1.2, mads))
            ratios[h] = math.exp(med_lr)
            spreads[h] = spread

    return ratios, spreads
