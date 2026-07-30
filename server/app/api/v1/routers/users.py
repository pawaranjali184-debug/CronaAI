from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies.auth import require_active_user, require_admin
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_services import get_user_by_id, list_users, update_user
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(require_active_user)) -> UserResponse:
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_profile(payload: UserUpdate, current_user: User = Depends(require_active_user), db: AsyncSession = Depends(get_db)) -> UserResponse:
    return await update_user(db, current_user, payload)


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(skip: int = 0, limit: int = 50, _admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    return await list_users(db, skip=skip, limit=limit)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, _admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)) -> None:
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await update_user(db, user, UserUpdate(full_name=user.full_name))
    user.is_deleted = True
    db.add(user)
    await db.commit()
