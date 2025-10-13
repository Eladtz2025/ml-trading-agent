"""Synthetic action implementations to back the Phoenix dashboard controls."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, Iterable, Mapping

import csv
import json

import numpy as np

from .action_registry import ActionContext, ActionRegistry, ActionResult
from .spec import iter_components

Metadata = Dict[str, object]

_NOTE_METADATA: Metadata = {
    "disclaimer": "Synthetic demonstration payload generated for dashboard wiring."
}


def _seed(component_id: str) -> int:
    return abs(hash(component_id)) % (2**32)


def _build_series(component_id: str, *, steps: int = 48, scale: float = 0.8) -> list[dict[str, object]]:
    rng = np.random.default_rng(_seed(component_id))
    base = datetime.utcnow() - timedelta(hours=steps)
    value = rng.normal(loc=0.0, scale=scale)
    series: list[dict[str, object]] = []
    for index in range(steps):
        value += rng.normal(scale=scale / 2)
        point_time = base + timedelta(minutes=30 * index)
        series.append(
            {
                "timestamp": point_time.isoformat(timespec="minutes"),
                "value": round(float(value), 6),
            }
        )
    return series


def _chart_action(context: ActionContext, component: Mapping[str, object]) -> ActionResult:
    series = _build_series(context.component_id)
    path = context.write_json({
        "component": context.component_id,
        "series": series,
    })
    artifacts = [ActionContext.relative_path(path)]
    title = component.get("title", context.component_id.replace("_", " "))
    message = f"Synthesised chart payload for {title}."
    return ActionResult(context.component_id, "ok", message, artifacts, metadata=_NOTE_METADATA.copy())


def _distribution_action(context: ActionContext, component: Mapping[str, object]) -> ActionResult:
    rng = np.random.default_rng(_seed(context.component_id))
    buckets = np.linspace(-3, 3, num=13)
    histogram = rng.integers(low=5, high=60, size=len(buckets))
    payload = {
        "component": context.component_id,
        "buckets": [round(float(value), 4) for value in buckets],
        "frequencies": histogram.tolist(),
    }
    path = context.write_json(payload)
    artifacts = [ActionContext.relative_path(path)]
    title = component.get("title", context.component_id)
    message = f"Refreshed distribution sample for {title}."
    return ActionResult(context.component_id, "ok", message, artifacts, metadata=_NOTE_METADATA.copy())


def _stat_action(context: ActionContext, component: Mapping[str, object]) -> ActionResult:
    rng = np.random.default_rng(_seed(context.component_id))
    metrics = {
        "mean": round(float(rng.normal(loc=0.0, scale=1.0)), 4),
        "stdev": round(float(rng.uniform(0.1, 2.0)), 4),
        "min": round(float(rng.uniform(-2.0, 0.0)), 4),
        "max": round(float(rng.uniform(0.0, 2.0)), 4),
    }
    path = context.write_json({"component": context.component_id, "metrics": metrics})
    artifacts = [ActionContext.relative_path(path)]
    title = component.get("title", context.component_id)
    message = f"Recorded metric snapshot for {title}."
    return ActionResult(context.component_id, "ok", message, artifacts, metadata=_NOTE_METADATA.copy())


def _table_action(context: ActionContext, component: Mapping[str, object]) -> ActionResult:
    rng = np.random.default_rng(_seed(context.component_id))
    columns = ["label", "value", "confidence"]
    rows = [
        {
            "label": f"item_{idx+1}",
            "value": round(float(rng.normal()), 5),
            "confidence": round(float(rng.uniform(0.5, 0.99)), 4),
        }
        for idx in range(8)
    ]
    path = context.artifact_path(extension="csv")
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    artifacts = [ActionContext.relative_path(path)]
    title = component.get("title", context.component_id)
    message = f"Exported table payload for {title}."
    return ActionResult(context.component_id, "ok", message, artifacts, metadata=_NOTE_METADATA.copy())


def _timeline_action(context: ActionContext, component: Mapping[str, object]) -> ActionResult:
    rng = np.random.default_rng(_seed(context.component_id))
    base = datetime.utcnow() - timedelta(hours=12)
    events = []
    for idx in range(6):
        event_time = base + timedelta(minutes=int(rng.integers(15, 180)) * idx)
        events.append(
            {
                "timestamp": event_time.isoformat(timespec="minutes"),
                "event": f"event_{idx+1}",
                "severity": rng.choice(["low", "medium", "high"]),
            }
        )
    path = context.write_json({"component": context.component_id, "events": events})
    artifacts = [ActionContext.relative_path(path)]
    title = component.get("title", context.component_id)
    message = f"Captured timeline events for {title}."
    return ActionResult(context.component_id, "ok", message, artifacts, metadata=_NOTE_METADATA.copy())


def _text_action(context: ActionContext, component: Mapping[str, object]) -> ActionResult:
    title = component.get("title", context.component_id)
    lines = [
        f"# {title}",
        "",  # blank line
        "> Synthetic snapshot generated for dashboard instrumentation.",
        "",
        json.dumps({"component": context.component_id, "generated_at": datetime.utcnow().isoformat(timespec="seconds")}, indent=2),
    ]
    content = "\n".join(lines)
    path = context.write_text(content, extension="md")
    artifacts = [ActionContext.relative_path(path)]
    message = f"Materialised markdown snapshot for {title}."
    return ActionResult(context.component_id, "ok", message, artifacts, metadata=_NOTE_METADATA.copy())


def _control_action(context: ActionContext, component: Mapping[str, object]) -> ActionResult:
    title = component.get("title", context.component_id)
    payload = {
        "component": context.component_id,
        "requested_at": datetime.utcnow().isoformat(timespec="seconds"),
        "payload": context.payload,
    }
    path = context.write_json(payload)
    artifacts = [ActionContext.relative_path(path)]
    message = f"Recorded control trigger for {title}."
    return ActionResult(context.component_id, "ok", message, artifacts, metadata=_NOTE_METADATA.copy())


_KIND_TO_HANDLER: Dict[str, Callable[[ActionContext, Mapping[str, object]], ActionResult]] = {
    "chart": _chart_action,
    "distribution": _distribution_action,
    "stat": _stat_action,
    "gauge": _stat_action,
    "table": _table_action,
    "timeline": _timeline_action,
    "text": _text_action,
    "control": _control_action,
}


def build_default_registry(*, root: Path | None = None) -> ActionRegistry:
    """Create an :class:`ActionRegistry` populated for every dashboard component."""

    registry = ActionRegistry(root=root)
    components = iter_components()

    for component_id, component in components.items():
        if component.get("cta", {}).get("type") == "vercel":
            # Dashboard handles this as an external link.
            continue

        kind = component.get("kind")
        handler = _KIND_TO_HANDLER.get(str(kind))
        if handler is None:
            raise ValueError(f"Unsupported component kind '{kind}' for {component_id}")

        registry.register(component_id, lambda ctx, comp=component, fn=handler: fn(ctx, comp))

    return registry
