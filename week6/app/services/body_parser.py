import json

from fastapi import HTTPException, Request
from pydantic import ValidationError

from app.schemas.candidate import CandidateUpdate


async def read_candidate_update(request: Request) -> CandidateUpdate:
    """Read the request body. Only JSON is accepted as input."""
    content_type = request.headers.get("content-type", "").split(";")[0].strip().lower()
    if content_type != "application/json":
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported Content-Type '{content_type or 'none'}'. The request body must be application/json.",
        )

    raw = await request.body()
    if not raw.strip():
        raise HTTPException(status_code=400, detail="The request body is empty.")

    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {exc}")
    if not isinstance(data, dict):
        raise HTTPException(status_code=422, detail="The JSON body must be an object, like {\"full_name\": ...}.")

    try:
        return CandidateUpdate.model_validate(data)
    except ValidationError as exc:
        # same style of error list FastAPI gives for a normal JSON body
        raise HTTPException(status_code=422, detail=json.loads(exc.json(include_url=False)))
