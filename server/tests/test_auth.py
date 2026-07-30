import asyncio
import pytest
from httpx import AsyncClient
from fastapi import status
from main import app


@pytest.mark.asyncio
async def test_signup_and_login(tmp_path):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        signup_payload = {"full_name": "Test User", "email": "test@example.com", "password": "Pass1234"}
        response = await client.post("/api/v1/auth/signup", json=signup_payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == "test@example.com"

        login_payload = {"email": "test@example.com", "password": "Pass1234"}
        response = await client.post("/api/v1/auth/login", json=login_payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
