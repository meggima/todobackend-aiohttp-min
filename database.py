from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey('tasks.task_id'), primary_key=True),
    Column("tag_id", Integer, ForeignKey('tags.tag_id'), primary_key=True)
)


class Task(Base):
    __tablename__= "tasks"
    task_id = Column('task_id', Integer, primary_key=True)
    title = Column('title', String)
    completed = Column('completed', BOOLEAN)
    order = Column('order', Integer)
    tags = relationship(
        "Tag", secondary=task_tags, back_populates="tasks"
    )

    def __init__(self, title = '', completed=False, order=0):
        self.title = title
        self.completed = completed
        self.order = order


class Tag(Base):
    __tablename__ = "tags"
    tag_id = Column('tag_id', Integer, primary_key=True)
    title = Column('title', String)
    tasks = relationship(
        "Task", secondary=task_tags, back_populates="tags"
    )

    def __init__(self, title = ''):
        self.title = title