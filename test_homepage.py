#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from home_page import MozTrapHomePage
from base_test import BaseTest
from unittestzero import Assert


class TestHomepage(BaseTest):

    def test_that_user_can_login_and_logout(self, mozwebqa):
        from login_page import MozTrapLoginPage
        login_pg = MozTrapLoginPage(mozwebqa)
        home_pg = MozTrapHomePage(mozwebqa)

        mozwebqa.selenium.open('/')

        Assert.false(home_pg.is_user_logged_in)

        login_pg.go_to_login_page()
        login_pg.login()

        user = home_pg.testsetup.credentials['default']
        users_name_text = user['name']

        Assert.true(home_pg.is_user_logged_in)
        Assert.equal(home_pg.users_name_text, users_name_text)

        home_pg.logout()
        mozwebqa.selenium.open('/')

        Assert.false(home_pg.is_user_logged_in)

    def test_that_user_can_select_product(self, mozwebqa_logged_in):
        home_pg = MozTrapHomePage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)

        home_pg.go_to_homepage_page()

        Assert.false(home_pg.is_element_visible(product['version']['homepage_locator']))

        home_pg.select_item(product['name'])

        Assert.true(home_pg.is_element_visible(product['version']['homepage_locator']))

        self.delete_product(mozwebqa_logged_in, product=product)

    def test_that_user_can_select_version(self, mozwebqa_logged_in):
        home_pg = MozTrapHomePage(mozwebqa_logged_in)

        run = self.create_run(mozwebqa_logged_in, activate=True)

        home_pg.go_to_homepage_page()
        home_pg.select_item(run['version']['product']['name'])

        Assert.false(home_pg.is_element_visible(run['homepage_locator']))

        home_pg.select_item(run['version']['name'])

        Assert.true(home_pg.is_element_visible(run['homepage_locator']))

        self.delete_product(mozwebqa_logged_in, product=run['version']['product'])

    def test_that_user_can_select_run(self, mozwebqa_logged_in):
        home_pg = MozTrapHomePage(mozwebqa_logged_in)

        run = self.create_run(mozwebqa_logged_in, activate=True)

        home_pg.go_to_homepage_page()
        home_pg.select_item(run['version']['product']['name'])
        home_pg.select_item(run['version']['name'])

        Assert.false(home_pg.is_element_visible(run['run_tests_locator']))

        home_pg.select_item(run['name'])

        Assert.true(home_pg.is_element_visible(run['run_tests_locator']))

        self.delete_product(mozwebqa_logged_in, product=run['version']['product'])
