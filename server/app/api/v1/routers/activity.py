from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies.auth import require_active_user
from app.schemas.activity import (
    FutureMemoryRequest,
    FutureMemoryResponse,
    HabitRequest,
    HabitResponse,
    HabitLogRequest,
    HabitLogResponse,
    MoodLogRequest,
    MoodLogResponse,
    NotificationResponse,
    ReportRequest,
    ReportResponse,
    DashboardStatsResponse,
)
from app.services.activity_services import (
    create_memory,
    list_memories,
    update_memory,
    delete_memory,
    create_habit,
    list_habits,
    create_habit_log,
    create_mood_log,
    list_notifications,
    mark_notification_read,
    create_report,
    get_dashboard_stats,
)
from app.models.future_memory import FutureMemory
from app.models.notification import Notification
from app.models.report import Report
from app.models.user import User

router = APIRouter()


@router.get("/dashboard-stats", response_model=DashboardStatsResponse)
async def dashboard_stats(current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> DashboardStatsResponse:
    stats = await get_dashboard_stats(db, current_user.id)
    return DashboardStatsResponse(**stats)


@router.post("/memories", response_model=FutureMemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_future_memory(payload: FutureMemoryRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> FutureMemoryResponse:
    memory = await create_memory(db, current_user.id, payload.title, payload.content, payload.tags, payload.category_id)
    return memory


@router.get("/memories", response_model=list[FutureMemoryResponse])
async def get_memories(query: str | None = Query(None), current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> list[FutureMemoryResponse]:
    return await list_memories(db, current_user.id, query)


@router.put("/memories/{memory_id}", response_model=FutureMemoryResponse)
async def update_future_memory(memory_id: int, payload: FutureMemoryRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> FutureMemoryResponse:
    result = await db.execute(select(FutureMemory).where(FutureMemory.id == memory_id, FutureMemory.user_id == current_user.id, FutureMemory.is_deleted == False))
    memory = result.scalars().first()
    if not memory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    return await update_memory(db, memory, payload.title, payload.content, payload.tags)


@router.delete("/memories/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_future_memory(memory_id: int, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> None:
    result = await db.execute(select(FutureMemory).where(FutureMemory.id == memory_id, FutureMemory.user_id == current_user.id, FutureMemory.is_deleted == False))
    memory = result.scalars().first()
    if not memory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    await delete_memory(db, memory)


@router.post("/habits", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
async def create_habit_item(payload: HabitRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> HabitResponse:
    return await create_habit(db, current_user.id, payload.name, payload.frequency, payload.target)


@router.get("/habits", response_model=list[HabitResponse])
async def get_habits(current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> list[HabitResponse]:
    return await list_habits(db, current_user.id)


@router.post("/habits/logs", response_model=HabitLogResponse, status_code=status.HTTP_201_CREATED)
async def create_habit_log_item(payload: HabitLogRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> HabitLogResponse:
    return await create_habit_log(db, payload.habit_id, payload.date, payload.status, payload.notes)


@router.post("/mood", response_model=MoodLogResponse, status_code=status.HTTP_201_CREATED)
async def create_mood_entry(payload: MoodLogRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> MoodLogResponse:
    return await create_mood_log(db, current_user.id, payload.mood, payload.intensity, payload.notes)


@router.get("/notifications", response_model=list[NotificationResponse])
async def get_user_notifications(current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> list[NotificationResponse]:
    return await list_notifications(db, current_user.id)


@router.post("/notifications/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification(notification_id: int, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> NotificationResponse:
    result = await db.execute(select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id, Notification.is_deleted == False))
    notification = result.scalars().first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return await mark_notification_read(db, notification)


@router.post("/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_user_report(payload: ReportRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> ReportResponse:
    return await create_report(db, current_user.id, payload.title, payload.summary, payload.report_type, payload.data)
