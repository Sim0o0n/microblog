from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Таблица пользователей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный ID
    username = Column(String, unique=True, index=True)  # Имя пользователя
    api_key = Column(String, unique=True, index=True)   # API-ключ (для авторизации)

    tweets = relationship("Tweet", back_populates="owner")  # Все твиты, созданные этим пользователем
    likes = relationship("Like", back_populates="user")     # Все лайки, поставленные этим пользователем
    following = relationship(                               # Все подписки, кого пользователь читает
        "Follow", foreign_keys='Follow.follower_id', back_populates="follower"
    )
    followers = relationship(                               # Все подписчики, кто читает пользователя
        "Follow", foreign_keys='Follow.following_id', back_populates="following"
    )

# Таблица твитов
class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)     # Уникальный ID
    content = Column(String, index=True)                   # Текстовое содержимое твита
    user_id = Column(Integer, ForeignKey("users.id"))      # Внешний ключ на владельца твита

    owner = relationship("User", back_populates="tweets")  # Владелец твита (обратно к User)
    likes = relationship("Like", back_populates="tweet")   # Лайки под этим твитом

# Таблица лайков
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)          # Уникальный ID
    user_id = Column(Integer, ForeignKey("users.id"))           # Кто поставил лайк
    tweet_id = Column(Integer, ForeignKey("tweets.id"))         # Какому твиту

    user = relationship("User", back_populates="likes")         # Обратно к пользователю
    tweet = relationship("Tweet", back_populates="likes")       # Обратно к твиту

# Таблица подписок
class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)              # Уникальный ID
    follower_id = Column(Integer, ForeignKey("users.id"))           # Кто подписался
    following_id = Column(Integer, ForeignKey("users.id"))          # На кого подписались

    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")  # Подписчик
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")# Тот, на кого подписались


# Загрузка медиафайлов
class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)



