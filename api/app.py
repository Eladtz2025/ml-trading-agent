"""FastAPI application exposing dashboard action endpoints."""

from __future__ import annotations

import logging
from typing import Any, Mapping

from fastapi import FastAPI, HTTPException

from dashboard import RegistryError, build_default_registry

logger = logging.getLogger(__name__)

app = FastAPI()
registry = build_default_registry()


@app.get("/")
def root() -> Mapping[str, str]:
    return {"status": "OK"}


@app.post("/actions/{component_id}")
def trigger_action(component_id: str) -> Mapping[str, Any]:
    try:
        result = registry.run(component_id)
    except RegistryError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        logger.exception("Unhandled error while running dashboard action", exc_info=exc)
        raise HTTPException(status_code=500, detail="Failed to execute action") from exc

    return result.to_dict()
