from fastapi import APIRouter, Depends, Path
from microblog.app.models import User
from microblog.app.auth import get_current_user
from sqlalchemy.orm import Session
from microblog.app import crud, models
from microblog.app.deps import get_db

router = APIRouter()

@router.get("/api/users/me")
def get_my_profile(user: User = Depends(get_current_user)):
    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.username,
            "followers": [],
            "following": []
        }
    }


@router.post("/api/users/{user_id}/follow")
def follow_user(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    success = crud.follow_user(db, current_user=user, target_user_id=user_id)
    if success:
        return {"result": True}
    return {
        "result": False,
        "error_type": "FollowError",
        "error_message": "User not found or already followed"
    }


@router.delete("/api/users/{user_id}/follow")
def unfollow_user(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    success = crud.unfollow_user(db, current_user=user, target_user_id=user_id)
    if success:
        return {"result": True}
    return {
        "result": False,
        "error_type": "FollowError",
        "error_message": "Follow relationship not found"
    }


@router.get("/api/users/{user_id}")
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_data = crud.get_user_by_id_with_followers(db, user_id)
    if not user_data:
        return {
            "result": False,
            "error_type": "UserNotFound",
            "error_message": "User with this ID does not exist"
        }

    return {"result": True, "user": user_data}
