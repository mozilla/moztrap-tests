#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

def pytest_funcarg__mozwebqa_logged_in(request):
    mozwebqa = request.getfuncargvalue('mozwebqa')

    from login_page import MozTrapLoginPage
    login_pg = MozTrapLoginPage(mozwebqa)
    mozwebqa.selenium.open('/')
    login_pg.login()

    return mozwebqa
