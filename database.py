from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()

task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey('tasks.task_id')),
    Column("tag_id", Integer, ForeignKey('tags.tag_id'))
)

class Tag(Base):
    __tablename__ = "tags"
    tag_id = Column('tag_id', Integer, primary_key=True)
    title = Column('title', String)
    tasks = relationship(
        "Task", secondary=task_tags
    )

class Task(Base):
    __tablename__= "tasks"
    task_id = Column('task_id', Integer, primary_key=True)
    title = Column('title', String)
    completed = Column('completed', BOOLEAN)
    order = Column('order', Integer)
    tags = relationship(
        "Tag", secondary=task_tags
    )
