from models.basemodel import BaseModel, base
from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List
from bcrypt import hashpw, gensalt,checkpw
from time import time
import jwt
from flask import current_app
from models import db

users_events = Table(
    'user_events',
    base.metadata,
    Column('event_id', String(60), ForeignKey('events.id'), nullable=False),
    Column('user_id', String(60), ForeignKey('users.id'),nullable=False),
    )


class User(BaseModel, base):
    """User class"""

    __tablename__ = "users"
    first_name: Mapped["str"] = mapped_column(String(50), nullable=False)
    last_name: Mapped["str"] = mapped_column(String(50), nullable=False)
    phoneNumber: Mapped["str"] = mapped_column(String(50), nullable=False)
    address: Mapped["str"] = mapped_column(String(100), nullable=False)
    email: Mapped["str"] = mapped_column(String(60), nullable=False)
    password: Mapped["str"] = mapped_column(String(60), nullable=False)
    from models.events import Event
    events: Mapped[List['Event']] = relationship(Event, secondary=users_events, backref='users', cascade='all, delete-orphan', single_parent=True)
    def __init__(self, *args, **kwargs) -> None:
        """Initialize a new User object"""
        super().__init__(*args, **kwargs)
        for key, value in kwargs.items():
            if key == "password":
                value = self.hash_password(value)
            setattr(self, key, value)

    def hash_password(self, password: str) -> str:
        """Hash password"""
        salt = gensalt()
        passwd = hashpw(password.encode('utf-8'), salt)
        return passwd.decode('utf-8')


    def check_password(self, password: str) -> bool:
        """Check password"""
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


    def get_reset_token(self, expires_in_sec=600):
        '''Generates a JWT token for resetting the user's password.
        
        Args:
            expires_in_sec (int): The expiration time of the token in seconds. Defaults to 600 seconds.
        
        Returns:
            str: A JWT token that encodes the user's ID and an expiration timestamp.
        '''
        encoded_data = jwt.encode(
            {'user_id': self.id, 'expire': time() + expires_in_sec},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return encoded_data

    @staticmethod
    def verify_reset_token(token):
        '''Verifies the JWT token and retrieves the user associated with it.
        
        Args:
            token (str): The JWT token to verify.
        
        Returns:
            User or None: The User object if the token is valid and not expired, otherwise None.
        '''
        try:
            decoded_data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            user_id = decoded_data['user_id']
            expiration = decoded_data['expire']
            if expiration < time():
                print('Token expired')
                return None

        except Exception:
            print('Token expired or invalid')
            return None
        return True