from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.utils.jwt import decode_token

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    token = credentials.credentials
    user_id = decode_token(token=token, expected_token_type="access")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_id