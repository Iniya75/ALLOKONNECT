"""
PlannerAgent — Category Rotation

Reads output/category_state.json to get the current category index,
returns the category name, then increments and saves the index.
"""

import json
import os
from pathlib import Path

CATEGORIES = [
    "Gadgets",
    "AI Hub",
    "Finance",
    "World News",
    "Open Source",
    "Space Station",
    "Features",
]

STATE_FILE = (
    Path(__file__).resolve().parent.parent / "output" / "category_state.json"
)


class PlannerAgent:

    def plan(self) -> dict:
        """
        Return the next category to generate and advance the rotation index.
        """
        index = self._read_index()
        category = CATEGORIES[index % len(CATEGORIES)]

        print(f"[PlannerAgent] Category index: {index} -> Category: {category}")

        # Advance to the next index
        self._write_index((index + 1) % len(CATEGORIES))

        return {"topic": category, "category": category}

    # ── helpers ──────────────────────────────────────────────────────────────

    def _read_index(self) -> int:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return int(data.get("index", 0))
            except Exception:
                pass
        return 0

    def _write_index(self, index: int) -> None:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"index": index}, f, indent=4)