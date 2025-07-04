from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import db
from flask_login import UserMixin


class KanbanColumn(db.Model):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    tasks = relationship("Task", backref="column", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    def __repr__(self):
        return f"<Column(id={self.id}, title='{self.title}')>"


class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Integer, ForeignKey("columns.id"), nullable=False)
    due_date = Column(String, index=True)
    tags = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date,
            "tags": self.tags.split(",") if self.tags else [],
        }

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', description='{self.description}', status='{self.status}', due_date='{self.due_date}', tags={self.tags})>"
    
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', password='{self.password}')>"
