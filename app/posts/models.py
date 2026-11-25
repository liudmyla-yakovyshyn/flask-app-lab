from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

if TYPE_CHECKING:
    from app.users.models import User


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(150), nullable=False)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    category: Mapped[str] = mapped_column(
        db.Enum("news", "publication", "tech", "other", name="post_category"),
        default="other",
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        db.Boolean,
        default=True,
        nullable=False,
    )
    user_id: Mapped[int | None] = mapped_column(
        db.ForeignKey("users.id"),
        nullable=True,
    )
    user: Mapped["User | None"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post {self.id}: {self.title}>"
