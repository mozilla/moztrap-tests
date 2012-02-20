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

        # TODO: uncomment when the id's are added
        #Assert.false(home_pg.is_user_logged_in)

        Assert.true(home_pg.is_user_logged_in)
        welcome_text = u'Welcome %s [Sign Out]' % user['name']
        Assert.equal(home_pg.users_name_text, welcome_text)

        login_page = home_pg.logout()

        #Assert.false(home_pg.is_user_logged_in)
        Assert.true(login_page.is_register_visible)
        Assert.true(login_page.is_signin_visible)

    def test_that_user_can_select_product(self, mozwebqa_logged_in):
        home_pg = CaseConductorHomePage(mozwebqa_logged_in)

        cycle = self.create_cycle(mozwebqa_logged_in, activate=True)

        home_pg.go_to_homepage_page()

        Assert.false(home_pg.is_element_visible(cycle['homepage_locator']))

        home_pg.select_item(cycle['product']['name'])

        Assert.true(home_pg.is_element_visible(cycle['homepage_locator']))

        # TODO: uncomment when platform allows for deleting activated cycles/runs
        #self.delete_cycle(mozwebqa_logged_in, cycle, delete_product=True)

    def test_that_user_can_select_cycle(self, mozwebqa_logged_in):
        home_pg = CaseConductorHomePage(mozwebqa_logged_in)

        run = self.create_run(mozwebqa_logged_in, activate=True)

        home_pg.go_to_homepage_page()
        home_pg.select_item(run['cycle']['product']['name'])

        Assert.false(home_pg.is_element_visible(run['homepage_locator']))

        home_pg.select_item(run['cycle']['name'])

        Assert.true(home_pg.is_element_visible(run['homepage_locator']))

        # TODO: uncomment when platform allows for deleting activated cycles/runs
        #self.delete_run(mozwebqa_logged_in, run, delete_cycle=True, delete_product=True)

    def test_that_user_can_select_run(self, mozwebqa_logged_in):
        home_pg = CaseConductorHomePage(mozwebqa_logged_in)

        run = self.create_run(mozwebqa_logged_in, activate=True)

        home_pg.go_to_homepage_page()
        home_pg.select_item(run['cycle']['product']['name'])
        home_pg.select_item(run['cycle']['name'])

        Assert.false(home_pg.is_element_visible(run['run_tests_locator']))

        home_pg.select_item(run['name'])

        Assert.true(home_pg.is_element_visible(run['run_tests_locator']))

        # TODO: uncomment when platform allows for deleting activated cycles/runs
        #self.delete_run(mozwebqa_logged_in, run, delete_cycle=True, delete_product=True)
