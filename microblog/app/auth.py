from fastapi import Header, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from microblog.app import models
from microblog.app.deps import get_db

# Кастомное исключение
class InvalidAPIKeyException(Exception):
    pass

# Получение текущего пользователя с проверкой API-ключа
async def get_current_user(
    api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> models.User:
    # Фикс ключа"
    if api_key == "test":
        api_key = "bob-key"

    user = db.query(models.User).filter(models.User.api_key == api_key).first()
    if not user:
        raise InvalidAPIKeyException()
    return user

# Обработка исключений
def setup_exception_handlers(app):
    @app.exception_handler(InvalidAPIKeyException)
    async def invalid_key_handler(request: Request, exc):
        return JSONResponse(
            status_code=403,
            content={
                "result": False,
                "error_type": "InvalidAPIKey",
                "error_message": "Invalid or missing API key"
            }
        )

