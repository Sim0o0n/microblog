import typing
from sqlalchemy.orm import Session
from microblog.app.models import Tweet, User, Like
import os
import uuid
from fastapi import UploadFile
from microblog.app.models import Media


def create_tweet(db: Session, content: str, owner: User) -> Tweet:
    tweet = Tweet(content=content, owner=owner)
    db.add(tweet)
    db.commit()
    db.refresh(tweet)
    return tweet

def delete_tweet(db: Session, tweet_id: int, user: User) -> bool:
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()

    if not tweet or tweet.owner != user:
        return False

    db.delete(tweet)
    db.commit()
    return True


def add_like(db: Session, tweet_id: int, user: User) -> bool:
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        return False

    existing = db.query(Like).filter(
        Like.tweet_id == tweet_id,
        Like.user_id == user.id
    ).first()

    if existing:
        return False

    like = Like(tweet_id=tweet_id, user_id=user.id)
    db.add(like)
    db.commit()
    return True


def remove_like(db: Session, tweet_id: int, user: User) -> bool:
    like = db.query(Like).filter(
        Like.tweet_id == tweet_id,
        Like.user_id == user.id
    ).first()

    if not like:
        return False

    db.delete(like)
    db.commit()
    return True

from microblog.app.models import Follow

def follow_user(db: Session, current_user: User, target_user_id: int) -> bool:
    if current_user.id == target_user_id:
        return False

    target = db.query(User).filter(User.id == target_user_id).first()
    if not target:
        return False

    existing = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == target_user_id
    ).first()

    if existing:
        return False

    follow = Follow(follower_id=current_user.id, following_id=target_user_id)
    db.add(follow)
    db.commit()
    return True


def unfollow_user(db: Session, current_user: User, target_user_id: int) -> bool:
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == target_user_id
    ).first()

    if not follow:
        return False

    db.delete(follow)
    db.commit()
    return True


def get_feed_tweets(db: Session, user: User) -> typing.List[typing.Dict]:
    # Получаем ID всех, на кого подписан текущий пользователь
    followed_ids = [
        follow.following_id for follow in user.following
    ]

    if not followed_ids:
        return []

    # Получаем твиты от этих пользователей
    tweets = db.query(Tweet).filter(Tweet.user_id.in_(followed_ids)).all()

    # Сортировка по количеству лайков
    tweets.sort(key=lambda t: len(t.likes), reverse=True)

    result = []
    for tweet in tweets:
        result.append({
            "id": tweet.id,
            "content": tweet.content,
            "attachments": [],
            "author": {
                "id": tweet.owner.id,
                "name": tweet.owner.username
            },
            "likes": [
                {"user_id": like.user.id, "name": like.user.username}
                for like in tweet.likes
            ]
        })

    return result



MEDIA_DIR = "media"

def save_media_file(db: Session, file: UploadFile) -> Media:
    os.makedirs(MEDIA_DIR, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(MEDIA_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    media = Media(file_path=file_path)
    db.add(media)
    db.commit()
    db.refresh(media)

    return media


def get_user_by_id_with_followers(db: Session, user_id: int) -> typing.Optional[typing.Dict]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    return {
        "id": user.id,
        "name": user.username,
        "followers": [
            {"id": f.follower.id, "name": f.follower.username}
            for f in user.followers
        ],
        "following": [
            {"id": f.following.id, "name": f.following.username}
            for f in user.following
        ]
    }
