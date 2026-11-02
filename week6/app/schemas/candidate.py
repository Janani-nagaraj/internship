import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

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
