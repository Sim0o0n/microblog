from microblog.app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

# Шаблон для работы с бдшками
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
