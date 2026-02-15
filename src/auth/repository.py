from src.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UserRepository:
    
    def __init__(self, db : AsyncSession):
        self.db = db


    async def get_user_by_mail(self, user_email : str) -> User | None:
        stmt = select(User).where(User.email == user_email)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    

    async def create_user_db(self, **fields) -> User:
        user = User(**fields)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

    async def update_user_refresh_token(self, user : User, refresh_token_hash : str) -> User:
        user.refresh_token_hash = refresh_token_hash
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

    async def update_user_password_db(self, user : User, new_password_hash : str) -> User:
        user.password_hash = new_password_hash
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

    async def get_user_by_id(self, user_id : str) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()



