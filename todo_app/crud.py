from sqlalchemy.orm import Session
from models import TodoItem
from schemas import TodoCreate

def create_todo_item(db: Session, todo: TodoCreate):
    # Преобразуем объект Pydantic в словарь
    db_item = TodoItem(**todo.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_todo_items(db: Session):
    return db.query(TodoItem).all()

def get_todo_item(db: Session, item_id: int):
    return db.query(TodoItem).filter(TodoItem.id == item_id).first()

def update_todo_item(db: Session, item_id: int, todo: TodoCreate):
    db_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if db_item:
        for key, value in todo.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_todo_item(db: Session, item_id: int):
    db_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
