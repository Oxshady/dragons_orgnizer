from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer,String, Float, ForeignKey
from models.basemodel import BaseModel, base


class Event(BaseModel, base):
	"""Event class"""
	__tablename__ = 'events'
	name: Mapped['str'] = mapped_column(String(60), nullable=False)
	image: Mapped['str'] = mapped_column(String(100), nullable=False)	
	description: Mapped['str'] = mapped_column(String(100), nullable=False)
	members: Mapped['int'] = mapped_column(Integer, nullable=False)
	price: Mapped['float'] = mapped_column(Float, nullable=False)
	category_id: Mapped['str'] = mapped_column(String(60), ForeignKey('categories.id'),nullable=False)
	def __init__(self, *args, **kwargs) -> None:
		""" Initialize a new Product object """
		super().__init__(*args, **kwargs)