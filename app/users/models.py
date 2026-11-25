from typing import TYPE_CHECKING
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import bcrypt, db, login_manager

if TYPE_CHECKING:
    from app.posts.models import Post


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(256), nullable=False)
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, raw_password: str) -> None:
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        try:
            return bcrypt.check_password_hash(self.password, raw_password)
        except ValueError:
            return False
