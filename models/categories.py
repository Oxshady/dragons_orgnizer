from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from models.basemodel import BaseModel, base
from typing import List
class Category(BaseModel, base):
    __tablename__ = 'categories'
    """Category class"""
    name: Mapped['str'] = mapped_column(String(60), nullable=False)
    description: Mapped['str'] = mapped_column(String(100), nullable=False)
    from models.events import Event
    product: Mapped[List['Event']] = relationship(Event, backref='category', cascade='all, delete-orphan')
    def __init__(self, *args, **kwargs) -> None:
        """ Initialize a new Category object """
        super().__init__(*args, **kwargs)