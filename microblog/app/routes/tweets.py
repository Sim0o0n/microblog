from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from microblog.app import schemas, models, crud
from microblog.app.auth import get_current_user
from microblog.app.deps import get_db

router = APIRouter()

@router.post("/api/tweets")
def create_tweet(
    request: schemas.TweetCreateRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    tweet = crud.create_tweet(db=db, content=request.tweet_data, owner=user)
    return {"result": True, "tweet_id": tweet.id}


@router.delete("/api/tweets/{tweet_id}")
def delete_tweet(
    tweet_id: int = Path(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    success = crud.delete_tweet(db=db, tweet_id=tweet_id, user=user)
    if success:
        return {"result": True}
    return {
        "result": False,
        "error_type": "Unauthorized",
        "error_message": "Tweet not found or permission denied"
    }

@router.post("/api/tweets/{tweet_id}/likes")
def like_tweet(
    tweet_id: int = Path(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    success = crud.add_like(db, tweet_id, user)
    if success:
        return {"result": True}
    return {
        "result": False,
        "error_type": "LikeError",
        "error_message": "Tweet not found or already liked"
    }


@router.delete("/api/tweets/{tweet_id}/likes")
def unlike_tweet(
    tweet_id: int = Path(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    success = crud.remove_like(db, tweet_id, user)
    if success:
        return {"result": True}
    return {
        "result": False,
        "error_type": "LikeError",
        "error_message": "Like not found"
    }

@router.get("/api/tweets")
def get_feed(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    feed = crud.get_feed_tweets(db=db, user=user)
    return {"result": True, "tweets": feed}
