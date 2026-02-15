from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from uuid import UUID

from src.config import settings
from src.exceptions import InvalidTokenException, TokenExpiredException

def create_access_token(user_id: UUID, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
    )
    to_encode = {"sub": str(user_id), "exp": expire, "token_type": "access", "role": role}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRES_DAYS
    )
    to_encode = {"sub": str(user_id), "exp": expire, "token_type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str, expected_token_type: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_type = payload.get("token_type")
        
        if token_type != expected_token_type:
            raise InvalidTokenException("Invalid token type")
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException("Token expired")
    except JWTError:
        raise InvalidTokenException("Invalid token")