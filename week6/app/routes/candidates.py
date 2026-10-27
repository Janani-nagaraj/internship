import re
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field, field_validator

import candidates_db as store
from auth import require_admin
from utils import clean_candidate_id

router = APIRouter(prefix="/candidates", tags=["Candidates (CRUD)"])

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class CandidateUpdate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100, examples=["Janani Nagaraj"])
    email: str = Field(max_length=150, examples=["janani@example.com"])
    status: Literal["PENDING", "VERIFIED", "REJECTED"] = "PENDING"

    @field_validator("full_name")
    @classmethod
    def strip_name(cls, value):
        return value.strip()

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        value = value.strip()
        if not EMAIL_PATTERN.match(value):
            raise ValueError("Enter a valid email address.")
        return value


class CandidateCreate(CandidateUpdate):
    candidate_id: str = Field(examples=["C001"])


class CandidateOut(BaseModel):
    candidate_id: str
    full_name: str
    email: str
    status: str
    created_at: datetime


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
