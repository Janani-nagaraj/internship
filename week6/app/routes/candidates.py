from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool

import app.db.candidates as store
from app.core.security import require_admin
from app.schemas.candidate import CandidateCreate, CandidateOut, CandidateUpdate
from app.services.body_parser import read_candidate_update
from app.services.response_format import build_response, choose_format
from app.services.validation import clean_candidate_id

router = APIRouter(prefix="/candidates", tags=["Candidates (CRUD)"])

# Tells Swagger: the request body is JSON only, the answer can be JSON or XML
PUT_DOCS = {
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": CandidateUpdate.model_json_schema(),
                "example": {"full_name": "Janani Nagaraj", "email": "janani@example.com", "status": "VERIFIED"},
            }
        },
    },
    "responses": {
        "200": {
            "description": "The updated candidate, as JSON or XML (choose with the Accept header or ?format=)",
            "content": {
                "application/json": {"schema": CandidateOut.model_json_schema()},
                "application/xml": {
                    "schema": {"type": "string"},
                    "example": (
                        '<?xml version="1.0" encoding="UTF-8"?>\n'
                        "<candidate><candidate_id>C070</candidate_id><full_name>Janani Nagaraj</full_name>"
                        "<email>janani@example.com</email><status>VERIFIED</status>"
                        "<created_at>2026-11-05T10:15:00+00:00</created_at></candidate>"
                    ),
                },
            },
        }
    },
}


def _db_error(exc):
    return HTTPException(status_code=500, detail=f"Database error: {exc}")


@router.post("", response_model=CandidateOut, status_code=201)
def create_candidate(body: CandidateCreate, user=Depends(require_admin)):
    candidate_id = clean_candidate_id(body.candidate_id)
    try:
        return store.create_candidate(candidate_id, body.full_name, body.email, body.status)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except Exception as exc:
        raise _db_error(exc)


@router.get("", response_model=list[CandidateOut])
def list_candidates(user=Depends(require_admin)):
    try:
        return store.list_candidates()
    except Exception as exc:
        raise _db_error(exc)


@router.get("/{candidate_id}", response_model=CandidateOut)
def read_candidate(candidate_id: str, user=Depends(require_admin)):
    candidate_id = clean_candidate_id(candidate_id)
    try:
        found = store.get_candidate(candidate_id)
    except Exception as exc:
        raise _db_error(exc)
    if found is None:
        raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")
    return found


@router.put("/{candidate_id}", openapi_extra=PUT_DOCS)
async def update_candidate(candidate_id: str, request: Request, user=Depends(require_admin)):
    """Replace a candidate. Input: JSON only. Output: JSON (default) or XML.

    Choose the output with the Accept header (application/json or application/xml)
    or with the query parameter ?format=json or ?format=xml.
    """
    candidate_id = clean_candidate_id(candidate_id)
    choose_format(request)  # reject a bad ?format= or Accept before touching the database
    body = await read_candidate_update(request)
    try:
        updated = await run_in_threadpool(
            store.update_candidate, candidate_id, body.full_name, body.email, body.status
        )
    except Exception as exc:
        raise _db_error(exc)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")
    return build_response(request, updated)


@router.delete("/{candidate_id}", status_code=204)
def delete_candidate(candidate_id: str, user=Depends(require_admin)):
    candidate_id = clean_candidate_id(candidate_id)
    try:
        deleted = store.delete_candidate(candidate_id)
    except Exception as exc:
        raise _db_error(exc)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")
    return Response(status_code=204)
