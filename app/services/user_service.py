from jose import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def create_user(email: str, password: str, db: AsyncSession):
    user = User(email=email, hashed_password=get_password_hash(password))
    db.add(user)
    await db.commit()

    return {"message": "User created successfully"}

async def authenticate_user(email: str, password: str, db: AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()

    if user and verify_password(password, user.hashed_password):
        return user

    return None

async def get_current_user(token: str, db: AsyncSession) -> User:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    email: str = payload.get("sub")

    query = select(User).where(User.email == email)

    result = db.execute(query)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user