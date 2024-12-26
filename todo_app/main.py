from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from schemas import TodoCreate, TodoResponse
from crud import create_todo_item, get_all_todo_items, get_todo_item, update_todo_item, delete_todo_item
from typing import List

app = FastAPI(
    title="Todo API",
    description="API для управления списком задач (Todo List). Позволяет создавать, читать, обновлять, удалять и переключать статус задач.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Todo Management",
            "description": "Управление задачами: создание, получение, обновление, удаление и переключение статуса."
        }
    ]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

init_db()

@app.post("/items",
          response_model=TodoResponse,
          tags=["Todo Management"],
          summary="Создать новую задачу",
          description="Создаёт новую задачу с указанными параметрами (название, описание, статус).")
def create_item(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo_item(db, todo)

@app.get("/items",
         response_model=List[TodoResponse],
         tags=["Todo Management"],
         summary="Получить список задач",
         description="Возвращает список всех задач из базы данных.")
def get_items(db: Session = Depends(get_db)):
    return get_all_todo_items(db)

@app.get("/items/{item_id}",
         response_model=TodoResponse,
         tags=["Todo Management"],
         summary="Получить задачу по ID",
         description="Возвращает данные задачи по указанному ID.")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = get_todo_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}",
         response_model=TodoResponse,
         tags=["Todo Management"],
         summary="Обновить задачу",
         description="Обновляет данные задачи по указанному ID.")
def update_item(item_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    item = update_todo_item(db, item_id, todo)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}",
            tags=["Todo Management"],
            summary="Удалить задачу",
            description="Удаляет задачу по указанному ID.")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = get_todo_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_todo_item(db, item_id)
    return {"message": "Item deleted"}

@app.post("/items/{item_id}/toggle",
          response_model=TodoResponse, tags=["Todo Management"],
          summary="Переключить статус задачи",
          description="Изменяет статус задачи на противоположный (выполнена/не выполнена).")
def toggle_item_status(item_id: int, db: Session = Depends(get_db)):
    item = get_todo_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.completed = not item.completed
    db.commit()
    db.refresh(item)
    return item
