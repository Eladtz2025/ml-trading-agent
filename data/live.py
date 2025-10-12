"""Live data ingestion helpers with synthetic stream tag support."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Mapping

import pandas as pd


@dataclass
class StreamTag:
    """Represents a logical stream and its associated metadata."""

    name: str
    description: str
    schema: Mapping[str, str]


@dataclass
class LiveIngestionManager:
    """Coordinate ingestion of streaming payloads into append-only stores."""

    root: Path
    tags: Dict[str, StreamTag] = field(default_factory=dict)

    def register_tag(self, tag: StreamTag) -> None:
        if tag.name in self.tags:
            raise ValueError(f"Tag '{tag.name}' already registered")
        self.tags[tag.name] = tag

    def ensure_registered(self, tag_name: str) -> StreamTag:
        try:
            return self.tags[tag_name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"Tag '{tag_name}' is not registered") from exc

    def ingest_records(self, tag_name: str, records: Iterable[Mapping[str, object]]) -> Path:
        """Append streaming records to the parquet log for ``tag_name``."""

        tag = self.ensure_registered(tag_name)
        frame = pd.DataFrame(list(records))
        if frame.empty:
            raise ValueError("No records provided for ingestion")

        missing = set(tag.schema).difference(frame.columns)
        if missing:
            raise KeyError(f"Missing required fields for tag '{tag_name}': {', '.join(sorted(missing))}")

        for column, dtype in tag.schema.items():
            frame[column] = frame[column].astype(dtype)

        frame["ingested_at"] = datetime.utcnow()

        destination = self.root / f"{tag_name}.parquet"
        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.exists():
            existing = pd.read_parquet(destination)
            frame = pd.concat([existing, frame], ignore_index=True)

        frame.to_parquet(destination, index=False)
        return destination

    def load_live_frame(self, tag_name: str) -> pd.DataFrame:
        """Return the accumulated dataframe for ``tag_name``."""

        destination = self.root / f"{tag_name}.parquet"
        if not destination.exists():
            raise FileNotFoundError(f"No data ingested yet for tag '{tag_name}'")
        return pd.read_parquet(destination)
