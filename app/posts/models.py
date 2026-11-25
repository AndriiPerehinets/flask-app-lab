from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.Enum('news', 'publication', 'tech', 'other', name='post_category'), default='other')
    is_active = db.Column(db.Boolean, default=True)

    user_id: Mapped[int | None] = mapped_column(db.ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f"<Post(title={self.title})>"


class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag('{self.name}')>"
