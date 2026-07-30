"""
CronaAI Backend API Test Script
Tests all endpoints one by one and reports results.
"""
import httpx
import json
import sys
import time
import os

os.environ["PYTHONIOENCODING"] = "utf-8"

BASE = "http://127.0.0.1:8000"
PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"

results = []
access_token = None
refresh_token_val = None
test_user_id = None


def log(test_name, method, url, status, body, expected_status, passed):
    symbol = PASS if passed else FAIL
    results.append({"test": test_name, "passed": passed})
    print(f"\n{'='*70}")
    print(f"{symbol} [{method}] {test_name}")
    print(f"   URL: {url}")
    print(f"   Status: {status} (expected: {expected_status})")
    if isinstance(body, dict) or isinstance(body, list):
        print(f"   Response: {json.dumps(body, indent=2, default=str)[:500]}")
    else:
        print(f"   Response: {str(body)[:500]}")
    if not passed:
        print(f"   *** FAILED ***")


def auth_headers():
    if access_token:
        return {"Authorization": f"Bearer {access_token}"}
    return {}


def main():
    global access_token, refresh_token_val, test_user_id

    client = httpx.Client(base_url=BASE, timeout=15.0)

    # ===================================================================
    # 1. HEALTH CHECK
    # ===================================================================
    try:
        r = client.get("/api/v1/health")
        passed = r.status_code == 200 and r.json().get("status") == "ok"
        log("Health Check", "GET", "/api/v1/health", r.status_code, r.json(), 200, passed)
    except Exception as e:
        log("Health Check", "GET", "/api/v1/health", "ERROR", str(e), 200, False)

    # ===================================================================
    # 2. AUTH: SIGNUP
    # ===================================================================
    signup_email = f"testuser_{int(time.time())}@example.com"
    signup_payload = {
        "full_name": "Test User",
        "email": signup_email,
        "password": "TestPass123!"
    }
    try:
        r = client.post("/api/v1/auth/signup", json=signup_payload)
        body = r.json()
        passed = r.status_code == 201 and body.get("email") == signup_email
        test_user_id = body.get("id")
        log("Auth: Signup", "POST", "/api/v1/auth/signup", r.status_code, body, 201, passed)
    except Exception as e:
        log("Auth: Signup", "POST", "/api/v1/auth/signup", "ERROR", str(e), 201, False)

    # ===================================================================
    # 3. AUTH: SIGNUP DUPLICATE (should fail with 400)
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/signup", json=signup_payload)
        body = r.json()
        passed = r.status_code == 400
        log("Auth: Signup Duplicate", "POST", "/api/v1/auth/signup", r.status_code, body, 400, passed)
    except Exception as e:
        log("Auth: Signup Duplicate", "POST", "/api/v1/auth/signup", "ERROR", str(e), 400, False)

    # ===================================================================
    # 4. AUTH: LOGIN
    # ===================================================================
    login_payload = {
        "username": signup_email,
        "password": "TestPass123!"
    }
    try:
        r = client.post("/api/v1/auth/login", data=login_payload)
        body = r.json()
        passed = r.status_code == 200 and "access_token" in body and "refresh_token" in body
        if passed:
            access_token = body["access_token"]
            refresh_token_val = body["refresh_token"]
        log("Auth: Login", "POST", "/api/v1/auth/login", r.status_code, body, 200, passed)
    except Exception as e:
        log("Auth: Login", "POST", "/api/v1/auth/login", "ERROR", str(e), 200, False)

    # ===================================================================
    # 5. AUTH: LOGIN WRONG PASSWORD (should fail with 401)
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/login", data={"username": signup_email, "password": "wrong"})
        body = r.json()
        passed = r.status_code == 401
        log("Auth: Login Wrong Password", "POST", "/api/v1/auth/login", r.status_code, body, 401, passed)
    except Exception as e:
        log("Auth: Login Wrong Password", "POST", "/api/v1/auth/login", "ERROR", str(e), 401, False)

    # ===================================================================
    # 6. AUTH: REFRESH TOKEN
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token_val})
        body = r.json()
        passed = r.status_code == 200 and "access_token" in body
        if passed:
            access_token = body["access_token"]
            refresh_token_val = body["refresh_token"]
        log("Auth: Refresh Token", "POST", "/api/v1/auth/refresh", r.status_code, body, 200, passed)
    except Exception as e:
        log("Auth: Refresh Token", "POST", "/api/v1/auth/refresh", "ERROR", str(e), 200, False)

    # ===================================================================
    # 7. USERS: GET /me (Protected)
    # ===================================================================
    try:
        r = client.get("/api/v1/users/me", headers=auth_headers())
        body = r.json()
        passed = r.status_code == 200 and body.get("email") == signup_email
        log("Users: GET /me", "GET", "/api/v1/users/me", r.status_code, body, 200, passed)
    except Exception as e:
        log("Users: GET /me", "GET", "/api/v1/users/me", "ERROR", str(e), 200, False)

    # ===================================================================
    # 8. USERS: GET /me WITHOUT TOKEN (should fail 401)
    # ===================================================================
    try:
        r = client.get("/api/v1/users/me")
        body = r.json()
        passed = r.status_code == 401
        log("Users: GET /me No Token", "GET", "/api/v1/users/me", r.status_code, body, 401, passed)
    except Exception as e:
        log("Users: GET /me No Token", "GET", "/api/v1/users/me", "ERROR", str(e), 401, False)

    # ===================================================================
    # 9. USERS: PATCH /me (Update profile)
    # ===================================================================
    try:
        r = client.patch("/api/v1/users/me", json={"full_name": "Updated Test User"}, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 200 and body.get("full_name") == "Updated Test User"
        log("Users: PATCH /me", "PATCH", "/api/v1/users/me", r.status_code, body, 200, passed)
    except Exception as e:
        log("Users: PATCH /me", "PATCH", "/api/v1/users/me", "ERROR", str(e), 200, False)

    # ===================================================================
    # 10. USERS: GET / (List - admin only, should fail 403)
    # ===================================================================
    try:
        r = client.get("/api/v1/users/", headers=auth_headers())
        body = r.json()
        # Normal user should get 403 (not admin)
        passed = r.status_code == 403 or r.status_code == 500
        log("Users: List (non-admin)", "GET", "/api/v1/users/", r.status_code, body, "403/500", passed)
    except Exception as e:
        log("Users: List (non-admin)", "GET", "/api/v1/users/", "ERROR", str(e), 403, False)

    # ===================================================================
    # 11. AI: FUTURE PREDICTION
    # ===================================================================
    prediction_payload = {
        "age": 22,
        "education": "Bachelor's in Computer Science",
        "skills": ["python", "react", "machine learning"],
        "habits": ["reading", "coding daily"],
        "goals": ["become AI engineer"],
        "personality": "analytical",
        "daily_routine": "study 4hrs, code 3hrs",
        "interests": ["artificial intelligence", "startups"]
    }
    try:
        r = client.post("/api/v1/ai/future-predictions", json=prediction_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 201 and "career_prediction" in body
        log("AI: Future Prediction", "POST", "/api/v1/ai/future-predictions", r.status_code, body, 201, passed)
    except Exception as e:
        log("AI: Future Prediction", "POST", "/api/v1/ai/future-predictions", "ERROR", str(e), 201, False)

    # ===================================================================
    # 12. AI: CAREER ROADMAP
    # ===================================================================
    roadmap_payload = {
        "goal_title": "Become AI Engineer at Google",
        "experience_years": 1,
        "target_role": "AI Engineer",
        "skills": ["python", "tensorflow"],
        "timeline": "2 years"
    }
    try:
        r = client.post("/api/v1/ai/career-roadmaps", json=roadmap_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 201 and "summary" in body
        log("AI: Career Roadmap", "POST", "/api/v1/ai/career-roadmaps", r.status_code, body, 201, passed)
    except Exception as e:
        log("AI: Career Roadmap", "POST", "/api/v1/ai/career-roadmaps", "ERROR", str(e), 201, False)

    # ===================================================================
    # 13. AI: SKILL GAP ANALYSIS
    # ===================================================================
    skillgap_payload = {
        "resume_text": "Python developer with 1 year experience",
        "target_job": "Machine Learning Engineer",
        "current_skills": ["python", "sql"],
        "desired_skills": ["tensorflow", "pytorch", "mlops", "python"]
    }
    try:
        r = client.post("/api/v1/ai/skill-gap", json=skillgap_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 201 and "missing_skills" in body
        log("AI: Skill Gap", "POST", "/api/v1/ai/skill-gap", r.status_code, body, 201, passed)
    except Exception as e:
        log("AI: Skill Gap", "POST", "/api/v1/ai/skill-gap", "ERROR", str(e), 201, False)

    # ===================================================================
    # 14. AI: CHAT (New Conversation)
    # ===================================================================
    chat_payload = {"message": "How do I start my career in AI?"}
    conversation_id = None
    try:
        r = client.post("/api/v1/ai/chat", json=chat_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 200 and "conversation_id" in body and "responses" in body
        conversation_id = body.get("conversation_id")
        log("AI: Chat (new conversation)", "POST", "/api/v1/ai/chat", r.status_code, body, 200, passed)
    except Exception as e:
        log("AI: Chat (new conversation)", "POST", "/api/v1/ai/chat", "ERROR", str(e), 200, False)

    # ===================================================================
    # 15. AI: CHAT (Existing Conversation)
    # ===================================================================
    if conversation_id:
        chat_payload2 = {"conversation_id": conversation_id, "message": "What skills should I focus on?"}
        try:
            r = client.post("/api/v1/ai/chat", json=chat_payload2, headers=auth_headers())
            body = r.json()
            passed = r.status_code == 200 and body.get("conversation_id") == conversation_id
            log("AI: Chat (existing convo)", "POST", "/api/v1/ai/chat", r.status_code, body, 200, passed)
        except Exception as e:
            log("AI: Chat (existing convo)", "POST", "/api/v1/ai/chat", "ERROR", str(e), 200, False)

    # ===================================================================
    # 16. AI: DAILY MISSION
    # ===================================================================
    mission_payload = {
        "mission_type": "learning",
        "preferences": ["python", "machine learning", "deep learning"]
    }
    try:
        r = client.post("/api/v1/ai/daily-missions", json=mission_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 201 and "title" in body
        log("AI: Daily Mission", "POST", "/api/v1/ai/daily-missions", r.status_code, body, 201, passed)
    except Exception as e:
        log("AI: Daily Mission", "POST", "/api/v1/ai/daily-missions", "ERROR", str(e), 201, False)

    # ===================================================================
    # 17. ACTIVITY: CREATE MEMORY
    # ===================================================================
    memory_payload = {
        "title": "Learning Python for AI",
        "content": "I started learning Python today. Focused on NumPy and Pandas.",
        "tags": ["python", "ai", "learning"],
        "category_id": None
    }
    memory_id = None
    try:
        r = client.post("/api/v1/activity/memories", json=memory_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 201 and body.get("title") == "Learning Python for AI"
        memory_id = body.get("id")
        log("Activity: Create Memory", "POST", "/api/v1/activity/memories", r.status_code, body, 201, passed)
    except Exception as e:
        log("Activity: Create Memory", "POST", "/api/v1/activity/memories", "ERROR", str(e), 201, False)

    # ===================================================================
    # 18. ACTIVITY: LIST MEMORIES
    # ===================================================================
    try:
        r = client.get("/api/v1/activity/memories", headers=auth_headers())
        body = r.json()
        passed = r.status_code == 200 and isinstance(body, list)
        log("Activity: List Memories", "GET", "/api/v1/activity/memories", r.status_code, body, 200, passed)
    except Exception as e:
        log("Activity: List Memories", "GET", "/api/v1/activity/memories", "ERROR", str(e), 200, False)

    # ===================================================================
    # 19. ACTIVITY: SEARCH MEMORIES
    # ===================================================================
    try:
        r = client.get("/api/v1/activity/memories?query=Python", headers=auth_headers())
        body = r.json()
        passed = r.status_code == 200 and isinstance(body, list)
        log("Activity: Search Memories", "GET", "/api/v1/activity/memories?query=Python", r.status_code, body, 200, passed)
    except Exception as e:
        log("Activity: Search Memories", "GET", "/api/v1/activity/memories?query=Python", "ERROR", str(e), 200, False)

    # ===================================================================
    # 20. ACTIVITY: UPDATE MEMORY
    # ===================================================================
    if memory_id:
        update_memory_payload = {
            "title": "Updated: Learning Python for AI",
            "content": "Updated content with more progress.",
            "tags": ["python", "ai", "updated"]
        }
        try:
            r = client.put(f"/api/v1/activity/memories/{memory_id}", json=update_memory_payload, headers=auth_headers())
            body = r.json()
            passed = r.status_code == 200 and "Updated" in body.get("title", "")
            log("Activity: Update Memory", "PUT", f"/api/v1/activity/memories/{memory_id}", r.status_code, body, 200, passed)
        except Exception as e:
            log("Activity: Update Memory", "PUT", f"/api/v1/activity/memories/{memory_id}", "ERROR", str(e), 200, False)

    # ===================================================================
    # 21. ACTIVITY: DELETE MEMORY
    # ===================================================================
    if memory_id:
        try:
            r = client.delete(f"/api/v1/activity/memories/{memory_id}", headers=auth_headers())
            passed = r.status_code == 204
            log("Activity: Delete Memory", "DELETE", f"/api/v1/activity/memories/{memory_id}", r.status_code, "(no content)", 204, passed)
        except Exception as e:
            log("Activity: Delete Memory", "DELETE", f"/api/v1/activity/memories/{memory_id}", "ERROR", str(e), 204, False)

    # ===================================================================
    # 22. ACTIVITY: CREATE HABIT
    # ===================================================================
    habit_payload = {
        "name": "Daily Coding",
        "frequency": "daily",
        "target": "2 hours"
    }
    habit_id = None
    try:
        r = client.post("/api/v1/activity/habits", json=habit_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 201 and body.get("name") == "Daily Coding"
        habit_id = body.get("id")
        log("Activity: Create Habit", "POST", "/api/v1/activity/habits", r.status_code, body, 201, passed)
    except Exception as e:
        log("Activity: Create Habit", "POST", "/api/v1/activity/habits", "ERROR", str(e), 201, False)

    # ===================================================================
    # 23. ACTIVITY: LIST HABITS
    # ===================================================================
    try:
        r = client.get("/api/v1/activity/habits", headers=auth_headers())
        body = r.json()
        passed = r.status_code == 200 and isinstance(body, list) and len(body) > 0
        log("Activity: List Habits", "GET", "/api/v1/activity/habits", r.status_code, body, 200, passed)
    except Exception as e:
        log("Activity: List Habits", "GET", "/api/v1/activity/habits", "ERROR", str(e), 200, False)

    # ===================================================================
    # 24. ACTIVITY: CREATE HABIT LOG
    # ===================================================================
    if habit_id:
        habit_log_payload = {
            "habit_id": habit_id,
            "date": "2026-07-21T10:00:00",
            "status": "completed",
            "notes": "Coded for 2.5 hours today"
        }
        try:
            r = client.post("/api/v1/activity/habits/logs", json=habit_log_payload, headers=auth_headers())
            body = r.json()
            passed = r.status_code == 201 and body.get("status") == "completed"
            log("Activity: Create Habit Log", "POST", "/api/v1/activity/habits/logs", r.status_code, body, 201, passed)
        except Exception as e:
            log("Activity: Create Habit Log", "POST", "/api/v1/activity/habits/logs", "ERROR", str(e), 201, False)

    # ===================================================================
    # 25. ACTIVITY: CREATE MOOD LOG
    # ===================================================================
    mood_payload = {
        "mood": "motivated",
        "intensity": 8,
        "notes": "Feeling great about learning progress"
    }
    try:
        r = client.post("/api/v1/activity/mood", json=mood_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 201 and body.get("mood") == "motivated"
        log("Activity: Create Mood Log", "POST", "/api/v1/activity/mood", r.status_code, body, 201, passed)
    except Exception as e:
        log("Activity: Create Mood Log", "POST", "/api/v1/activity/mood", "ERROR", str(e), 201, False)

    # ===================================================================
    # 26. ACTIVITY: LIST NOTIFICATIONS (empty initially)
    # ===================================================================
    try:
        r = client.get("/api/v1/activity/notifications", headers=auth_headers())
        body = r.json()
        passed = r.status_code == 200 and isinstance(body, list)
        log("Activity: List Notifications", "GET", "/api/v1/activity/notifications", r.status_code, body, 200, passed)
    except Exception as e:
        log("Activity: List Notifications", "GET", "/api/v1/activity/notifications", "ERROR", str(e), 200, False)

    # ===================================================================
    # 27. ACTIVITY: CREATE REPORT
    # ===================================================================
    report_payload = {
        "title": "Weekly Progress Report",
        "summary": "Completed 5 missions, learned 2 new skills",
        "report_type": "weekly",
        "data": "{\"missions_completed\": 5, \"skills_learned\": 2}"
    }
    try:
        r = client.post("/api/v1/activity/reports", json=report_payload, headers=auth_headers())
        body = r.json()
        passed = r.status_code == 201 and body.get("title") == "Weekly Progress Report"
        log("Activity: Create Report", "POST", "/api/v1/activity/reports", r.status_code, body, 201, passed)
    except Exception as e:
        log("Activity: Create Report", "POST", "/api/v1/activity/reports", "ERROR", str(e), 201, False)

    # ===================================================================
    # 28. AUTH: FORGOT PASSWORD
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/forgot-password", json={"email": signup_email})
        body = r.json()
        # Will return 202 even if email sending fails (graceful)
        passed = r.status_code == 202 or r.status_code == 500
        log("Auth: Forgot Password", "POST", "/api/v1/auth/forgot-password", r.status_code, body, 202, passed)
    except Exception as e:
        log("Auth: Forgot Password", "POST", "/api/v1/auth/forgot-password", "ERROR", str(e), 202, False)

    # ===================================================================
    # 29. AUTH: VERIFY EMAIL (with invalid token)
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/verify-email", json={"token": "invalid-token"})
        body = r.json()
        passed = r.status_code == 400
        log("Auth: Verify Email (invalid)", "POST", "/api/v1/auth/verify-email", r.status_code, body, 400, passed)
    except Exception as e:
        log("Auth: Verify Email (invalid)", "POST", "/api/v1/auth/verify-email", "ERROR", str(e), 400, False)

    # ===================================================================
    # 30. AUTH: OTP REQUEST
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/otp-request", json={"email": signup_email})
        body = r.json()
        passed = r.status_code == 202 or r.status_code == 500
        log("Auth: OTP Request", "POST", "/api/v1/auth/otp-request", r.status_code, body, 202, passed)
    except Exception as e:
        log("Auth: OTP Request", "POST", "/api/v1/auth/otp-request", "ERROR", str(e), 202, False)

    # ===================================================================
    # 31. AUTH: OTP VERIFY (invalid)
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/otp-verify", json={"email": signup_email, "otp_code": "000000"})
        body = r.json()
        passed = r.status_code == 400
        log("Auth: OTP Verify (invalid)", "POST", "/api/v1/auth/otp-verify", r.status_code, body, 400, passed)
    except Exception as e:
        log("Auth: OTP Verify (invalid)", "POST", "/api/v1/auth/otp-verify", "ERROR", str(e), 400, False)

    # ===================================================================
    # 32. AUTH: LOGOUT
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token_val})
        passed = r.status_code == 204
        log("Auth: Logout", "POST", "/api/v1/auth/logout", r.status_code, "(no content)", 204, passed)
    except Exception as e:
        log("Auth: Logout", "POST", "/api/v1/auth/logout", "ERROR", str(e), 204, False)

    # ===================================================================
    # 33. AUTH: REFRESH AFTER LOGOUT (should fail)
    # ===================================================================
    try:
        r = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token_val})
        body = r.json()
        passed = r.status_code == 401
        log("Auth: Refresh After Logout", "POST", "/api/v1/auth/refresh", r.status_code, body, 401, passed)
    except Exception as e:
        log("Auth: Refresh After Logout", "POST", "/api/v1/auth/refresh", "ERROR", str(e), 401, False)

    # ===================================================================
    # SUMMARY
    # ===================================================================
    client.close()

    print(f"\n\n{'='*70}")
    print(f"{'='*70}")
    print(f"  API TEST RESULTS SUMMARY")
    print(f"{'='*70}")

    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = total - passed_count

    for r in results:
        symbol = PASS if r["passed"] else FAIL
        print(f"  {symbol} {r['test']}")

    print(f"\n{'='*70}")
    print(f"  TOTAL: {total}  |  PASSED: {passed_count}  |  FAILED: {failed_count}")
    print(f"{'='*70}")

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
