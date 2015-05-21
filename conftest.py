# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from mocks.mock_product import MockProduct
from mocks.mock_element import MockElement
from mocks.moztrap_api import MoztrapAPI


@pytest.fixture
def stored_users(variables):
    return variables['users']


@pytest.fixture
def existing_user(stored_users):
    return stored_users['default']


@pytest.fixture(scope='function')
def login(request, mozwebqa, existing_user):
    from pages.login_page import MozTrapLoginPage
    login_pg = MozTrapLoginPage(mozwebqa)
    login_pg.go_to_login_page()
    login_pg.login(existing_user['email'], existing_user['password'])


@pytest.fixture
def api(request, variables):
    url = request.getfuncargvalue('mozwebqa').base_url
    return MoztrapAPI(variables['api']['user'], variables['api']['key'], url)


@pytest.fixture(scope='function')
def product(request, api):
    """Return a product created via the API."""
    product = MockProduct()
    api.create_product(product)

    def fin():
        if not product.get('deleted', False):
            api.delete_product(product)
    request.addfinalizer(fin)
    return product


@pytest.fixture(scope='function')
def element(request, api, product):
    """Return an element with an embedded category created via the API."""
    element = MockElement()
    api.create_element(element)

    def fin():
        api.delete_product(product)
        product['deleted'] = True
        api.delete_element(element)
    request.addfinalizer(fin)
    return element
