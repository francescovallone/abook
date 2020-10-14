# -*- coding: utf-8 -*-
"""
Integration tests for the :mod:`repoze.who`-powered authentication sub-system.

As abook grows and the authentication method changes, only these tests
should be updated.

"""
from __future__ import unicode_literals

from nose.tools import eq_, ok_

from abook.tests import TestController


class TestAuthentication(TestController):
    """
    Tests for the default authentication setup.

    If your application changes how the authentication layer is configured
    those tests should be updated accordingly
    """

    application_under_test = 'main'
    # def test_forced_login(self):
    #     """Anonymous users are forced to login

    #     Test that anonymous users are automatically redirected to the login
    #     form when authorization is denied. Next, upon successful login they
    #     should be redirected to the initially requested page.

    #     """
    #     # Requesting a protected area
    #     resp = self.app.get('/contacts/', status=302)
    #     ok_(resp.location.startswith('http://localhost/login'))
    #     # Getting the login form:
    #     resp = resp.follow(status=200)
    #     form = resp.form
    #     # Submitting the login form:
    #     form['login'] = 'MushiKun'
    #     form['password'] = 'managepass'
    #     post_login = form.submit(status=302)
    #     # Being redirected to the initially requested page:
    #     ok_(post_login.location.startswith('http://localhost/post_login'))
    #     initial_page = post_login.follow(status=302)
    #     ok_('authtkt' in initial_page.request.cookies,
    #         "Session cookie wasn't defined: %s" % initial_page.request.cookies)
    #     ok_(initial_page.location.startswith('http://localhost/contacts/'),
    #         initial_page.location)

    # def test_voluntary_login(self):
    #     """Voluntary logins must work correctly"""
    #     # Going to the login form voluntarily:
    #     resp = self.app.get('/login', status=200)
    #     form = resp.form
    #     # Submitting the login form:
    #     form['login'] = 'MushiKun'
    #     form['password'] = 'managepass'
    #     post_login = form.submit(status=302)
    #     # Being redirected to the home page:
    #     ok_(post_login.location.startswith('http://localhost/post_login'))
    #     home_page = post_login.follow(status=302)
    #     ok_('authtkt' in home_page.request.cookies,
    #         'Session cookie was not defined: %s' % home_page.request.cookies)
    #     eq_(home_page.location, 'http://localhost/')

    # def test_logout(self):
    #     """Logouts must work correctly"""
    #     # Logging in voluntarily the quick way:
    #     resp = self.app.get('/login_handler?login=MushiKun&password=managepass',
    #                         status=302)
    #     resp = resp.follow(status=302)
    #     ok_('authtkt' in resp.request.cookies,
    #         'Session cookie was not defined: %s' % resp.request.cookies)
    #     # Logging out:
    #     resp = self.app.get('/logout_handler', status=302)
    #     ok_(resp.location.startswith('http://localhost/post_logout'))
    #     # Finally, redirected to the home page:
    #     home_page = resp.follow(status=302)
    #     authtkt = home_page.request.cookies.get('authtkt')
    #     ok_(not authtkt or authtkt == 'INVALID',
    #         'Session cookie was not deleted: %s' % home_page.request.cookies)
    #     eq_(home_page.location, 'http://localhost/')

    # def test_failed_login_keeps_username(self):
    #     """Wrong password keeps user_name in login form"""
    #     resp = self.app.get('/login_handler?login=MushiKun&password=badpassword',
    #                         status=302)
    #     resp = resp.follow(status=200)
    #     ok_('Invalid Password' in resp, resp)
    #     eq_(resp.form['login'].value, 'MushiKun')

    def test_create_contact(self):
        resp = self.app.get('/login', status=200)
        form = resp.form
        # Submitting the login form:
        form['login'] = 'MushiKun'
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
        form['email'] = "example@example.com"
        post_add = form.submit(status=302)
        ok_(post_add.location.startswith('http://localhost/contacts'))
        eq_(post_add.location, 'http://localhost/contacts')

    def test_remove_contact(self):
        resp = self.app.get('/login', status=200)
        form = resp.form
        # Submitting the login form:
        form['login'] = 'MushiKun'
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
        ok_(post_add.location.startswith('http://localhost/contacts'))
        eq_(post_add.location, 'http://localhost/contacts')

    def test_list_contact(self):
        resp = self.app.get('/login', status=200)
        form = resp.form
        # Submitting the login form:
        form['login'] = 'MushiKun'
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
        form['email'] = "example@example.com"
        post_add = form.submit(status=302)
        ok_(post_add.location.startswith('http://localhost/contacts'))
        eq_(post_add.location, 'http://localhost/contacts')
        resp = self.app.get('http://localhost/contacts')
        ok_("Test Contact" in resp)