from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from schemas import user_schema
from services import auth_service
from db.deps import get_db

router = APIRouter()

@router.post(
    "/register",
    response_model=user_schema.User,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint pro registraci nového uživatele.
    - Přijme data odpovídající schématu UserCreate.
    - Zavolá servisní logiku pro vytvoření uživatele.
    - Vrátí data odpovídající schématu User (bez hesla).
    """
    return auth_service.create_user(db=db, user=user)


@router.post("/login", response_model=user_schema.Token)
async def login_for_access_token(
        user_credentials: user_schema.UserLogin,
        db: Session = Depends(get_db)
):
    """
    Endpoint pro přihlášení uživatele a získání JWT tokenu.
    """
    user = auth_service.authenticate_user(db, user_credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nesprávné přihlašovací údaje",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(
        data={"sub": user.email}  # "sub" (subject) je standardní název pro identifikátor v JWT
    )

    return {"access_token": access_token, "token_type": "bearer"}