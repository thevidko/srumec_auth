from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import settings

# Vytvoříme "engine", který se bude starat o připojení
engine = create_engine(settings.DATABASE_URL)

# Vytvoříme "továrnu" na databázové session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Vytvoříme základní třídu pro naše databázové modely (ORM)
Base = declarative_base()