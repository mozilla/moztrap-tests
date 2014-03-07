#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.base_page import MozTrapBasePage


class MozTrapRunTestsPage(MozTrapBasePage):

    _page_title = 'Run Tests'

    _test_item_locator = (By.CSS_SELECTOR, '#runtests .listitem')

    @property
    def test_results(self):
        return [TestResult(self.testsetup, web_el) for web_el
                in self.selenium.find_elements(*self._test_item_locator)]

    def get_test_result(self, case_name):
        for result in self.test_results:
            if result.case_name.lower() == case_name.lower():
                return result
        raise Exception('Test case "%s" is not found in the results' % case_name)


class TestResult(PageRegion):

    _case_result_locator = (By.CSS_SELECTOR, '.result')
    _case_name_locator = (By.CSS_SELECTOR, '.title')
    _suite_name_locator = (By.CSS_SELECTOR, '.filter-link.suite')
    _case_position_number_locator = (By.CSS_SELECTOR, '.order')

    _result_passed_locator = (By.CSS_SELECTOR, '.result.passed')
    _result_failed_locator = (By.CSS_SELECTOR, '.result.failed')
    _result_invalid_locator = (By.CSS_SELECTOR, '.result.invalidated')
    _result_blocked_locator = (By.CSS_SELECTOR, '.result.blocked')
    _result_skipped_locator = (By.CSS_SELECTOR, '.result.skipped')

    _open_test_summary_locator = (By.CSS_SELECTOR, '.item-summary')
    _pass_test_button_locator = (By.CSS_SELECTOR, '.action-pass')
    _fail_test_button_locator = (By.CSS_SELECTOR, '.stepfail-summary')
    _invalidate_test_button_locator = (By.CSS_SELECTOR, '.invalid-summary')
    _block_test_button_locator = (By.CSS_SELECTOR, '.block-summary')
    _skip_test_button_locator = (By.CSS_SELECTOR, '.action-skip')

    _failed_step_comment_locator = (By.CSS_SELECTOR, '.fail-field textarea[name="comment"]')
    _failed_step_submit_locator = (By.CSS_SELECTOR, '.fail')
    _invalid_test_comment_locator = (By.CSS_SELECTOR, '.invalid-input')
    _invalid_test_submit_locator = (By.CSS_SELECTOR, '.invalid')
    _blocked_test_comment_locator = (By.CSS_SELECTOR, '.block-input')
    _blocked_test_submit_locator = (By.CSS_SELECTOR, '.block')

    @property
    def case_name(self):
        return self.find_element(*self._case_name_locator).text

    @property
    def suite_name(self):
        return self.find_element(*self._suite_name_locator).text

    @property
    def position_number(self):
        return self.find_element(*self._case_position_number_locator).text

    @property
    def is_test_passed(self):
        return self.is_element_present(*self._result_passed_locator)

    @property
    def is_test_failed(self):
        return self.is_element_present(*self._result_failed_locator)

    @property
    def is_test_invalid(self):
        return self.is_element_present(*self._result_invalid_locator)

    @property
    def is_blocked(self):
        return self.is_element_present(*self._result_blocked_locator)

    @property
    def is_skipped(self):
        return self.is_element_present(*self._result_skipped_locator)

    def open_test_summary(self):
        self.find_element(*self._open_test_summary_locator).click()

    def pass_test(self):
        self.open_test_summary()
        self.find_element(*self._pass_test_button_locator).click()
        self.wait_for_ajax()

    def fail_test(self):
        self.open_test_summary()
        self.find_element(*self._fail_test_button_locator).click()
        self.type_in_element(self._failed_step_comment_locator,
                             u'Test case "%s" failed' % self.case_name)
        self.find_element(*self._failed_step_submit_locator).click()
        self.wait_for_ajax()

    def invalidate_test(self):
        self.open_test_summary()
        self.selenium.find_element(*self._invalidate_test_button_locator).click()
        self.type_in_element(self._invalid_test_comment_locator,
                             u'Test case "%s" is invalid' % self.case_name)
        self.selenium.find_element(*self._invalid_test_submit_locator).click()
        self.wait_for_ajax()

    def mark_blocked(self):
        self.open_test_summary()
        self.selenium.find_element(*self._block_test_button_locator).click()
        self.type_in_element(self._blocked_test_comment_locator,
                             u'Test case "%s" is blocked' % self.case_name)
        self.selenium.find_element(*self._blocked_test_submit_locator).click()
        self.wait_for_ajax()

    def skip_test(self):
        self.open_test_summary()
        self.find_element(*self._skip_test_button_locator).click()
        self.wait_for_ajax()
