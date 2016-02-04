# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter
from pages.page import PageRegion


class MozTrapViewRunResultsPage(MozTrapBasePage):

    _page_title = 'Results-Runs'

    _run_results_item_locator = (By.CSS_SELECTOR, '#runresults .listitem')

    def go_to_view_run_results_page(self):
        self.get_relative_path('/results/runs/')
        self.is_the_current_page

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    @property
    def test_run_results(self):
        return [TestRunResult(self.testsetup, web_element)
                for web_element in self.find_elements(*self._run_results_item_locator)]


class TestRunResult(PageRegion):

    _product_version_locator = (By.CSS_SELECTOR, '.product-version')
    _name_locator = (By.CSS_SELECTOR, '.name')

    @property
    def product_version(self):
        return self.find_element(*self._product_version_locator).text

    @property
    def name(self):
        return self.find_element(*self._name_locator).text
