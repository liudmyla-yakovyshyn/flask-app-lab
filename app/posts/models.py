from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app import db


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
    author: Mapped[str] = mapped_column(
        db.String(20),
        default="Anonymous",
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Post {self.id}: {self.title}>"

