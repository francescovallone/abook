# -*- coding: utf-8 -*-
"""
Integration tests for the :mod:`repoze.who`-powered authentication sub-system.

As abook grows and the authentication method changes, only these tests
should be updated.

"""
from __future__ import unicode_literals

from nose.tools import eq_, ok_

from abook.tests import TestController

from abook import model

class TestAuthentication(TestController):
    """
    Tests for the default authentication setup.

    If your application changes how the authentication layer is configured
    those tests should be updated accordingly
    """

    application_under_test = 'main'

    def test_create_contact(self):
        resp = self.app.get('/login', status=200)
        form = resp.form
        # Submitting the login form:
        form['login'] = 'francesco'
        form['password'] = 'managepass'
        post_login = form.submit(status=302)
        # Being redirected to the home page:
        ok_(post_login.location.startswith('http://localhost/post_login'))
        home_page = post_login.follow(status=302)
        ok_('authtkt' in home_page.request.cookies,
            'Session cookie was not defined: %s' % home_page.request.cookies)
        eq_(home_page.location, 'http://localhost/')
        resp = self.app.get('/add_contact', status=200)
        form = resp.form
        form['name'] = "Test Contact"
        form['number'] = "3510589682"
        post_add = form.submit(status=302)
        ok_(post_add.location.startswith('http://localhost/contacts'))
        eq_(post_add.location, 'http://localhost/contacts')
        him = model.User.by_user_name("francesco")
        contacts = [x.display_name for x in him.address_book]
        ok_("Test Contact" in contacts)

    def test_remove_contact(self):
        resp = self.app.get('/login', status=200)
        form = resp.form
        # Submitting the login form:
        form['login'] = 'francesco'
        form['password'] = 'managepass'
        post_login = form.submit(status=302)
        # Being redirected to the home page:
        ok_(post_login.location.startswith('http://localhost/post_login'))
        home_page = post_login.follow(status=302)
        ok_('authtkt' in home_page.request.cookies,
            'Session cookie was not defined: %s' % home_page.request.cookies)
        eq_(home_page.location, 'http://localhost/')
        resp = self.app.get('/add_contact', status=200)
        form = resp.form
        form['name'] = "Test Contact"
        form['number'] = "3510589682"
        post_add = form.submit(status=302)
        ok_(post_add.location.startswith('http://localhost/contacts'))
        eq_(post_add.location, 'http://localhost/contacts')
        resp = self.app.get('/contacts', status=200)
        form = resp.form
        form['contact_name'] = "Test Contact"
        form['contact_id'] = 2
        post_remove = form.submit(status=302)
        ok_(post_add.location.startswith('http://localhost/delete_contact'))
        eq_(post_add.location, 'http://localhost/contacts')
        ok_("Test Contact" not in resp)    def test_remove_contact(self):
        resp = self.app.get('/login', status=200)
        form = resp.form
        # Submitting the login form:
        form['login'] = 'francesco'
        form['password'] = 'managepass'
        post_login = form.submit(status=302)
        # Being redirected to the home page:
        ok_(post_login.location.startswith('http://localhost/post_login'))
        home_page = post_login.follow(status=302)
        ok_('authtkt' in home_page.request.cookies,
            'Session cookie was not defined: %s' % home_page.request.cookies)
        eq_(home_page.location, 'http://localhost/')
        resp = self.app.get('/add_contact', status=200)
        form = resp.form
        form['name'] = "Test Contact"
        form['number'] = "3510589682"
        post_add = form.submit(status=302)
        ok_(post_add.location.startswith('http://localhost/contacts'))
        eq_(post_add.location, 'http://localhost/contacts')
        resp = self.app.get('/contacts', status=200)
        form = resp.form
        form['contact_name'] = "Test Contact"
        form['contact_id'] = 2
        post_remove = form.submit(status=302)
        ok_(post_add.location.startswith('http://localhost/delete_contact'))
        eq_(post_add.location, 'http://localhost/contacts')
        ok_("Test Contact" not in resp)


    def test_list_contact(self):
        resp = self.app.get('/login', status=200)
        form = resp.form
        # Submitting the login form:
        form['login'] = 'francesco'
        form['password'] = 'managepass'
        post_login = form.submit(status=302)
        # Being redirected to the home page:
        ok_(post_login.location.startswith('http://localhost/post_login'))
        home_page = post_login.follow(status=302)
        ok_('authtkt' in home_page.request.cookies,
            'Session cookie was not defined: %s' % home_page.request.cookies)
        eq_(home_page.location, 'http://localhost/')
        resp = self.app.get('/contacts', status=200)
        him = model.User.by_user_name("francesco")
        contacts_name = [x.display_name for x in him.address_book]
        for c in contacts_name:
            ok_(c in resp)