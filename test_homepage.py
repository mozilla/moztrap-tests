#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from home_page import CaseConductorHomePage
from base_test import BaseTest
from unittestzero import Assert


class TestHomepage(BaseTest):

    def test_that_user_can_login_and_logout(self, mozwebqa_logged_in):
        home_pg = CaseConductorHomePage(mozwebqa_logged_in)

        user = home_pg.testsetup.credentials['default']
        home_pg.go_to_homepage_page()

        Assert.true(home_pg.is_user_logged_in)
        users_name_text = user['name']
        Assert.equal(home_pg.users_name_text, users_name_text)

        login_page = home_pg.logout()

        Assert.false(home_pg.is_user_logged_in)
        Assert.true(login_page.is_register_visible)
        Assert.true(login_page.is_signin_visible)

    def test_that_user_can_login_using_browserid(self, mozwebqa):
        from login_page import CaseConductorLoginPage
        login_pg = CaseConductorLoginPage(mozwebqa)
        home_pg = CaseConductorHomePage(mozwebqa)

        mozwebqa.selenium.open('/')

        Assert.false(home_pg.is_user_logged_in)
        Assert.true(login_pg.is_register_visible)
        Assert.true(login_pg.is_signin_visible)

        login_pg.login_using_browserid()

        user = home_pg.testsetup.credentials['default']
        users_name_text = user['name']

        Assert.true(home_pg.is_user_logged_in)
        Assert.equal(home_pg.users_name_text, users_name_text)

        home_pg.logout()

    def test_that_user_can_select_product(self, mozwebqa_logged_in):
        home_pg = CaseConductorHomePage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)

        home_pg.go_to_homepage_page()

        Assert.false(home_pg.is_element_visible(product['version']['homepage_locator']))

        home_pg.select_item(product['name'])

        Assert.true(home_pg.is_element_visible(product['version']['homepage_locator']))

        self.delete_product(mozwebqa_logged_in, product=product)

    def test_that_user_can_select_version(self, mozwebqa_logged_in):
        home_pg = CaseConductorHomePage(mozwebqa_logged_in)

        run = self.create_run(mozwebqa_logged_in, activate=True)

        home_pg.go_to_homepage_page()
        home_pg.select_item(run['version']['product']['name'])

        Assert.false(home_pg.is_element_visible(run['homepage_locator']))

        home_pg.select_item(run['version']['name'])

        Assert.true(home_pg.is_element_visible(run['homepage_locator']))

        self.delete_product(mozwebqa_logged_in, product=run['version']['product'])

    def test_that_user_can_select_run(self, mozwebqa_logged_in):
        home_pg = CaseConductorHomePage(mozwebqa_logged_in)

        run = self.create_run(mozwebqa_logged_in, activate=True)

        home_pg.go_to_homepage_page()
        home_pg.select_item(run['version']['product']['name'])
        home_pg.select_item(run['version']['name'])

        Assert.false(home_pg.is_element_visible(run['run_tests_locator']))

        home_pg.select_item(run['name'])

        Assert.true(home_pg.is_element_visible(run['run_tests_locator']))

        self.delete_product(mozwebqa_logged_in, product=run['version']['product'])
