# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class MozTrapBasePage(Page):

    @property
    def header(self):
        return self.Header(self.base_url, self.selenium)

    class Header(Page):

        _run_tests_locator = (By.CSS_SELECTOR, 'li.runtests-nav > a')
        _manage_locator = (By.CSS_SELECTOR, 'li.manage-nav > a')

        _user_name_locator = (By.CSS_SELECTOR, '#accountnav .account-welcome .fn')
        _logout_locator = (By.CSS_SELECTOR, '#logoutform > button')
        _signin_locator = (By.CSS_SELECTOR, '.signin')

        _drilldown_locator = (By.CSS_SELECTOR, 'nav.drilldown > h2')

        @property
        def is_user_logged_in(self):
            return self.is_element_visible(*self._logout_locator)

        @property
        def username_text(self):
            return self.selenium.find_element(*self._user_name_locator).text

        def click_logout(self):
            self.selenium.find_element(*self._logout_locator).click()

        def click_run_tests(self):
            self.selenium.find_element(*self._run_tests_locator).click()
            from pages.run_tests_page import MozTrapRunTestsPage
            return MozTrapRunTestsPage(self.base_url, self.selenium)

        def click_manage_locator(self):
            self.selenium.find_element(*self._manage_locator).click()
            from pages.manage_runs_page import MozTrapManageRunsPage
            return MozTrapManageRunsPage(self.base_url, self.selenium)

        def toggle_drilldown(self):
            self.selenium.find_element(*self._drilldown_locator).click()

        def login(self, email, password):
            self.find_element(*self._signin_locator).click()
            from pages.login_page import MozTrapLoginPage
            MozTrapLoginPage(self.base_url, self.selenium).login(email, password)
