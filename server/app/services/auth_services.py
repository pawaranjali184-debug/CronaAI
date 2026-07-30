from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, Role
from app.models.refresh_token import RefreshToken
from app.models.otp_verification import OTPVerification
from app.schemas.auth import SignupRequest
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.config import settings

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email, User.is_deleted == False))
    return result.scalars().first()


async def create_role_if_missing(db: AsyncSession, name: str, description: str) -> Role:
    result = await db.execute(select(Role).where(Role.name == name))
    role = result.scalars().first()
    if role:
        return role
    role = Role(name=name, description=description)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


async def create_user(db: AsyncSession, payload: SignupRequest) -> User:
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    default_role = await create_role_if_missing(db, name="User", description="Standard user role")
    verification_token = f"verify-{payload.email}-{int(datetime.utcnow().timestamp())}"
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role_id=default_role.id,
        email_verification_token=verification_token,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def verify_email_token(db: AsyncSession, token: str) -> User:
    result = await db.execute(select(User).where(User.email_verification_token == token, User.is_deleted == False))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification token")
    user.is_verified = True
    user.email_verification_token = None
    db.add(user)
    await db.commit()
    return user


async def authenticate_user(db: AsyncSession, payload: LoginRequest) -> User:
    user = await get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account inactive")
    return user


async def create_tokens(db: AsyncSession, user: User) -> dict[str, str]:
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token_record = RefreshToken(token=refresh_token, user_id=user.id, expires_at=expires_at)
    db.add(token_record)
    await db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> dict[str, str]:
    payload = decode_token(refresh_token)
    if payload.get("scope") != "refresh_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = int(payload["sub"])
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token, RefreshToken.revoked == None))
    token_record = result.scalars().first()
    if token_record is None or token_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    await revoke_refresh_token(db, token_record)
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await create_tokens(db, user)


async def revoke_refresh_token(db: AsyncSession, token_record: RefreshToken) -> None:
    token_record.revoked = datetime.utcnow()
    db.add(token_record)
    await db.commit()


async def create_otp_for_user(db: AsyncSession, user: User, code: str, expires: datetime) -> OTPVerification:
    otp = OTPVerification(user_id=user.id, code=code, expires_at=expires)
    db.add(otp)
    await db.commit()
    await db.refresh(otp)
    return otp


async def verify_otp(db: AsyncSession, email: str, code: str) -> User:
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    result = await db.execute(select(OTPVerification).where(OTPVerification.user_id == user.id, OTPVerification.code == code, OTPVerification.verified == "false"))
    otp = result.scalars().first()
    if not otp or otp.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP invalid or expired")
    otp.verified = "true"
    user.is_verified = True
    db.add_all([otp, user])
    await db.commit()
    return user
