import json
from pydantic import BaseModel, ValidationError
from app.models.user_profile import UserProfile
from app.services.agent.llm_client import generate_text
PLANNER_SYSTEM_PROMPT = """Given a professional profile, list up to 5 concrete
search queries worth researching about this person's market position — their
current role, adjacent roles, and related skills. Respond with ONLY valid
JSON: {"queries": [str, ...]}"""
class ResearchPlan(BaseModel):
    queries: list[str]
def build_research_plan(profile: UserProfile) -> ResearchPlan:
    prompt = (
        f"Current role: {profile.current_role}\n"
        f"Field: {profile.field}\n"
        f"Region: {profile.region}\n"
        f"Skills: {', '.join(profile.skills)}\n"
        f"Years of experience: {profile.years_experience}"
    )
    response = generate_text(prompt=prompt, system=PLANNER_SYSTEM_PROMPT)
    try:
        return ResearchPlan.model_validate(json.loads(response))
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Planner did not return valid structured data: {e}")