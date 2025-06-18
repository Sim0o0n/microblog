from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from microblog.app.database import SessionLocal, engine
from microblog.app.models import User, Base
from microblog.app.auth import setup_exception_handlers
from microblog.app.routes import users, tweets, medias

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Инициализация пользователей
def init_fake_users():
    db = SessionLocal()
    if not db.query(User).first():
        db.add_all([
            User(username="alice", api_key="alice-key"),
            User(username="bob", api_key="bob-key")
        ])
        db.commit()
    db.close()

init_fake_users()

app = FastAPI(title="Microblog API")

setup_exception_handlers(app)

# Роуты
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(medias.router)

# Медиафайлы
app.mount("/media", StaticFiles(directory="media"), name="media")

# Абсолютный путь к frontend
frontend_path = Path(__file__).resolve().parent.parent.parent / "frontend"

# Статика фронтенда
app.mount("/css", StaticFiles(directory=frontend_path / "css"), name="css")
app.mount("/js", StaticFiles(directory=frontend_path / "js"), name="js")
app.mount("/favicon.ico", StaticFiles(directory=frontend_path), name="favicon")

# Главная страница
@app.get("/")
def serve_frontend():
    return FileResponse(frontend_path / "index.html")

@app.get("/ping")
def ping():
    return {"message": "pong"}
