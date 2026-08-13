# services/pipeline/extraction_agent.py
import json
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ValidationError
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile
from app.services.agent.llm_client import generate_text

EXTRACTION_SYSTEM_PROMPT = """You extract structured career information from
resumes. Respond with ONLY valid JSON, no other text:
{"current_role": str or null, "field": str, "region": str,
 "skills": [str, ...], "years_experience": number or null}"""


class ExtractedFields(BaseModel):
    current_role: Optional[str] = None
    field: str
    region: str
    skills: list[str]
    years_experience: Optional[float] = None


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_structured_fields(raw_text: str) -> ExtractedFields:
    response = generate_text(prompt=raw_text, system=EXTRACTION_SYSTEM_PROMPT)
    try:
        return ExtractedFields.model_validate(json.loads(response))
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"LLM extraction did not return valid structured data: {e}")


def run_extraction(
    session: Session, user_id: UUID, file_path: str, source_filename: str
) -> UserProfile:
    raw_text = extract_text_from_pdf(file_path)
    fields = extract_structured_fields(raw_text)

    profile = UserProfile(
        user_id=user_id,
        source_filename=source_filename,
        raw_text=raw_text,
        current_role=fields.current_role,
        field=fields.field,
        region=fields.region,
        skills=fields.skills,
        years_experience=fields.years_experience,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile