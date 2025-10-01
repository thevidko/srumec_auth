# app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from models import user_model
from schemas import user_schema

# 1. Nastavení pro hashování hesel
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    print(f"[DEBUG] Hashuji heslo: {repr(password)} délka: {len(password)}")
    password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)


def create_user(db: Session, user: user_schema.UserCreate):
    """
    Vytvoří nového uživatele v databázi.

    Args:
        db: Databázová session.
        user: Data nového uživatele (z Pydantic schématu).

    Returns:
        Vytvořený uživatelský objekt (z SQLAlchemy modelu).
    """
    # 2. Zkontrolujeme, zda uživatel s daným emailem již neexistuje
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uživatel s tímto emailem již existuje."
        )

    # 3. Vytvoříme hash hesla
    hashed_password = get_password_hash(user.password)

    # 4. Vytvoříme instanci databázového modelu
    db_user = user_model.User(
        email=user.email.__str__(),
        hashed_password=hashed_password
    )

    # 5. Přidáme nového uživatele do session a uložíme do databáze
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Obnoví objekt, aby obsahoval data z DB (např. vygenerované ID)

    return db_user