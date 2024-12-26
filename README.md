# FastAPI Microservices Project

## Описание
Этот проект состоит из двух микросервисов:
1. **TODO Service**: Сервис для управления списком задач (создание, получение, обновление, удаление, переключение статуса задач).
2. **Short URL Service**: Сервис для сокращения URL-адресов с функциональностью редиректа и статистики.

Проект реализован с использованием **FastAPI**, **SQLAlchemy** и упакован в контейнеры **Docker**.

---

## Установка и запуск локально

### 1. Клонирование репозитория
```bash
git clone https://github.com/FeVoll/fastapi_microservices_project
cd fastapi_microservices_project
```

### 2. Установка зависимостей
Для каждого сервиса (`todo_app` и `shorturl_app`) выполните:
```bash
cd todo_app
pip install -r requirements.txt
cd ../shorturl_app
pip install -r requirements.txt
```

### 3. Запуск сервисов
#### TODO Service:
```bash
cd todo_app
uvicorn main:app --reload --port 8000
```

#### Short URL Service:
```bash
cd shorturl_app
uvicorn main:app --reload --port 8001
```

### 4. Доступ к API
- TODO Service: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Short URL Service: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## Запуск в Docker

### 1. Сборка Docker-образов
#### TODO Service:
```bash
docker build -t fevoll/todo-service:latest ./todo_app
```

#### Short URL Service:
```bash
docker build -t fevoll/shorturl-service:latest ./shorturl_app
```

### 2. Создание томов для данных
```bash
docker volume create todo_data
docker volume create shorturl_data
```

### 3. Запуск контейнеров
#### TODO Service:
```bash
docker run -d -p 8000:80 -v todo_data:/app/data --name todo_app_container fevoll/todo-service:latest
```

#### Short URL Service:
```bash
docker run -d -p 8001:80 -v shorturl_data:/app/data --name shorturl_app_container fevoll/shorturl-service:latest
```

### 4. Доступ к API
- TODO Service: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Short URL Service: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## Использование API

### TODO Service
#### Создание задачи
- **POST** `/items`
- **Пример запроса:**
  ```json
  {
    "title": "Купить продукты",
    "description": "Молоко, хлеб, сыр",
    "completed": false
  }
  ```
- **Пример ответа:**
  ```json
  {
    "id": 1,
    "title": "Купить продукты",
    "description": "Молоко, хлеб, сыр",
    "completed": false
  }
  ```

#### Получение всех задач
- **GET** `/items`
- **Пример ответа:**
  ```json
  [
    {
      "id": 1,
      "title": "Купить продукты",
      "description": "Молоко, хлеб, сыр",
      "completed": false
    }
  ]
  ```

#### Переключение статуса задачи
- **POST** `/items/{item_id}/toggle`
- **Пример ответа:**
  ```json
  {
    "id": 1,
    "title": "Купить продукты",
    "description": "Молоко, хлеб, сыр",
    "completed": true
  }
  ```

### Short URL Service
#### Создание короткой ссылки
- **POST** `/urls`
- **Пример запроса:**
  ```json
  {
    "full_url": "https://example.com"
  }
  ```
- **Пример ответа:**
  ```json
  {
    "short_id": "abc123",
    "full_url": "https://example.com"
  }
  ```

#### Перенаправление по короткой ссылке
- **GET** `/{short_id}`
- Перенаправляет на полный URL.

#### Получение статистики
- **GET** `/stats/{short_id}`
- **Пример ответа:**
  ```json
  {
    "short_id": "abc123",
    "full_url": "https://example.com",
    "clicks": 5
  }
  ```

---

## Использование Docker Compose

### 1. Файл `docker-compose.yml`
Создайте в корне проекта файл `docker-compose.yml` с содержимым:
```yaml
version: "3.9"

services:
  todo_app:
    build:
      context: ./todo_app
    container_name: todo_app_container
    ports:
      - "8000:80"
    volumes:
      - todo_data:/app/data

  shorturl_app:
    build:
      context: ./shorturl_app
    container_name: shorturl_app_container
    ports:
      - "8001:80"
    volumes:
      - shorturl_data:/app/data

volumes:
  todo_data:
  shorturl_data:
```

### 2. Сборка и запуск контейнеров
```bash
docker-compose up --build -d
```

### 3. Остановка и удаление контейнеров
```bash
docker-compose down
```

---

## Зависимости
- Python 3.10
- FastAPI
- SQLAlchemy
- Uvicorn
- Docker

---

