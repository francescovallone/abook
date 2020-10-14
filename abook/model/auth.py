import os
from datetime import datetime
from hashlib import sha256
__all__ = ['User', 'Contact']

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from abook.model import DeclarativeBase, metadata, DBSession


class User(DeclarativeBase):
    __tablename__ = 'ab_user'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(Unicode(128), unique=True, nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    _password = Column('password', Unicode(128))
    address_book = relation('Contact', cascade="all, delete-orphan")

    def __repr__(self):
        return '<User: name=%s, email=%s>' % (
            repr(self.user_name),
            repr(self.email),
        )

    def __unicode__(self):
        return self.user_name

    
    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter_by(email_address=email).first()

    @classmethod
    def by_user_name(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter_by(user_name=username).first()

    @classmethod
    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hash = sha256()
        # Make sure password is a str because we cannot hash unicode objects
        hash.update((password + salt).encode('utf-8'))
        hash = hash.hexdigest()

        password = salt + hash


        return password

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def validate_password(self, password):
        hash = sha256()
        hash.update((password + self.password[:64]).encode('utf-8'))
        return self.password[64:] == hash.hexdigest()


class Contact(DeclarativeBase):
    __tablename__ = 'ab_contact'
    contact_id = Column(Integer, autoincrement=True, primary_key=True)
    display_name = Column(Unicode(255), unique=False, nullable=False)
    phone_number = Column(Unicode(16), unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey('ab_user.user_id'))

    def __repr__(self):
        return '<Contact: user_id=%s, display=%s, number=%s>' % (
            repr(self.user_id),
            repr(self.display_name),
            repr(self.phone_number)
        )