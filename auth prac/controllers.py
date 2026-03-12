from schema import UserCreateModel, UserResponseModel, APIResponseModel, LoginModel
from utils.password_worker import hash_password, verify_password
from sqlalchemy.orm import Session
from model import User
from fastapi import HTTPException
from uuid import uuid4
from utils.token_handler import create_access_token



async def get_all_users(db: Session):
  users = db.query(User).all()
  return APIResponseModel(
    success=True,
    message="Users fetched successfully",
    data=users
    )
  
async def get_user_by_id(db: Session, user_id: str):
  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return APIResponseModel(
    success=True,
    message="User fetched successfully",
    data=user
    )
  

async def login_user(db: Session, login_data: LoginModel):
    """Authenticate by email/password and return JWT (sign-in)."""
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
    })
    return APIResponseModel(
        success=True,
        message="Login successful",
        data={
            "user": user,
            "access_token": access_token,
        },
    )


async def create_user(db: Session, user_data: UserCreateModel):
    """Signup only (public). Creates user and returns JWT."""
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hassed_password = hash_password(user_data.password)
    new_user_id = str(uuid4())
    new_user = User(
        id=new_user_id,
        name=user_data.name,
        email=user_data.email,
        password=hassed_password,
        role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token({
        "id": new_user_id,
        "email": new_user.email,
        "name": new_user.name,
        "role": new_user.role,
    })
    return APIResponseModel(
        success=True,
        message="User created successfully",
        data={
            "user": new_user,
            "access_token": access_token,
        },
    )
  
async def update_user(db: Session, user_id: str, user_data: UserCreateModel):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    db.commit()
    db.refresh(user)
    return APIResponseModel(
        success=True,
        message="User updated successfully",
        data=user,
    )


async def delete_user(db: Session, user_id: str):
    """Admin only (enforced at route level)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return APIResponseModel(
        success=True,
        message="User deleted successfully",
        data=None,
    )