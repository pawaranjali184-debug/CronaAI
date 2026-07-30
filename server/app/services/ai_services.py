import logging
from datetime import datetime

from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from groq import Groq
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.career import CareerRoadmap
from app.models.chat import Message
from app.models.daily_mission import DailyMission, MissionHistory
from app.models.future_prediction import FuturePrediction
from app.models.skill import SkillGapReport
from app.schemas.ai import (
    CareerRoadmapRequest,
    DailyMissionRequest,
    FuturePredictionRequest,
    SkillGapRequest,
)

# Initialize Groq Client
client = Groq(api_key=settings.GROQ_API_KEY)
logger = logging.getLogger(__name__)


def generate_future_prediction(data: FuturePredictionRequest) -> dict:
    career = (
        f"Based on your background, a strong future path is to pursue "
        f"{data.interests[0]} and develop skills in {', '.join(data.skills)}."
    )

    salary = (
        f"Estimated salary range: "
        f"${50_000 + len(data.skills) * 5000:,} - "
        f"${80_000 + len(data.skills) * 7000:,}"
    )

    probability = round(min(0.95, 0.45 + len(data.skills) * 0.05), 2)

    recommendations = (
        "Focus on consistent learning, build small projects, "
        "join communities, and track progress weekly."
    )

    return {
        "career_prediction": career,
        "salary_estimate": salary,
        "success_probability": probability,
        "recommendations": recommendations,
    }


async def generate_career_roadmap(data: CareerRoadmapRequest) -> dict:
    """
    Generate a personalized career roadmap using Groq AI.
    """

    try:
        prompt = f"""
Create a personalized career roadmap.

Goal Title:
{data.goal_title}

Target Role:
{data.target_role}

Timeline:
{data.timeline}

Generate:

1. A concise roadmap summary.
2. Recommended learning resources.
3. Important skills to learn.
4. Suggested projects.
5. Certifications (if applicable).
6. Interview preparation tips.

Return the response in this exact format:

Summary:
...

Resources:
...

"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Crona AI.

You are an expert Career Mentor.

Generate personalized career roadmaps that are practical,
realistic, and easy to follow.
""",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.5,
            max_tokens=1000,
        )

        response = completion.choices[0].message.content.strip()

        summary = response
        resources = ""

        if "Resources:" in response:
            parts = response.split("Resources:", 1)
            summary = parts[0].replace("Summary:", "").strip()
            resources = parts[1].strip()

        return {
            "summary": summary,
            "timeline": data.timeline,
            "resources": resources,
        }

    except Exception as e:
        print("Groq Roadmap Error:", e)

        return {
            "summary": f"Roadmap to become a {data.target_role}.",
            "timeline": data.timeline,
            "resources": "Unable to generate AI roadmap at this time.",
        }


def generate_skill_gap(data: SkillGapRequest) -> dict:
    missing = [
        skill
        for skill in data.desired_skills
        if skill not in data.current_skills
    ]

    if not missing:
        missing = ["communication", "problem solving"]

    order = ", ".join(missing)
    readiness = round(max(0.1, 1.0 - len(missing) * 0.15), 2)

    return {
        "missing_skills": ", ".join(missing),
        "priority_order": order,
        "readiness_score": readiness,
    }


async def create_prediction(
    db: AsyncSession,
    user_id: int,
    request: FuturePredictionRequest,
) -> FuturePrediction:

    generated = generate_future_prediction(request)

    prediction = FuturePrediction(
        user_id=user_id,
        input_data=request.model_dump_json(),
        career_prediction=generated["career_prediction"],
        salary_estimate=generated["salary_estimate"],
        success_probability=generated["success_probability"],
        recommendations=generated["recommendations"],
    )

    db.add(prediction)
    await db.commit()
    await db.refresh(prediction)

    return prediction


async def create_roadmap(
    db: AsyncSession,
    user_id: int,
    request: CareerRoadmapRequest,
) -> CareerRoadmap:

    generated = await generate_career_roadmap(request)

    roadmap = CareerRoadmap(
        user_id=user_id,
        goal_title=request.goal_title,
        summary=generated["summary"],
        timeline=generated["timeline"],
        resources=generated["resources"],
    )

    db.add(roadmap)
    await db.commit()
    await db.refresh(roadmap)

    return roadmap


async def create_skill_gap(
    db: AsyncSession,
    user_id: int,
    request: SkillGapRequest,
) -> SkillGapReport:

    generated = generate_skill_gap(request)

    report = SkillGapReport(
        user_id=user_id,
        target_job=request.target_job,
        missing_skills=generated["missing_skills"],
        priority_order=generated["priority_order"],
        readiness_score=generated["readiness_score"],
    )

    db.add(report)
    await db.commit()
    await db.refresh(report)

    return report


# ============================
# GROQ CHATBOT
# ============================

async def generate_chat_response(message: str) -> str:
    """
    Generate an AI response using the Groq API.
    """

    if not message or not message.strip():
        return "Please enter a message."

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Crona AI.

You are an intelligent AI Career Mentor.

Your responsibilities include helping users with:

• Career guidance
• Career planning
• Future career prediction
• Skill gap analysis
• Personalized learning roadmaps
• Resume improvement
• Interview preparation
• Programming
• Artificial Intelligence
• Machine Learning
• Software Development
• Project ideas
• Higher education guidance
• Motivation

Guidelines:

- Be professional.
- Give practical advice.
- Prefer bullet points whenever useful.
- Explain concepts simply.
- If asked unrelated questions, answer politely.
- Keep responses concise unless the user requests detailed explanations.
""",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("Groq API Error:", e)
        return (
            "Sorry, I couldn't generate a response right now. "
            "Please try again later."
        )


async def create_chat_message(
    db: AsyncSession,
    conversation_id: int,
    sender: str,
    content: str,
) -> Message:

    message = Message(
        conversation_id=conversation_id,
        sender=sender,
        content=content,
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)
    logger.info(f"Chat message saved: id={message.id}, conversation={conversation_id}, sender={sender}")

    return message


async def create_daily_mission(
    db: AsyncSession,
    user_id: int,
    request: DailyMissionRequest,
) -> DailyMission:

    title = f"{request.mission_type.title()} mission"

    description = (
        f"A mission focused on "
        f"{', '.join(request.preferences[:3])}."
    )

    mission = DailyMission(
        user_id=user_id,
        mission_type=request.mission_type,
        title=title,
        description=description,
        status="pending",
    )

    db.add(mission)
    await db.commit()
    await db.refresh(mission)

    # Also create a MissionHistory record
    history = MissionHistory(
        mission_id=mission.id,
        notes=f"Mission created: {title}",
    )
    db.add(history)
    await db.commit()
    logger.info(f"Created daily mission id={mission.id} with history for user={user_id}")

    return mission