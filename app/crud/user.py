from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate
from utils.security import hash_password

def create_user(db: Session, user: UserCreate):

    existing_user = (
        db.query(User)
        .filter(
            (User.username == user.username) |
            (User.email == user.email)
        )
        .first()
    )

    if existing_user:
        if existing_user.username == user.username:
            raise ValueError("Username already exists")

        if existing_user.email == user.email:
            raise ValueError("Email already exists")

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user