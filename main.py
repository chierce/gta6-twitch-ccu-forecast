"""GTA VI Launch-Day Twitch CCU Quantile Forecaster.

Standard library only, Node/Python offline sandbox compliant.
"""

import json
import math
import os
import sys
from pathlib import Path

# Ensure local lib directory is on sys.path even when grader passes -P
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.model import LEVELS, Z, extract_comparable_stats, round2

INPUT_DIR = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def forecast_case(case: dict[str, any], name: str) -> dict[str, any]:
    if case.get("levels") != LEVELS:
        raise ValueError(f"{name} asks for unexpected levels {case.get('levels')}")

    first = next((k for k in case.get("known", []) if k.get("hour") == 1), None)
    if first is None:
        raise ValueError(f"{name} has no hour-1 print")

    p1 = max(1, first.get("viewers", 1))
    ratios, spreads = extract_comparable_stats(case)

    hours_output = []
    for row in case.get("forecast", []):
        h = row["hour"]
        idx = h - 1
        r = ratios[idx]
        s = spreads[idx]

        q = [round2(p1 * r * math.exp(z * s)) for z in Z]

        # Enforce strict quantile ordering q05 <= q25 <= q50 <= q75 <= q95
        for i in range(1, len(q)):
            if q[i] < q[i - 1]:
                q[i] = q[i - 1]

        hours_output.append({"hour": h, "q": q})

    return {"hours": hours_output}


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(INPUT_DIR.glob("*.in")):
        case = json.loads(path.read_text(encoding="utf-8"))
        forecast = forecast_case(case, path.name)
        out_file = OUTPUT_DIR / f"{path.stem}.out"
        out_file.write_text(json.dumps(forecast, separators=(",", ":")) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
