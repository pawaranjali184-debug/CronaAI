from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies.auth import require_active_user
from app.schemas.ai import (
    FuturePredictionRequest,
    FuturePredictionResponse,
    CareerRoadmapRequest,
    CareerRoadmapResponse,
    SkillGapRequest,
    SkillGapResponse,
    ChatRequest,
    ChatResponse,
    ConversationResponse,
    MessageResponse,
    DailyMissionRequest,
    DailyMissionResponse,
)
from app.services.ai_services import (
    create_prediction,
    create_roadmap,
    create_skill_gap,
    generate_chat_response,
    create_chat_message,
    create_daily_mission,
)
from app.models.chat import Conversation, Message
from app.models.daily_mission import DailyMission
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/future-predictions", response_model=FuturePredictionResponse, status_code=status.HTTP_201_CREATED)
async def future_prediction(payload: FuturePredictionRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> FuturePredictionResponse:
    prediction = await create_prediction(db, current_user.id, payload)
    return prediction


@router.post("/career-roadmaps", response_model=CareerRoadmapResponse, status_code=status.HTTP_201_CREATED)
async def career_roadmap(payload: CareerRoadmapRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> CareerRoadmapResponse:
    roadmap = await create_roadmap(db, current_user.id, payload)
    return roadmap


@router.post("/skill-gap", response_model=SkillGapResponse, status_code=status.HTTP_201_CREATED)
async def skill_gap(payload: SkillGapRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> SkillGapResponse:
    report = await create_skill_gap(db, current_user.id, payload)
    return report


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> ChatResponse:
    try:
        conversation = None
        if payload.conversation_id is not None:
            result = await db.execute(select(Conversation).where(Conversation.id == payload.conversation_id, Conversation.user_id == current_user.id, Conversation.is_deleted == False))
            conversation = result.scalars().first()
        if conversation is None:
            title = payload.message[:60] if payload.message else "New conversation"
            conversation = Conversation(user_id=current_user.id, title=title)
            db.add(conversation)
            await db.commit()
            await db.refresh(conversation)
            logger.info(f"Created new conversation id={conversation.id} for user={current_user.id}")

        user_message = await create_chat_message(db, conversation.id, "user", payload.message)
        logger.info(f"Saved user message id={user_message.id} in conversation={conversation.id}")

        assistant_response = await generate_chat_response(payload.message)

        assistant_msg = await create_chat_message(db, conversation.id, "assistant", assistant_response)
        logger.info(f"Saved assistant message id={assistant_msg.id} in conversation={conversation.id}")

        return ChatResponse(conversation_id=conversation.id, title=conversation.title, message=user_message.content, responses=[assistant_response], created_at=user_message.created_at)
    except Exception as e:
        logger.error(f"Chat endpoint error for user={current_user.id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Chat processing failed: {str(e)}")


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> list[ConversationResponse]:
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id, Conversation.is_deleted == False)
        .order_by(Conversation.created_at.desc())
    )
    return result.scalars().all()


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_conversation_messages(conversation_id: int, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> list[MessageResponse]:
    # Verify conversation belongs to user
    convo_result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == current_user.id, Conversation.is_deleted == False)
    )
    conversation = convo_result.scalars().first()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id, Message.is_deleted == False)
        .order_by(Message.created_at.asc())
    )
    return result.scalars().all()


@router.post("/daily-missions", response_model=DailyMissionResponse, status_code=status.HTTP_201_CREATED)
async def daily_mission(payload: DailyMissionRequest, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> DailyMissionResponse:
    mission = await create_daily_mission(db, current_user.id, payload)
    return mission


@router.get("/daily-missions", response_model=list[DailyMissionResponse])
async def list_daily_missions(current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> list[DailyMissionResponse]:
    result = await db.execute(
        select(DailyMission)
        .where(DailyMission.user_id == current_user.id, DailyMission.is_deleted == False)
        .order_by(DailyMission.created_at.desc())
    )
    return result.scalars().all()
