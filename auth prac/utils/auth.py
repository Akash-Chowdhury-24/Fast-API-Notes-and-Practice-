"""
Auth dependencies: Bearer token extraction (manual) and role-based checks.
Frontend sends: Authorization: Bearer <jwt_token>
"""
from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel

from .token_handler import decode_access_token


class TokenPayload(BaseModel):
    id: str
    email: str
    name: str
    role: str


def get_current_user(request: Request) -> TokenPayload:

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header[len("Bearer "):].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return TokenPayload(
            id=payload["id"],
            email=payload["email"],
            name=payload["name"],
            role=payload["role"],
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_admin(current_user: TokenPayload = Depends(get_current_user)) -> TokenPayload:

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return current_user


def require_self_or_admin(
    user_id: str,
    current_user: TokenPayload = Depends(get_current_user),
) -> TokenPayload:

    if current_user.role == "admin" or current_user.id == user_id:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not allowed to perform this action for this user",
    )
