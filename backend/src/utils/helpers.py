import json

from sqlalchemy.orm import Session

from src.models import GlobalSignInCount, User
from src.websocket import manager


def increment_sign_in_count(db: Session, user: User):
    user.sign_in_count += 1
    db.commit()
    db.refresh(user)
    return user


def increment_global_sign_in_count(db: Session):
    global_count = db.query(GlobalSignInCount).first()
    global_count.count += 1
    db.commit()
    db.refresh(global_count)
    return global_count.count


async def increment_counts_and_broadcast(db: Session, user: User):
    """Increment personal and global sign-in counts and broadcast updates"""

    user = increment_sign_in_count(db, user)
    global_count = increment_global_sign_in_count(db)

    await manager.broadcast(
        json.dumps({"type": "update", "globalSignInCount": global_count})
    )
    await manager.send_personal_update(
        str(user.id),
        json.dumps({"type": "personalUpdate", "personalSignInCount": user.sign_in_count}),
    )

    if global_count >= 5:
        await manager.broadcast(
            json.dumps({"message": "Global sign-in count has reached 5!"})
        )

    return user, global_count
