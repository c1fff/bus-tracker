from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends



from src.auth.repository import UserRepository
from src.auth.sсhemas import UserCreate, UserLogin, AuthToken
from src.utils.security import get_password_hash, verify_password
from src.utils.jwt import create_access_token, create_refresh_token, decode_token
from src.exceptions import InvalidTokenException, TokenExpiredException
from src.auth.dependencies import get_current_user

def require_driver(user: dict):
    if user["role"] != "driver":
        raise HTTPException(403, "Only drivers can send location")
    return user