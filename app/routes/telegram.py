from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_db
from app.services.telegram_service import (
    connect_telegram, complete_login, create_client, get_chats, get_messages
)
from app.services.user_service import get_current_user, oauth2_scheme

router = APIRouter()


async def get_current_user_from_token(token: str, db: AsyncSession):
    try:
        return await get_current_user(token, db)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or user not found")


@router.post("/connect", status_code=status.HTTP_200_OK)
async def send_code(phone: str, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    await get_current_user_from_token(token, db)

    try:
        client = await connect_telegram(phone)

        return {"status": "success", "message": "Code sent to your Telegram account"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to send code: {str(e)}")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(phone: str, code: str, password: str = None, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user = await get_current_user_from_token(token, db)
    client = await connect_telegram(phone)

    try:
        result = await complete_login(client, phone, code, password)

        user.phone = phone
        db.add(user)
        db.commit()
        db.refresh(user)

        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to login: {str(e)}")
    finally:
        await client.disconnect()


@router.get("/chats", status_code=status.HTTP_200_OK)
async def get_all_chats(phone: str, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    await get_current_user_from_token(token, db)
    client = create_client(phone)
    await client.connect()

    try:
        chats = await get_chats(client)

        return {"status": "success", "data": {"chats": chats}}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get chats: {str(e)}")
    finally:
        await client.disconnect()


@router.get("/messages", status_code=status.HTTP_200_OK)
async def get_chat_messages(phone: str, chat_id: int, limit: int = 50, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    await get_current_user_from_token(token, db)
    client = create_client(phone)
    await client.connect()

    try:
        messages = await get_messages(client, chat_id, limit)

        return {"status": "success", "data": {"messages": messages}}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get messages: {str(e)}")
    finally:
        await client.disconnect()


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(phone: str, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user = await get_current_user_from_token(token, db)
    client = create_client(phone)
    await client.connect()

    try:
        message = await client.log_out()

        user.phone = None
        db.add(user)
        db.commit()
        db.refresh(user)

        return {"status": "success", "message": message}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to logout: {str(e)}")
    finally:
        await client.disconnect()
