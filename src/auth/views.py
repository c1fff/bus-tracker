from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.db import get_db 
from src.auth.services import UserServices
from src.auth.sсhemas import UserCreate, UserRead, UserLogin, AuthToken, RefreshToken, UserChangePassword
from src.auth.dependencies import get_current_user



router = APIRouter(
    tags=["auth"]
)


@router.post("/register", response_model=UserRead)
async def register_user(user_data: UserCreate, db: AsyncSession=Depends(get_db)):
    services = UserServices(db)
    return await services.register(user_data)



@router.post("/login", response_model=AuthToken)
async def login_user(user_data: UserLogin, db: AsyncSession=Depends(get_db)):
    services = UserServices(db)
    return await services.login(user_data)


@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return current_user


@router.post("/change_password", response_model=UserRead)
async def change_user_password(user: UserChangePassword, current_user = Depends(get_current_user), db : AsyncSession=Depends(get_db)):
    services = UserServices(db)
    return await services.change_user_pass(current_user, user.old_password, user.new_password)


@router.post("/refresh", response_model=AuthToken)
async def check_refresh_token(refresh_token : RefreshToken, db : AsyncSession=Depends(get_db)):
    services = UserServices(db)
    return await services.update_user_refresh_token(refresh_token.token)

