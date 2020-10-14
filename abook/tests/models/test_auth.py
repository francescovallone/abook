# -*- coding: utf-8 -*-
"""Test suite for the TG app's models"""
from __future__ import unicode_literals
from nose.tools import eq_

from abook import model
from abook.tests.models import ModelTest


# class TestUser(ModelTest):
#     """Unit test case for the ``User`` model."""

#     klass = model.User
#     attrs = dict(
#         user_name="ignucius",
#         email_address="ignucius@example.org"
#         address_book=[]
#     )

#     def test_obj_creation_username(self):
#         """The obj constructor must set the user name right"""
#         eq_(self.obj.user_name, "ignucius")

#     def test_obj_creation_email(self):
#         """The obj constructor must set the email right"""
#         eq_(self.obj.email_address, "ignucius@example.org")

#     def test_getting_by_email(self):
#         """Users should be fetcheable by their email addresses"""
#         him = model.User.by_email_address("ignucius@example.org")
#         eq_(him, self.obj)


# class TestContact(ModelTest):
#     """Unit test case for the ``Contact`` model."""

#     klass = model.Contact
#     attrs = dict(
#         display_name="test_contact",
#         phone_number="3501010100",
#         email="example@example.com",
#         user_id=1
#     )
