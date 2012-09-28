#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_products_page import MozTrapManageProductsPage


class TestManageProductsPage(BaseTest):

    def test_that_user_can_create_and_delete_product(self, mozwebqa_logged_in):
        manage_products_pg = MozTrapManageProductsPage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)

        manage_products_pg.filter_products_by_name(name=product['name'])

        Assert.true(manage_products_pg.is_element_present(*product['locator']))

        manage_products_pg.delete_product(name=product['name'])

        Assert.false(manage_products_pg.is_element_present(*product['locator']))

    @pytest.mark.xfail(reason = "795244 - [dev]Searching by name for a product just created does not return any results ")
    def test_that_user_can_filter_product_by_name(self, mozwebqa_logged_in):
        manage_products_pg = MozTrapManageProductsPage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)

        manage_products_pg.filter_products_by_name(name='Another Product')

        Assert.false(manage_products_pg.is_element_present(*product['locator']))

        manage_products_pg.remove_name_filter(name='Another Product')
        manage_products_pg.filter_products_by_name(name=product['name'])

        Assert.true(manage_products_pg.is_element_present(*product['locator']))

        manage_products_pg.delete_product(name=product['name'])

    def test_that_user_can_filter_product_by_name_without_mouse(self, mozwebqa_logged_in):
        manage_products_pg = MozTrapManageProductsPage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)

        manage_products_pg.filter_products_by_name_without_mouse(name='Another Product')

        Assert.false(manage_products_pg.is_element_present(*product['locator']))

        manage_products_pg.remove_name_filter(name='Another Product')
        manage_products_pg.filter_products_by_name_without_mouse(name=product['name'])

        Assert.true(manage_products_pg.is_element_present(*product['locator']))

        manage_products_pg.delete_product(name=product['name'])
