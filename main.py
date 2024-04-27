# Нужные библиотеки
import uvicorn
from fastapi import FastAPI, status, HTTPException
from typing import Dict
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
import json

app = FastAPI()

# Модель карточки продукта
class Product(BaseModel):
    product_id: int = 0
    name: str
    description: str | None = None
    price: float

# Хранилище данных
store: Dict[int, Product] = {}

# Создание карточки продукта
@app.post("/products")
async def create_product(product: Product):
    # Установка идентификатора карточки продукта на основе размера хранилища
    product.product_id = len(store) + 1
    # Добавление карточки продукта в хранилище
    store[product.product_id] = product
    # Возвращение JSON-ответа с кодом состояния 201 (CREATED)
    return JSONResponse( 
        {"id": product.product_id},
          status_code=status.HTTP_201_CREATED,
    )

# Чтение карточки продукта
@app.get("/products/{product_id}")
async def read_product(product_id: int):
    # Проверка наличия карточки продукта с указанным идентификатором в хранилище
    if product_id not in store:
        # Если карточка продукта не найден, то генерируется исключение 404 (NOT FOUND)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с id {product_id} не найден",
        )
    # Получение карточки продукта и преобразование в JSON-формат
    product = jsonable_encoder(store[product_id])
    # Возвращение JSON-ответа c кодом состояния 200 (OK)
    return JSONResponse(
        product,
        status_code=status.HTTP_200_OK,)

# Загрузка списка продуктов в виде JSON-файла
@app.get("/products_download")
async def download_products():
    products = list(store.values())
    # Запись списка продуктов в JSON-файл
    with open("products.json", "w") as f:
        json.dump(jsonable_encoder(products), f, indent=4, ensure_ascii=False)
    # Возвращение файла продуктов в качестве ответа
    return FileResponse(
        "products.json",
        headers={
            "Content-Disposition": "attachment; filename=all_products.json",
        },
    )

# Стартовая страница
@app.get('/', response_class = HTMLResponse)
def index():
    return "<b> Привет, пользователь! </b>" 

# Запуск сервера приложения FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)