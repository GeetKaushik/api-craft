# Reads the bearer token from the request's Authorization header.
# Validates its signature and expiration.
# Extracts the user ID from the token.
# Fetches that user from SQL Server.
# Rejects invalid tokens and inactive accounts.
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.database.dependencies import get_session
from app.database.models import User
from app.services.auth_service import decode_access_token


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> User:
    # Verify the JWT signature and expiry.
    try:
        payload = decode_access_token(credentials.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract the user ID from the token.
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Find the account associated with the token.
    try:
        user = session.get(User, int(user_id))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or account inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
