from pydantic import BaseModel, EmailStr
from datetime import datetime

# -- Základní schéma s atributy, které jsou společné --
class UserBase(BaseModel):
    email: EmailStr  # EmailStr automaticky validuje, že jde o platný email


# -- Schéma pro vytváření uživatele (co přijímáme od klienta) --
class UserCreate(UserBase):
    password: str


# -- Schéma pro čtení uživatele (co vracíme klientovi) --
# Nikdy nevracíme heslo!
class User(UserBase):
    id: int
    created_at: datetime

    # Konfigurace, která Pydanticu řekne, aby četl data i z atributů objektu
    # (nejen ze slovníku), což je nutné pro konverzi z ORM modelu.
    class Config:
        from_attributes = True
