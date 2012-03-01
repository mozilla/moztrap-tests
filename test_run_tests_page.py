#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from run_tests_page import CaseConductorRunTestsPage
from base_test import BaseTest
from unittestzero import Assert


class TestRunTestsPage(BaseTest):

    def test_that_user_can_pass_test(self, mozwebqa_logged_in):
        run_tests_pg = CaseConductorRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in)

        Assert.false(run_tests_pg.is_test_passed(case_name=case['name']))

        run_tests_pg.start_test(case_name=case['name'])
        run_tests_pg.pass_test(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_passed(case_name=case['name']))

        # TODO: cleanup when platform allows for deleting activated items

    def test_that_user_can_fail_test(self, mozwebqa_logged_in):
        run_tests_pg = CaseConductorRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in)

        run_tests_pg.start_test(case_name=case['name'])

        Assert.false(run_tests_pg.is_test_failed(case_name=case['name']))

        run_tests_pg.fail_test(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_failed(case_name=case['name']))

        # TODO: cleanup when platform allows for deleting activated items

    def test_that_user_can_mark_test_invalid(self, mozwebqa_logged_in):
        run_tests_pg = CaseConductorRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in)

        run_tests_pg.start_test(case_name=case['name'])

        Assert.false(run_tests_pg.is_test_invalid(case_name=case['name']))

        run_tests_pg.mark_test_invalid(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_invalid(case_name=case['name']))

        # TODO: cleanup when platform allows for deleting activated items
