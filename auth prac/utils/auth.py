"""
Auth dependencies: OAuth2 Bearer token extraction and role-based checks.
Frontend sends: Authorization: Bearer <jwt_token>
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from .token_handler import decode_access_token

# Tells FastAPI to read token from header: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=True)


class TokenPayload(BaseModel):
    """Claims we expect inside the JWT (from create_access_token)."""
    id: str
    email: str
    name: str
    role: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    Dependency: extract Bearer token and validate JWT.
    Returns the token payload (current user info); raises 401 if invalid/missing.
    """
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
    """
    Dependency: allow only if the token has role 'admin'.
    Use on routes that are admin-only (e.g. delete user, list all users).
    """
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
    """
    Dependency: allow if current user is admin OR is the same user as user_id.
    Use on routes like PUT /users/{user_id} (update own profile or admin updates anyone).
    Note: use in route as Depends() with user_id coming from path.
    """
    if current_user.role == "admin" or current_user.id == user_id:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not allowed to perform this action for this user",
    )
