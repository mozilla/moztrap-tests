#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from mocks.moztrap_api import MoztrapAPI


@pytest.fixture(scope='function')
def mozwebqa_logged_in(request):
    from pages.login_page import MozTrapLoginPage
    mozwebqa = request.getfuncargvalue('mozwebqa')
    login_pg = MozTrapLoginPage(mozwebqa)
    login_pg.go_to_login_page()
    login_pg.login()

    return mozwebqa


@pytest.fixture(scope='function', autouse=True)
def cleanup_product(request):
    mozwebqa = request.getfuncargvalue('mozwebqa')

    # This acts like a tearDown, running after each test function
    def fin():
        # If a product was created via the API it will be stored in mozwebqa
        if hasattr(mozwebqa, 'product'):
            api = MoztrapAPI(mozwebqa)
            api.delete_product(mozwebqa.product)
    request.addfinalizer(fin)
