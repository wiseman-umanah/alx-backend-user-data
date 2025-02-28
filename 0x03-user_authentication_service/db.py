#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user to db

        Args:
            email (str): email of user
            hashed_password (str): hashed password of user

        Returns:
            User: returns user object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find user based on keywords

        Returns:
            User: The user found based on the criteria.

        Raises:
            InvalidRequestError: If an invalid attribute is provided.
            NoResultFound: If no user matches the criteria.
        """
        keys = User.__table__.columns.keys()
        if not kwargs:
            raise InvalidRequestError
        for i in kwargs.keys():
            if i not in keys:
                raise InvalidRequestError
        res = self._session.query(User).filter_by(**kwargs).first()
        if res is None:
            raise NoResultFound
        return res

    def update_user(self, user_id: str, **kwargs) -> None:
        """updated user model

        Args:
            user_id (str): the user_id to update
        """
        try:
            user = self.find_user_by(id=user_id)
            keys = User.__table__.columns.keys()
            if not kwargs:
                raise NoResultFound
            for i in kwargs.keys():
                if i not in keys:
                    raise NoResultFound
        except NoResultFound:
            raise ValueError
        self._session.query(User).filter(User.id == user.id).update(kwargs)
        self._session.commit()
