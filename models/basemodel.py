from sqlalchemy import String, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from uuid import uuid4
from datetime import datetime
time = "%Y-%m-%dT%H:%M:%S.%f"
base = declarative_base()

class BaseModel:
    """ Base class for all models """
    id: Mapped['str'] = mapped_column(String(60), primary_key=True, default=lambda: uuid4().hex)
    created_at: Mapped['datetime'] = mapped_column(DateTime, default=datetime.utcnow())
    updated_at: Mapped['datetime'] = mapped_column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    
    def __init__(self, *args, **kwargs) -> None:
        """ Initialize a new Base object """
        for key, value in kwargs.items():
            setattr(self, key, value)
        if not self.id:
            self.id = uuid4().hex
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()

    def save(self):
        """ Save the current instance to the database """
        from models import storage
        storage.post(self)

    def delete(self):
        """ Delete the current instance from the database """
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict