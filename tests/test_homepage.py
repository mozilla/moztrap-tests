# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home_page import MozTrapHomePage
from pages.base_test import BaseTest


class TestHomepage(BaseTest):

    @pytest.mark.moztrap([3385, 3386])
    @pytest.mark.nondestructive
    def test_that_user_can_login_and_logout(self, base_url, selenium, existing_user):
        from pages.login_page import MozTrapLoginPage
        login_pg = MozTrapLoginPage(base_url, selenium)
        home_pg = MozTrapHomePage(base_url, selenium)

        home_pg.get_relative_path('/')
        assert not home_pg.header.is_user_logged_in

        login_pg.go_to_login_page()
        login_pg.login(existing_user['email'], existing_user['password'])
        assert home_pg.header.is_user_logged_in
        assert existing_user['name'] == home_pg.header.username_text

        home_pg.header.click_logout()
        home_pg.get_relative_path('/')
        assert not home_pg.header.is_user_logged_in

    @pytest.mark.moztrap(3387)
    def test_that_user_can_select_product(self, base_url, selenium, login, product):
        home_pg = MozTrapHomePage(base_url, selenium)

        home_pg.go_to_home_page()

        assert not home_pg.is_product_version_visible(product)

        home_pg.select_item(product['name'])

        assert home_pg.is_product_version_visible(product)

    @pytest.mark.moztrap(3388)
    def test_that_user_can_select_version(self, base_url, selenium, login, product):
        home_pg = MozTrapHomePage(base_url, selenium)

        run = self.create_run(base_url, selenium, product=product, activate=True)

        home_pg.go_to_home_page()
        home_pg.select_item(run['version']['product']['name'])

        assert not home_pg.is_element_visible(*run['homepage_locator'])

        home_pg.select_item(run['version']['name'])

        assert home_pg.is_element_visible(*run['homepage_locator'])

    @pytest.mark.moztrap(3414)
    def test_that_user_can_select_run(self, base_url, selenium, login, product):
        home_pg = MozTrapHomePage(base_url, selenium)

        run = self.create_run(base_url, selenium, product=product, activate=True)

        home_pg.go_to_home_page()
        home_pg.select_item(run['version']['product']['name'])
        home_pg.select_item(run['version']['name'])

        assert not home_pg.is_element_visible(*run['run_tests_locator'])

        home_pg.select_item(run['name'])

        assert home_pg.is_element_visible(*run['run_tests_locator'])
