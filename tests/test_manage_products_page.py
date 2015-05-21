#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_products_page import MozTrapManageProductsPage


class TestManageProductsPage(BaseTest):

    @pytest.mark.moztrap([145, 146])
    def test_that_user_can_create_and_delete_product(self, mozwebqa, login):
        manage_products_pg = MozTrapManageProductsPage(mozwebqa)

        product = self.create_product(mozwebqa)

        manage_products_pg.filter_form.filter_by(lookup='name', value=product['name'])

        Assert.true(manage_products_pg.is_element_present(*product['locator']))

        manage_products_pg.delete_product(name=product['name'])

        Assert.false(manage_products_pg.is_element_present(*product['locator']))

    @pytest.mark.moztrap(151)
    def test_that_user_can_filter_product_by_name(self, mozwebqa, login, product):
        manage_products_pg = MozTrapManageProductsPage(mozwebqa)
        manage_products_pg.go_to_manage_products_page()

        filter_item = manage_products_pg.filter_form.filter_by(lookup='name', value='Another Product')

        Assert.false(manage_products_pg.is_product_present(product))

        filter_item.remove_filter()
        manage_products_pg.filter_form.filter_by(lookup='name', value=product['name'])

        Assert.true(manage_products_pg.is_product_present(product))

    @pytest.mark.moztrap(3415)
    def test_that_user_can_filter_product_by_name_without_mouse(self, mozwebqa, login, product):
        manage_products_pg = MozTrapManageProductsPage(mozwebqa)
        manage_products_pg.go_to_manage_products_page()

        filter_item = manage_products_pg.filter_form.filter_without_mouse_by(lookup='name', value='Another Product')

        Assert.false(manage_products_pg.is_product_present(product))

        filter_item.remove_filter()
        manage_products_pg.filter_form.filter_without_mouse_by(lookup='name', value=product['name'])

        Assert.true(manage_products_pg.is_product_present(product))
