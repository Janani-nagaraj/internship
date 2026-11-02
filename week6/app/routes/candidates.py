from fastapi import APIRouter, Depends, HTTPException, Response

import app.db.candidates as store
from app.core.security import require_admin
from app.schemas.candidate import CandidateCreate, CandidateOut, CandidateUpdate
from app.services.validation import clean_candidate_id

router = APIRouter(prefix="/candidates", tags=["Candidates (CRUD)"])


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


@router.put("/{candidate_id}", response_model=CandidateOut)
def update_candidate(candidate_id: str, body: CandidateUpdate, user=Depends(require_admin)):
    candidate_id = clean_candidate_id(candidate_id)
    try:
        updated = store.update_candidate(candidate_id, body.full_name, body.email, body.status)
    except Exception as exc:
        raise _db_error(exc)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")
    return updated


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
