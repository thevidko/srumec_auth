from fastapi import APIRouter, Depends, status
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
