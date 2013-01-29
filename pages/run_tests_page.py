#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page, PageRegion
from pages.base_page import MozTrapBasePage


class MozTrapRunTestsPage(MozTrapBasePage):

    _page_title = 'Run Tests'

    _test_pass_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .action-pass')
    _test_is_passed_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem.passed[data-title="%(case_name)s"]')
    _test_is_failed_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem.failed[data-title="%(case_name)s"]')
    _test_is_invalid_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem.invalidated[data-title="%(case_name)s"]')
    _test_summary_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .item-summary')
    _step_fail_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .steps .stepitem[data-step-number="%(step_number)s"] .stepfail .stepfail-summary')
    _step_fail_result_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .steps .stepitem[data-step-number="%(step_number)s"] .stepfail .stepfail-content .fail-field textarea[name="comment"]')
    _step_fail_submit_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .steps .stepitem[data-step-number="%(step_number)s"] .stepfail .stepfail-content .form-actions .fail')
    _test_invalid_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .testinvalid .invalid-summary')
    _test_invalid_desc_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .testinvalid .invalid-form .invalid-input')
    _test_invalid_submit_locator = (By.CSS_SELECTOR, '#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .testinvalid .invalid-form .form-actions .invalid')

    _test_item_locator = (By.CSS_SELECTOR, '.listitem')

    def open_test_summary(self, case_name):
        _open_test = (self._test_summary_locator[0], self._test_summary_locator[1] % {'case_name': case_name})
        self.selenium.find_element(*_open_test).click()

    def pass_test(self, case_name):
        _pass_test_locator = (self._test_pass_locator[0], self._test_pass_locator[1] % {'case_name': case_name})

        self.open_test_summary(case_name)
        self.selenium.find_element(*_pass_test_locator).click()
        self.wait_for_ajax()

    def fail_test(self, case_name, step_number=1):
        _step_fail_locator = (self._step_fail_locator[0], self._step_fail_locator[1] % {'case_name': case_name, 'step_number': step_number})
        _step_fail_result_locator = (self._step_fail_result_locator[0], self._step_fail_result_locator[1] % {'case_name': case_name, 'step_number': step_number})
        _step_fail_submit_locator = (self._step_fail_submit_locator[0], self._step_fail_submit_locator[1] % {'case_name': case_name, 'step_number': step_number})
        _step_fail_result = u'%(case_name)s step %(step_number)s failed' % {'step_number': step_number, 'case_name': case_name}

        self.open_test_summary(case_name)
        self.selenium.find_element(*_step_fail_locator).click()
        self.type_in_element(_step_fail_result_locator, _step_fail_result)
        self.selenium.find_element(*_step_fail_submit_locator).click()
        self.wait_for_ajax()

    def mark_test_invalid(self, case_name):
        _test_invalid_locator = (self._test_invalid_locator[0], self._test_invalid_locator[1] % {'case_name': case_name})
        _test_invalid_desc_locator = (self._test_invalid_desc_locator[0], self._test_invalid_desc_locator[1] % {'case_name': case_name})
        _test_invalid_submit_locator = (self._test_invalid_submit_locator[0], self._test_invalid_submit_locator[1] % {'case_name': case_name})
        _test_invalid_desc = u'%(case_name)s is invalid' % {'case_name': case_name}

        self.open_test_summary(case_name)
        self.selenium.find_element(*_test_invalid_locator).click()
        self.type_in_element(_test_invalid_desc_locator, _test_invalid_desc)
        self.selenium.find_element(*_test_invalid_submit_locator).click()
        self.wait_for_ajax()

    def is_test_passed(self, case_name):
        _test_is_passed_locator = (self._test_is_passed_locator[0], self._test_is_passed_locator[1] % {'case_name': case_name})

        return self.is_element_present(*_test_is_passed_locator)

    def is_test_failed(self, case_name):
        _test_is_failed_locator = (self._test_is_failed_locator[0], self._test_is_failed_locator[1] % {'case_name': case_name})

        return self.is_element_present(*_test_is_failed_locator)

    def is_test_invalid(self, case_name):
        _test_is_invalid_locator = (self._test_is_invalid_locator[0], self._test_is_invalid_locator[1] % {'case_name': case_name})

        return self.is_element_present(*_test_is_invalid_locator)

    @property
    def test_items(self):
        return [self.TestItem(self.testsetup, web_el) for web_el
                in self.selenium.find_elements(*self._test_item_locator)]

    class TestItem(PageRegion):

        _case_result_locator = (By.CSS_SELECTOR, '.result')
        _case_name_locator = (By.CSS_SELECTOR, '.title')
        _suite_name_locator = (By.CSS_SELECTOR, 'a[data-type="suite"]')
        _case_position_number_locator = (By.CSS_SELECTOR, '.order')

        @property
        def result(self):
            return self.find_element(*self._case_result_locator).text

        @property
        def name(self):
            return self.find_element(*self._case_name_locator).text

        @property
        def suite_name(self):
            return self.find_element(*self._suite_name_locator).text

        @property
        def position_number(self):
            return self.find_element(*self._case_position_number_locator).text
