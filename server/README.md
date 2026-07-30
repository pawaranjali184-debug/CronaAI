# CronaAI Backend Server

A development-ready Python backend for the CronaAI platform using FastAPI, MySQL, and SQLAlchemy.

## Setup

1. Copy `.env.example` to `.env` and configure your MySQL connection.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Create the MySQL database:

```sql
CREATE DATABASE cronaai_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. Run the server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API

The API is available at `http://127.0.0.1:8000`.
Swagger docs: `http://127.0.0.1:8000/docs`

## Testing

```bash
pytest
```

## Features

- JWT authentication with access and refresh tokens
- Signup, login, logout, refresh, password reset, email verification, OTP verification
- Future prediction, career roadmap, skill gap analysis, AI chat assistant, daily missions
- Memory store, achievements, habits, moods, notifications, reports
- Simple local file uploads for avatar and resume
- Basic email sending for development
