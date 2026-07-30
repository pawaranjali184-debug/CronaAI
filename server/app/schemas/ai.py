from datetime import datetime
from pydantic import BaseModel
from typing import List


class FuturePredictionRequest(BaseModel):
    age: int
    education: str
    skills: List[str]
    habits: List[str]
    goals: List[str]
    personality: str
    daily_routine: str
    interests: List[str]


class FuturePredictionResponse(BaseModel):
    id: int
    career_prediction: str
    salary_estimate: str | None
    success_probability: float | None
    recommendations: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class CareerRoadmapRequest(BaseModel):
    goal_title: str
    experience_years: int
    target_role: str
    skills: List[str]
    timeline: str


class CareerRoadmapResponse(BaseModel):
    id: int
    goal_title: str
    summary: str
    timeline: str | None
    resources: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class SkillGapRequest(BaseModel):
    resume_text: str
    target_job: str
    current_skills: List[str]
    desired_skills: List[str]


class SkillGapResponse(BaseModel):
    id: int
    missing_skills: str
    priority_order: str
    readiness_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    title: str | None
    message: str
    responses: list[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    title: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class DailyMissionRequest(BaseModel):
    mission_type: str
    preferences: list[str]


class DailyMissionResponse(BaseModel):
    id: int
    mission_type: str
    title: str
    description: str
    scheduled_for: datetime | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
