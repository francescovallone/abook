# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, validate
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from abook import model
from abook.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController
import tw2.core as twc
import tw2.forms as twf
import transaction
import re
from formencode import validators

from abook.lib.base import BaseController
from abook.controllers.error import ErrorController

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the abook application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "abook"


    @expose('abook.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')
    

    @expose('abook.templates.contacts')
    def contacts(self):
        if request.identity:
            logged = DBSession.query(model.User).filter(model.User.user_name == request.identity['repoze.who.userid']).first()
            items = [{'contact_id': item.contact_id, 'name':item.display_name,'phone':item.phone_number} for item in logged.address_book]
            """Handle the front-page."""
            print(items)
            return dict(form=DeleteContactForm,items=items, username=logged.user_name, contact_lenght=len(items))
        else:
            redirect('/')
            flash(_("You must be logged in"), 'error')


    @expose('abook.templates.addc')
    def add_contact(self, *args, **kw):
        if not request.identity:
            redirect('/')
            flash(_("You must be logged in"), 'error')
        else:
            return dict(form=ContactForm)
        

    @expose()
    def save_contact(self, **kw):
        c = model.Contact()
        c.display_name = kw['name']
        c.phone_number = kw['number']
        DBSession.add(c)
        logged = DBSession.query(model.User).filter(model.User.user_name == request.identity['repoze.who.userid']).first()
        logged.address_book.append(c)
        DBSession.add(logged)
        DBSession.flush()
        transaction.commit()
        redirect('/contacts')
        flash(_('Contact %s added!') % kw['name'])


    @expose()
    def delete_contact(self, **kw):
        DBSession.query(model.Contact).filter(model.Contact.contact_id==int(kw['contact_id'])).delete()
        transaction.commit()
        redirect('/contacts')
        flash(_("Contact %s deleted successfully!") % kw['contact_name'])


    @expose('json')
    def export_contacts(self):
        logged = DBSession.query(model.User).filter(model.User.user_name == request.identity['repoze.who.userid']).first()
        data = {'user': logged.user_name, 'contacts': [{'contact_name':item.display_name,'contact_number':item.phone_number} for item in logged.address_book]}
        return data


    @expose('abook.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)


    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)


class ContactForm(twf.Form):
    """The WidgetsList defines the fields of the form."""

    class child(twf.ListLayout):
        name = twf.TextField(twc.Required)
        number = twf.TextField(twc.Required)
    action = lurl('/save_contact')


class DeleteContactForm(twf.Form):
    class child(twf.ListLayout):
        contact_id = twf.IgnoredField()
        contact_name = twf.IgnoredField()
    action = lurl('/delete_contact')