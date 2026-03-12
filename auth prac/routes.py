from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from controllers import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    login_user,
)
from schema import (
    UserCreateModel,
    LoginModel,
    APIResponseModel,
    UserResponseModel,
    UserAuthTokenResponseModel
)
from utils.auth import get_current_user, require_admin, require_self_or_admin

router = APIRouter()

# ---------- Public (no auth) ----------

@router.post("/login", response_model=APIResponseModel[UserAuthTokenResponseModel])
async def login_route(login_data: LoginModel, db: Session = Depends(get_db)):
    """Login: email + password → returns JWT. Frontend stores token and sends as Bearer."""
    return await login_user(db, login_data)


@router.post("/users", response_model=APIResponseModel[UserAuthTokenResponseModel], status_code=status.HTTP_201_CREATED)
async def signup_route(user_data: UserCreateModel, db: Session = Depends(get_db)):
    """Signup only (public). Returns user + access_token."""
    return await create_user(db, user_data)


# ---------- Protected: admin only (define before /users/{user_id}) ----------

@router.get("/users", response_model=APIResponseModel[List[UserResponseModel]])
async def get_all_users_route(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return await get_all_users(db)


# ---------- Protected: any authenticated user ----------

@router.get("/users/{user_id}", response_model=APIResponseModel[UserResponseModel])
async def get_user_by_id_route(
    user_id: str,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_user),
):
    return await get_user_by_id(db, user_id)


@router.delete("/users/{user_id}", response_model=APIResponseModel[None])
async def delete_user_route(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Delete user — admin only."""
    return await delete_user(db, user_id)


# ---------- Protected: admin or that specific user only ----------

@router.put("/users/{user_id}", response_model=APIResponseModel[UserResponseModel])
async def update_user_route(
    user_id: str,
    user_data: UserCreateModel,
    db: Session = Depends(get_db),
    current_user=Depends(require_self_or_admin),
):
    """Update user — admin or the user themselves only."""
    return await update_user(db, user_id, user_data)



