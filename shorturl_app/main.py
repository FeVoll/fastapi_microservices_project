from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import URL
import random
import string

app = FastAPI(
    title="Short URL Service",
    description="Сервис для сокращения URL-адресов с функциональностью редиректа и статистики. 🚀",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Short URL Management",
            "description": "Управление короткими URL: создание, редирект, статистика."
        }
    ]
)

Base.metadata.create_all(bind=engine)

def generate_short_id(db: Session):
    while True:
        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not db.query(URL).filter(URL.short_id == short_id).first():
            return short_id

@app.post(
    "/urls",
    summary="Создать короткую ссылку",
    description="Создаёт новую короткую ссылку для указанного полного URL.",
    tags=["Short URL Management"]
)
def create_short_url(full_url: str, db: Session = Depends(get_db)):
    short_id = generate_short_id(db)
    db_url = URL(short_id=short_id, full_url=full_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {
        "short_id": db_url.short_id,
        "full_url": db_url.full_url
    }

@app.get(
    "/{short_id}",
    summary="Перенаправление по короткой ссылке",
    description="Перенаправляет пользователя на полный URL, связанный с указанным коротким идентификатором.",
    tags=["Short URL Management"]
)
def redirect_to_url(short_id: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_id == short_id).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)

    return RedirectResponse(url=db_url.full_url)

@app.get(
    "/stats/{short_id}",
    summary="Получить статистику по короткой ссылке",
    description="Возвращает статистику по указанной короткой ссылке, включая количество переходов.",
    tags=["Short URL Management"]
)
def get_url_stats(short_id: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_id == short_id).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return {
        "short_id": db_url.short_id,
        "full_url": db_url.full_url,
        "clicks": db_url.clicks
    }
