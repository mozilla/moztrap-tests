# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.base_test import BaseTest
from pages.manage_products_page import MozTrapManageProductsPage


class TestManageProductsPage(BaseTest):

    @pytest.mark.moztrap([145, 146])
    def test_that_user_can_create_and_delete_product(self, base_url, selenium, login):
        manage_products_pg = MozTrapManageProductsPage(base_url, selenium)

        product = self.create_product(base_url, selenium)

        manage_products_pg.filter_form.filter_by(lookup='name', value=product['name'])

        assert manage_products_pg.is_element_present(*product['locator'])

        manage_products_pg.delete_product(name=product['name'])

        assert not manage_products_pg.is_element_present(*product['locator'])

    @pytest.mark.moztrap(151)
    def test_that_user_can_filter_product_by_name(self, base_url, selenium, login, product):
        manage_products_pg = MozTrapManageProductsPage(base_url, selenium)
        manage_products_pg.go_to_manage_products_page()

        filter_item = manage_products_pg.filter_form.filter_by(lookup='name', value='Another Product')

        assert not manage_products_pg.is_product_present(product)

        filter_item.remove_filter()
        manage_products_pg.filter_form.filter_by(lookup='name', value=product['name'])

        assert manage_products_pg.is_product_present(product)

    @pytest.mark.moztrap(3415)
    def test_that_user_can_filter_product_by_name_without_mouse(self, base_url, selenium, login, product):
        manage_products_pg = MozTrapManageProductsPage(base_url, selenium)
        manage_products_pg.go_to_manage_products_page()

        filter_item = manage_products_pg.filter_form.filter_without_mouse_by(lookup='name', value='Another Product')

        assert not manage_products_pg.is_product_present(product)

        filter_item.remove_filter()
        manage_products_pg.filter_form.filter_without_mouse_by(lookup='name', value=product['name'])

        assert manage_products_pg.is_product_present(product)
