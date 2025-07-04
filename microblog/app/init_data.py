from microblog.app.database import SessionLocal
from microblog.app import models

def run():
    db = SessionLocal()

    # Очистка старых данных
    db.query(models.Like).delete()
    db.query(models.Tweet).delete()
    db.query(models.Follow).delete()
    db.query(models.User).delete()

    # Создание пользователей
    alice = models.User(username="alice", api_key="alice-key")
    bob = models.User(username="bob", api_key="bob-key")
    charlie = models.User(username="charlie", api_key="charlie-key")

    db.add_all([alice, bob, charlie])
    db.commit()

    db.refresh(alice)
    db.refresh(bob)
    db.refresh(charlie)

    # Подписки
    db.add(models.Follow(follower_id=bob.id, following_id=alice.id))
    db.add(models.Follow(follower_id=charlie.id, following_id=alice.id))

    # Твиты от Alice
    tweet1 = models.Tweet(content="Привет, мир!", user_id=alice.id)
    tweet2 = models.Tweet(content="Второй твит от Alice", user_id=alice.id)

    db.add_all([tweet1, tweet2])
    db.commit()

    db.refresh(tweet1)
    db.refresh(tweet2)

    # Лайки
    db.add(models.Like(user_id=bob.id, tweet_id=tweet1.id))
    db.add(models.Like(user_id=charlie.id, tweet_id=tweet1.id))
    db.add(models.Like(user_id=charlie.id, tweet_id=tweet2.id))

    db.commit()
    db.close()
    print("✅ Данные успешно инициализированы.")

if __name__ == "__main__":
    run()
