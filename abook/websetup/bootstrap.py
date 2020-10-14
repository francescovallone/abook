# -*- coding: utf-8 -*-
"""Setup the wiki20 application"""
from __future__ import print_function, unicode_literals
import transaction
from abook import model


def bootstrap(command, conf, vars):
    """Place any commands to setup wiki20 here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        c = model.Contact()
        c.display_name = 'Managers Group'
        c.phone_number = '3510589682'
        model.DBSession.add(c)

        u = model.User()
        u.user_name = "francesco"
        u.email = 'example@example.com'
        u.password = 'managepass'
        u.address_book.append(c)

        model.DBSession.add(u)

        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
