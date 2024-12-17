from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import get_password_hash, verify_password, create_access_token, get_db
from app.services.user_service import oauth2_scheme

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = get_password_hash(user.password)
        new_user = User(email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error while saving user data")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {str(e)}")

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    phone = db_user.phone if db_user.phone else None

    return {"access_token": access_token, "token_type": "bearer", "phone": phone}

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(token: str = Depends(oauth2_scheme)):
    return {"message": "Logout successful"}
