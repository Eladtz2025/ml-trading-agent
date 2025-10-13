from __future__ import annotations

from pathlib import Path

from dashboard import build_default_registry
from dashboard.spec import iter_components


def _expected_components() -> set[str]:
    expected = set()
    for component_id, component in iter_components().items():
        cta = component.get("cta", {})
        if isinstance(cta, dict) and cta.get("type") == "vercel":
            continue
        expected.add(component_id)
    return expected


def test_registry_covers_all_components(tmp_path: Path) -> None:
    registry = build_default_registry(root=tmp_path)
    assert set(registry.list_components()) == _expected_components()


def test_action_execution_creates_artifacts(tmp_path: Path) -> None:
    registry = build_default_registry(root=tmp_path)
    component_id = next(iter(_expected_components()))
    result = registry.run(component_id)

    assert result.status == "ok"
    assert result.artifacts, "Action should return at least one artifact"

    for artifact in result.artifacts:
        path = Path(artifact)
        if not path.is_absolute():
            path = Path.cwd() / path
        assert path.exists(), f"Expected artifact {path} to exist"

    log_file = tmp_path / "logs" / "action_log.jsonl"
    assert log_file.exists(), "Execution should be logged"
    assert log_file.read_text(encoding="utf-8").strip(), "Log file should not be empty"
