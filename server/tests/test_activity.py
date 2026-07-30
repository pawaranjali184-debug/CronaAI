import pytest
from httpx import AsyncClient
from fastapi import status
from main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "ok"
