import pytest
from httpx import AsyncClient
from fastapi import status
from main import app


@pytest.mark.asyncio
async def test_future_prediction_endpoint():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        payload = {
            "age": 26,
            "education": "Bachelor's degree",
            "skills": ["python", "data analysis"],
            "habits": ["reading", "coding"],
            "goals": ["lead product team"],
            "personality": "analytical",
            "daily_routine": "morning study, evening practice",
            "interests": ["ai", "product"],
        }
        response = await client.post("/api/v1/ai/future-predictions", json=payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
