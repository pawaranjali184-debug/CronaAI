from datetime import datetime, date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.future_memory import FutureMemory
from app.models.daily_mission import DailyMission
from app.models.habit import Habit, HabitLog
from app.models.mood import MoodLog
from app.models.notification import Notification
from app.models.report import Report
from app.models.future_prediction import FuturePrediction


async def create_memory(db: AsyncSession, user_id: int, title: str, content: str, tags: list[str], category_id: int | None) -> FutureMemory:
    memory = FutureMemory(
        user_id=user_id,
        title=title,
        content=content,
        tags=", ".join(tags) if tags else None,
        category_id=category_id,
        summary=None,
    )
    db.add(memory)
    await db.commit()
    await db.refresh(memory)
    return memory


async def list_memories(db: AsyncSession, user_id: int, query: str | None = None) -> list[FutureMemory]:
    statement = select(FutureMemory).where(FutureMemory.user_id == user_id, FutureMemory.is_deleted == False)
    if query:
        statement = statement.where(FutureMemory.title.ilike(f"%{query}%") | FutureMemory.content.ilike(f"%{query}%"))
    result = await db.execute(statement)
    return result.scalars().all()


async def update_memory(db: AsyncSession, memory: FutureMemory, title: str | None, content: str | None, tags: list[str] | None) -> FutureMemory:
    if title is not None:
        memory.title = title
    if content is not None:
        memory.content = content
    if tags is not None:
        memory.tags = ", ".join(tags)
    db.add(memory)
    await db.commit()
    await db.refresh(memory)
    return memory


async def delete_memory(db: AsyncSession, memory: FutureMemory) -> None:
    memory.is_deleted = True
    db.add(memory)
    await db.commit()


async def create_habit(db: AsyncSession, user_id: int, name: str, frequency: str | None, target: str | None) -> Habit:
    habit = Habit(user_id=user_id, name=name, frequency=frequency, target=target)
    db.add(habit)
    await db.commit()
    await db.refresh(habit)
    return habit


async def list_habits(db: AsyncSession, user_id: int) -> list[Habit]:
    result = await db.execute(select(Habit).where(Habit.user_id == user_id, Habit.is_deleted == False))
    return result.scalars().all()


async def create_habit_log(db: AsyncSession, habit_id: int, date: datetime, status: str, notes: str | None) -> HabitLog:
    log = HabitLog(habit_id=habit_id, date=date, status=status, notes=notes)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


async def create_mood_log(db: AsyncSession, user_id: int, mood: str, intensity: int | None, notes: str | None) -> MoodLog:
    mood_log = MoodLog(user_id=user_id, mood=mood, intensity=intensity, notes=notes)
    db.add(mood_log)
    await db.commit()
    await db.refresh(mood_log)
    return mood_log


async def list_notifications(db: AsyncSession, user_id: int) -> list[Notification]:
    result = await db.execute(select(Notification).where(Notification.user_id == user_id, Notification.is_deleted == False))
    return result.scalars().all()


async def mark_notification_read(db: AsyncSession, notification: Notification) -> Notification:
    notification.read = "true"
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def create_report(db: AsyncSession, user_id: int, title: str, summary: str, report_type: str, data: str | None) -> Report:
    report = Report(user_id=user_id, title=title, summary=summary, report_type=report_type, data=data)
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


async def get_dashboard_stats(db: AsyncSession, user_id: int) -> dict:
    """Fetch aggregated dashboard stats for the current user."""

    # Active missions count
    missions_result = await db.execute(
        select(func.count(DailyMission.id)).where(
            DailyMission.user_id == user_id,
            DailyMission.status == "pending",
            DailyMission.is_deleted == False,
        )
    )
    active_missions = missions_result.scalar() or 0

    # Habits tracked count
    habits_result = await db.execute(
        select(func.count(Habit.id)).where(
            Habit.user_id == user_id,
            Habit.is_deleted == False,
        )
    )
    habits_tracked = habits_result.scalar() or 0

    # Mood today — latest mood entry for today
    today_start = datetime.combine(date.today(), datetime.min.time())
    mood_result = await db.execute(
        select(MoodLog.mood)
        .where(
            MoodLog.user_id == user_id,
            MoodLog.logged_at >= today_start,
        )
        .order_by(MoodLog.logged_at.desc())
        .limit(1)
    )
    mood_today = mood_result.scalar() or "—"

    # Predictions count
    predictions_result = await db.execute(
        select(func.count(FuturePrediction.id)).where(
            FuturePrediction.user_id == user_id,
            FuturePrediction.is_deleted == False,
        )
    )
    predictions_count = predictions_result.scalar() or 0

    return {
        "active_missions": active_missions,
        "habits_tracked": habits_tracked,
        "mood_today": mood_today,
        "predictions_count": predictions_count,
    }
