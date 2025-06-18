from fastapi import Header, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from microblog.app import models
from microblog.app.deps import get_db

class InvalidAPIKeyException(Exception):
    pass

async def get_current_user(
    api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> models.User:
    user = db.query(models.User).filter(models.User.api_key == api_key).first()
    if not user:
        raise InvalidAPIKeyException()
    return user

def setup_exception_handlers(app):
    from fastapi import Request

    @app.exception_handler(InvalidAPIKeyException)
    async def invalid_key_handler(request: Request, exc):
        return JSONResponse(
            status_code=200,
            content={
                "result": False,
                "error_type": "InvalidAPIKey",
                "error_message": "Invalid or missing API key"
            }
        )
