#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException


class Page(object):
    """
    Base class for all Pages
    """

    def __init__(self, testsetup):
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout
        self._selenium_root = hasattr(self, '_root_element') and self._root_element or self.selenium

    @property
    def is_the_current_page(self):
        if self._page_title:
            page_title = self.page_title
            Assert.contains(self._page_title, page_title)

    @property
    def url_current_page(self):
        return(self.selenium.current_url)

    def maximize_window(self):
        try:
            self.selenium.maximize_window()
        except WebDriverException as e:
            pass

    @property
    def page_title(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
        return self.selenium.title

    def get_relative_path(self, url):
        self.selenium.get(self.base_url + url)

    def is_element_visible(self, by, value):
        try:
            return self._selenium_root.find_element(by, value).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            # this will return a snapshot, which takes time.
            return False

    def is_element_present(self, by, value):
        self.selenium.implicitly_wait(0)
        try:
            self._selenium_root.find_element(by, value)
            return True
        except NoSuchElementException:
            # this will return a snapshot, which takes time.
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_element_to_be_visible(self, *locator):
        """Wait for an element to become visible"""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: self._selenium_root.find_element(*locator).is_displayed())
        except TimeoutException:
            Assert.fail(TimeoutException)
        finally:
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: self._selenium_root.find_element(*locator))
        except TimeoutException:
            Assert.fail(TimeoutException)
        finally:
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_element_not_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: len(self._selenium_root.find_elements(*locator)) < 1)
        except TimeoutException:
            Assert.fail(TimeoutException)
        finally:
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def wait_for_ajax(self):
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.execute_script('return $.active == 0'))
        except TimeoutException:
            Assert.fail('wait for AJAX timed out after %s seconds' % self.timeout)
        finally:
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def type_in_element(self, locator, text):
        """
        Type a string into an element.

        This method clears the element first then types the string via send_keys.

        Arguments:
        locator -- a locator for the element
        text -- the string to type via send_keys
        """

        text_fld = self._selenium_root.find_element(*locator)
        text_fld.clear()
        text_fld.send_keys(text)

    def find_element(self, *locator):
        return self._selenium_root.find_element(*locator)

    def find_elements(self, *locator):
        return self._selenium_root.find_elements(*locator)

    def go_back(self):
        self.selenium.back()


class PageRegion(Page):

    def __init__(self, testsetup, element):
        self._root_element = element
        Page.__init__(self, testsetup)
