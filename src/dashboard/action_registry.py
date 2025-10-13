"""Registry and execution helpers for dashboard-triggered actions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Iterable, Mapping, MutableMapping

import json

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ACTION_ROOT = REPO_ROOT / "reports" / "dashboard_actions"


class RegistryError(RuntimeError):
    """Raised when dashboard actions cannot be registered or executed."""


@dataclass(slots=True)
class ActionContext:
    """Holds execution context for a dashboard-triggered action."""

    component_id: str
    root: Path = field(default_factory=lambda: DEFAULT_ACTION_ROOT)
    payload: Mapping[str, object] = field(default_factory=dict)
    started_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def artifact_directory(self) -> Path:
        destination = self.root / self.component_id
        destination.mkdir(parents=True, exist_ok=True)
        return destination

    def artifact_path(self, *, extension: str = "json") -> Path:
        timestamp = self.started_at.strftime("%Y%m%dT%H%M%SZ")
        filename = f"{timestamp}.{extension}"
        return self.artifact_directory() / filename

    def write_json(self, data: Mapping[str, object] | Iterable[object]) -> Path:
        path = self.artifact_path(extension="json")
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, default=str)
        return path

    def write_text(self, content: str, *, extension: str = "md") -> Path:
        path = self.artifact_path(extension=extension)
        path.write_text(content, encoding="utf-8")
        return path

    @staticmethod
    def relative_path(path: Path) -> str:
        try:
            return str(path.relative_to(REPO_ROOT))
        except ValueError:  # pragma: no cover - defensive fallback
            return str(path)


@dataclass(slots=True)
class ActionResult:
    """Represents the outcome of an action execution."""

    component_id: str
    status: str
    message: str
    artifacts: list[str] = field(default_factory=list)
    metadata: MutableMapping[str, object] | None = None

    def to_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "component_id": self.component_id,
            "status": self.status,
            "message": self.message,
            "artifacts": self.artifacts,
        }
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


ActionHandler = Callable[[ActionContext], ActionResult]


class ActionRegistry:
    """Registers and executes dashboard-triggered actions."""

    def __init__(self, *, root: Path | None = None) -> None:
        self.root = root or DEFAULT_ACTION_ROOT
        self.root.mkdir(parents=True, exist_ok=True)
        self._handlers: Dict[str, ActionHandler] = {}

    def register(self, component_id: str, handler: ActionHandler) -> None:
        if component_id in self._handlers:
            raise RegistryError(f"Action for component '{component_id}' already registered")
        self._handlers[component_id] = handler

    def register_many(self, mapping: Mapping[str, ActionHandler]) -> None:
        for component_id, handler in mapping.items():
            self.register(component_id, handler)

    def get_handler(self, component_id: str) -> ActionHandler:
        try:
            return self._handlers[component_id]
        except KeyError as exc:
            raise RegistryError(f"Component '{component_id}' has no registered action") from exc

    def run(self, component_id: str, payload: Mapping[str, object] | None = None) -> ActionResult:
        handler = self.get_handler(component_id)
        context = ActionContext(component_id=component_id, root=self.root, payload=payload or {})
        result = handler(context)

        if result.component_id != component_id:
            raise RegistryError(
                f"Action for '{component_id}' returned result for '{result.component_id}'"
            )

        self._log_execution(result, context)
        return result

    def _log_execution(self, result: ActionResult, context: ActionContext) -> None:
        log_dir = self.root / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        entry = {
            "component_id": result.component_id,
            "status": result.status,
            "message": result.message,
            "artifacts": result.artifacts,
            "started_at": context.started_at.isoformat(timespec="seconds"),
            "logged_at": datetime.utcnow().isoformat(timespec="seconds"),
        }

        log_path = log_dir / "action_log.jsonl"
        with log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(entry) + "\n")

    def list_components(self) -> list[str]:
        return sorted(self._handlers)

    def __contains__(self, component_id: str) -> bool:
        return component_id in self._handlers
