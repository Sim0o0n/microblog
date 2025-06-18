from pydantic import BaseModel, Field
from typing import Optional, List


# === СХЕМЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ===

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    api_key: str = Field(..., min_length=8)

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# === СХЕМЫ ДЛЯ ТВИТОВ ===

class TweetBase(BaseModel):
    content: str = Field(..., max_length=280)

class TweetCreate(TweetBase):
    pass

class Tweet(TweetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TweetCreateRequest(BaseModel):
    tweet_data: str = Field(..., max_length=280)
    tweet_media_ids: Optional[List[int]] = None


# === СХЕМЫ ДЛЯ ЛАЙКОВ ===

class LikeBase(BaseModel):
    user_id: int
    tweet_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    id: int

    class Config:
        orm_mode = True


# === СХЕМЫ ДЛЯ ПОДПИСОК ===

class FollowBase(BaseModel):
    follower_id: int
    following_id: int

class FollowCreate(FollowBase):
    pass

class Follow(FollowBase):
    id: int

    class Config:
        orm_mode = True


# === СХЕМЫ ДЛЯ ЛЕНТЫ ТВИТОВ ===
class LikeInfo(BaseModel):
    user_id: int
    name: str

class UserInfo(BaseModel):
    id: int
    name: str

class TweetFeedItem(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: UserInfo
    likes: List[LikeInfo]

    class Config:
        orm_mode = True


class MediaOut(BaseModel):
    result: bool
    media_id: int


# === СХЕМЫ ДЛЯ ПРОФИЛЯ ===

class SimpleUserInfo(BaseModel):
    id: int
    name: str

class UserPublicProfile(BaseModel):
    id: int
    name: str
    followers: List[SimpleUserInfo]
    following: List[SimpleUserInfo]

class UserPublicResponse(BaseModel):
    result: bool
    user: UserPublicProfile
