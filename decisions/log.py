"""Utility for logging architectural and ML decisions with PR traceability."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Mapping


@dataclass
class DecisionRecord:
    identifier: str
    title: str
    pr_number: int
    summary: str
    owners: list[str]
    metadata: Mapping[str, str]
    created_at: str = datetime.utcnow().isoformat(timespec="seconds")


class DecisionLogger:
    def __init__(self, destination: str | Path) -> None:
        self.destination = Path(destination)
        self.destination.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: DecisionRecord) -> Path:
        payload = asdict(record)
        payload["created_at"] = datetime.utcnow().isoformat(timespec="seconds")

        if self.destination.exists():
            existing = json.loads(self.destination.read_text(encoding="utf-8"))
        else:
            existing = []

        existing.append(payload)
        self.destination.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        return self.destination
