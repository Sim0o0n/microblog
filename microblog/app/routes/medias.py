from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from microblog.app import crud, models
from microblog.app.auth import get_current_user
from microblog.app.deps import get_db

router = APIRouter()

@router.post("/api/medias")
def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    media = crud.save_media_file(db=db, file=file)
    return {"result": True, "media_id": media.id}
