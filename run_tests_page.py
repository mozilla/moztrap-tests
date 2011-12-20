#!/usr/bin/env python
#
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Case Conductor
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from base_page import CaseConductorBasePage


class CaseConductorRunTestsPage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'
    _test_action_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../div[@class="status"]/button[@class="%(action)s"]'
    _test_is_passed_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../div[@class="status"]/span[@class="passed"]'
    _test_is_failed_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../div[@class="status"]/span[@class="failed"]'
    _test_is_invalid_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../div[@class="status"]/span[@class="invalidated"]'
    _test_summary_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../..'
    _step_fail_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../../..//ol[@class="steps"]/li[%(step_number)s]/div[contains(@class,"stepfail")]/p[@class="summary"]'
    _step_fail_result_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../../..//ol[@class="steps"]/li[%(step_number)s]/div[contains(@class,"stepfail")]//li[@class="fail-desc"]/textarea[@name="actualResult"]'
    _step_fail_submit_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../../..//ol[@class="steps"]/li[%(step_number)s]/div[contains(@class,"stepfail")]//div[@class="form-actions"]/button[@class="fail"]'
    _test_invalid_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../../..//form[contains(@class,"testinvalid")]/h4[@class="summary"]'
    _test_invalid_desc_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../../..//form[contains(@class,"testinvalid")]//textarea[@name="comment"]'
    _test_invalid_submit_locator = u'xpath=//section[@id="run"]//article[contains(@class,"item")]//h3[@title="%(case_name)s"]/../../..//form[contains(@class,"testinvalid")]//div[@class="form-actions"]/button[@class="invalid"]'

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
        _step_fail_result = u'Test Case step %(step_number)s failed' % {'step_number': step_number}

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
        _test_invalid_desc = 'Test Case is invalid'

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
