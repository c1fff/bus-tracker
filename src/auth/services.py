from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from src.auth.repository import UserRepository
from src.auth.sсhemas import UserCreate, UserLogin, AuthToken
from src.utils.security import get_password_hash, verify_password
from src.utils.jwt import create_access_token, create_refresh_token, decode_token
from src.exceptions import InvalidTokenException, TokenExpiredException

class UserServices:

    def __init__(self, db : AsyncSession):
        self.repository = UserRepository(db)



    async def register(self, user_to_create : UserCreate):
        existing = await self.repository.get_user_by_mail(user_to_create.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
        hashed_pass = get_password_hash(user_to_create.password)

        return await self.repository.create_user_db(
            email=user_to_create.email,
            password_hash=hashed_pass,
            phone=user_to_create.phone,
            full_name=user_to_create.full_name,
            role=user_to_create.role,
            is_active=user_to_create.is_active,
        )
    

    async def login(self, user_to_login : UserLogin) -> AuthToken:
        existing = await self.repository.get_user_by_mail(user_to_login.email)
        if not existing:
            raise HTTPException(status_code=400, detail="User doesn't exist")
        verification = verify_password(user_to_login.password, existing.password_hash)
        if not verification:
            raise HTTPException(status_code=400, detail="Wrong password")
        
        user_access_token = create_access_token(existing.id, existing.role)
        user_refresh_token = create_refresh_token(existing.id)

        user_refresh_token_hash = get_password_hash(user_refresh_token)

        await self.repository.update_user_refresh_token(existing, user_refresh_token_hash)

        return AuthToken(
            access_token=user_access_token,
            refresh_token=user_refresh_token
        )
    
    async def change_user_pass(self, user_id : str, old_password : str, new_password : str):
        existing = await self.repository.get_user_by_id(user_id)
        if not existing:
            raise HTTPException(status_code=400, detail="User doesn't exist")
        verification = verify_password(old_password, existing.password_hash)
        if not verification:
            raise HTTPException(status_code=400, detail="Wrong password")
        
        hashed_pass = get_password_hash(new_password)

        result = await self.repository.update_user_password_db(existing, hashed_pass)

        if not result:
            raise HTTPException(status_code=500, detail="Server error")
        
        return result
    
    async def update_user_refresh_token(self, user_refresh_token : str):
        try:
            user_id = decode_token(user_refresh_token, expected_token_type="refresh")
        except TokenExpiredException:
            raise HTTPException(
                status_code=401,
                detail="Refresh token expired"
            )
        except InvalidTokenException:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )
        
        existing = await self.repository.get_user_by_id(user_id)

        if not existing:
            raise HTTPException(status_code=400, detail="User doesn't exist") # register 
        
        verification = verify_password(user_refresh_token, existing.refresh_token_hash)

        if not verification:
            raise HTTPException(status_code=400, detail="Invalid refresh token") # login again

        user_access_token = create_access_token(existing.id, existing.role)
        user_refresh_token = create_refresh_token(existing.id)

        user_refresh_token_hash = get_password_hash(user_refresh_token)

        await self.repository.update_user_refresh_token(existing, user_refresh_token_hash)

        return AuthToken(
            access_token=user_access_token,
            refresh_token=user_refresh_token
        )



        


        
