from datetime import datetime
from pydantic import BaseModel


from pydantic import Field


class FutureMemoryRequest(BaseModel):
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    category_id: int | None = None


class FutureMemoryResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: str | None
    summary: str | None

    category_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class HabitRequest(BaseModel):
    name: str
    frequency: str | None = None
    target: str | None = None


class HabitResponse(BaseModel):
    id: int
    name: str
    frequency: str | None
    target: str | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class HabitLogRequest(BaseModel):
    habit_id: int
    date: datetime
    status: str = "completed"
    notes: str | None = None


class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    date: datetime
    status: str
    notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class MoodLogRequest(BaseModel):
    mood: str
    intensity: int | None = None
    notes: str | None = None


class MoodLogResponse(BaseModel):
    id: int
    mood: str
    intensity: int | None
    notes: str | None
    logged_at: datetime

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    id: int
    title: str
    content: str | None
    priority: str
    read: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReportRequest(BaseModel):
    title: str
    summary: str
    report_type: str
    data: str | None = None


class ReportResponse(BaseModel):
    id: int
    title: str
    summary: str
    report_type: str
    data: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStatsResponse(BaseModel):
    active_missions: int
    habits_tracked: int
    mood_today: str
    predictions_count: int
