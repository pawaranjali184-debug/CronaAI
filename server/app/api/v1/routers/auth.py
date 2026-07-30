from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import SignupRequest, LoginRequest, RefreshRequest, PasswordResetRequest, PasswordResetConfirm, VerifyEmailRequest, OTPRequest, OTPVerifyRequest, LogoutRequest
from app.schemas.user import UserResponse, TokenResponse
from app.services.auth_services import create_user, authenticate_user, create_tokens, refresh_tokens, revoke_refresh_token, create_otp_for_user, verify_otp, verify_email_token, get_user_by_email
from app.services.email_service import send_email
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.utils.security import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupRequest, db: AsyncSession = Depends(get_db)) -> UserResponse:
    user = await create_user(db, payload)
    try:
        send_email(
            subject="Verify your CronaAI account",
            recipient=user.email,
            content=f"Please verify your account by using this token: {user.email_verification_token}",
        )
    except Exception as e:
        print("Email sending failed:", e)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:

    payload = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    user = await authenticate_user(db, payload)
    tokens = await create_tokens(db, user)

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    tokens = await refresh_tokens(db, payload.refresh_token)
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: LogoutRequest, db: AsyncSession = Depends(get_db)) -> None:
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == payload.refresh_token, RefreshToken.revoked == None)
    )
    token_record = result.scalars().first()
    if token_record:
        await revoke_refresh_token(db, token_record)


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(payload: PasswordResetRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    user = await get_user_by_email(db, payload.email)
    if user:
        reset_token = f"reset-{user.id}-{int(datetime.utcnow().timestamp())}"
        user.reset_token = reset_token
        await db.commit()
        send_email(
            subject="Reset your CronaAI password",
            recipient=user.email,
            content=f"Use this token to reset your password: {reset_token}",
        )
    return {"message": "If the email is registered, a password reset link has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(payload: PasswordResetConfirm, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    result = await db.execute(select(User).where(User.reset_token == payload.token, User.is_deleted == False))
    user = result.scalars().first()
    if not user:
        return {"message": "Invalid or expired reset token."}
    user.password_hash = hash_password(payload.new_password)
    user.reset_token = None
    await db.commit()
    return {"message": "Password reset successful."}


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(payload: VerifyEmailRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    user = await verify_email_token(db, payload.token)
    return {"message": "Email verified successfully.", "user_id": user.id}


@router.post("/otp-request", status_code=status.HTTP_202_ACCEPTED)
async def request_otp(payload: OTPRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    user = await get_user_by_email(db, payload.email)
    if not user:
        return {"message": "If the email is registered, an OTP has been sent."}
    otp_code = f"{datetime.utcnow().timestamp():.0f}"[-6:]
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    await create_otp_for_user(db, user, otp_code, expires_at)
    send_email(
        subject="Your CronaAI verification OTP",
        recipient=user.email,
        content=f"Your OTP code is {otp_code}. It expires in 10 minutes.",
    )
    return {"message": "If the email is registered, an OTP has been sent."}


@router.post("/otp-verify", status_code=status.HTTP_200_OK)
async def otp_verify(payload: OTPVerifyRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    user = await verify_otp(db, payload.email, payload.otp_code)
    return {"message": "OTP verified successfully.", "user_id": user.id}
