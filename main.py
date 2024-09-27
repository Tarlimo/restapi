from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Импортируем List для типов списков
import models
from crud import create_item, get_items, get_item, update_item, delete_item
from database import engine, get_db
from schemas import ItemCreate, ItemUpdate, ItemResponse

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Эндпоинт для создания Item
@app.post("/items/", response_model=ItemResponse)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db=db, item=item)

# Эндпоинт для получения списка всех Item
@app.get("/items/", response_model=List[ItemResponse])  # Используем List из typing
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_items(db=db, skip=skip, limit=limit)

# Эндпоинт для получения одного Item по ID
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Эндпоинт для обновления Item
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item_endpoint(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Эндпоинт для удаления Item
@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    db_item = delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
