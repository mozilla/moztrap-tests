#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage


class CaseConductorRunTestsPage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _test_action_locator = u'css=#runtests .itemlist .listitem[data-title="%(case_name)s"] .itemhead .results .result-action.%(action)s'
    _test_is_passed_locator = u'css=#runtests .itemlist .listitem.passed[data-title="%(case_name)s"]'
    _test_is_failed_locator = u'css=#runtests .itemlist .listitem.failed[data-title="%(case_name)s"]'
    _test_is_invalid_locator = u'css=#runtests .itemlist .listitem.invalidated[data-title="%(case_name)s"]'
    _test_summary_locator = u'css=#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .item-summary'
    _step_fail_locator = u'css=#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .steps .stepitem[data-step-number="%(step_number)s"] .stepfail .stepfail-summary'
    _step_fail_result_locator = u'css=#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .steps .stepitem[data-step-number="%(step_number)s"] .stepfail .stepfail-content .fail-field .fail-input'
    _step_fail_submit_locator = u'css=#runtests .itemlist .listitem[data-title="%(case_name)s"] .itembody .steps .stepitem[data-step-number="%(step_number)s"] .stepfail .stepfail-content .form-actions .fail'
    _test_invalid_locator = u'css=#runtests .itemlist .listitem[data-title="%(case_name)s"] .itemhead .testinvalid .invalid-summary'
    _test_invalid_desc_locator = u'css=#runtests .itemlist .listitem[data-title="%(case_name)s"] .itemhead .testinvalid .invalid-form .invalid-input'
    _test_invalid_submit_locator = u'css=#runtests .itemlist .listitem[data-title="%(case_name)s"] .itemhead .testinvalid .invalid-form .form-actions .invalid'

    def start_test(self, case_name):
        _start_test_locator = self._test_action_locator % {'case_name': case_name, 'action': 'start'}

        self.click(_start_test_locator)
        self.wait_for_ajax()

    def pass_test(self, case_name):
        _pass_test_locator = self._test_action_locator % {'case_name': case_name, 'action': 'pass'}

        self.click(_pass_test_locator)
        self.wait_for_ajax()

    def fail_test(self, case_name, step_number=1):
        _test_summary_locator = self._test_summary_locator % {'case_name': case_name}
        _step_fail_locator = self._step_fail_locator % {'case_name': case_name, 'step_number': step_number}
        _step_fail_result_locator = self._step_fail_result_locator % {'case_name': case_name, 'step_number': step_number}
        _step_fail_submit_locator = self._step_fail_submit_locator % {'case_name': case_name, 'step_number': step_number}
        _step_fail_result = u'%(case_name)s step %(step_number)s failed' % {'step_number': step_number, 'case_name': case_name}

        self.click(_test_summary_locator)
        self.click(_step_fail_locator)
        self.type(_step_fail_result_locator, _step_fail_result)
        self.click(_step_fail_submit_locator)
        self.wait_for_ajax()

    def mark_test_invalid(self, case_name):
        _test_summary_locator = self._test_summary_locator % {'case_name': case_name}
        _test_invalid_locator = self._test_invalid_locator % {'case_name': case_name}
        _test_invalid_desc_locator = self._test_invalid_desc_locator % {'case_name': case_name}
        _test_invalid_submit_locator = self._test_invalid_submit_locator % {'case_name': case_name}
        _test_invalid_desc = u'%(case_name)s is invalid' % {'case_name': case_name}

        self.click(_test_summary_locator)
        self.click(_test_invalid_locator)
        self.type(_test_invalid_desc_locator, _test_invalid_desc)
        self.click(_test_invalid_submit_locator)
        self.wait_for_ajax()

    def is_test_passed(self, case_name):
        _test_is_passed_locator = self._test_is_passed_locator % {'case_name': case_name}

        return self.is_element_present(_test_is_passed_locator)

    def is_test_failed(self, case_name):
        _test_is_failed_locator = self._test_is_failed_locator % {'case_name': case_name}

        return self.is_element_present(_test_is_failed_locator)

    def is_test_invalid(self, case_name):
        _test_is_invalid_locator = self._test_is_invalid_locator % {'case_name': case_name}

        return self.is_element_present(_test_is_invalid_locator)
