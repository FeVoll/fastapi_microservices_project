import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Убедитесь, что папка "data" существует
os.makedirs("data", exist_ok=True)

# Укажите путь к базе данных в папке "data"
DATABASE_URL = "sqlite:///./data/todo.db"

# Настройки SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # Создаём таблицы, если их нет
    Base.metadata.create_all(bind=engine)
