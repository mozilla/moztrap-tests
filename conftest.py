#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from mocks.mock_product import MockProduct
from mocks.mock_element import MockElement
from mocks.moztrap_api import MoztrapAPI


@pytest.fixture(scope='function')
def mozwebqa_logged_in(request):
    from pages.login_page import MozTrapLoginPage
    mozwebqa = request.getfuncargvalue('mozwebqa')
    login_pg = MozTrapLoginPage(mozwebqa)
    login_pg.go_to_login_page()
    login_pg.login()

    return mozwebqa


@pytest.fixture(scope='function')
def product(request):
    """Return a product created via the Moztrap API, and automatically delete the product after the test."""
    mozwebqa = request.getfuncargvalue('mozwebqa')
    credentials = mozwebqa.credentials['default']
    request.product = MockProduct()
    api = MoztrapAPI(credentials['username'], credentials['api_key'], mozwebqa.base_url)
    api.create_product(request.product)

    # This acts like a tearDown, running after each test function
    def fin():
        # If a product was created via the API it will be stored in mozwebqa
        if hasattr(request, 'product'):
            api = MoztrapAPI(credentials['username'], credentials['api_key'], mozwebqa.base_url)
            api.delete_product(request.product)
    request.addfinalizer(fin)
    return request.product


@pytest.fixture(scope='function')
def element(request):
    """Return an element with an embedded category created via the Moztrap API,
     and automatically delete them after the test."""
    mozwebqa = request.getfuncargvalue('mozwebqa')
    credentials = mozwebqa.credentials['default']
    request.element = MockElement()
    api = MoztrapAPI(credentials['username'], credentials['api_key'], mozwebqa.base_url)
    api.create_element(request.element)

    # This acts like a tearDown, running after each test function
    def fin():
        # If a product was created via the API it will be stored in mozwebqa
        if hasattr(request, 'element'):
            api = MoztrapAPI(credentials['username'], credentials['api_key'], mozwebqa.base_url)
            # TODO: Neither of these deletes work - generate a 500 error - maybe because the test case is still around?
            # api.delete_element(request.element)
            # api.delete_category(request.element['category'])
    request.addfinalizer(fin)
    return request.element


@pytest.fixture(scope='function')
def product(request):
    """Return a product created via the Moztrap API, and automatically delete the product after the test."""
    mozwebqa = request.getfuncargvalue('mozwebqa')
    credentials = mozwebqa.credentials['default']
    request.product = MockProduct()
    api = MoztrapAPI(credentials['username'], credentials['api_key'], mozwebqa.base_url)
    api.create_product(request.product)

    # This acts like a tearDown, running after each test function
    def fin():
        # If a product was created via the API it will be stored in mozwebqa
        if hasattr(request, 'product'):
            api.delete_product(request.product)
    request.addfinalizer(fin)
    return request.product
