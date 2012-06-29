#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import base64
from unittestzero import Assert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


class Page(object):
    """
    Base class for all Pages
    """

    def __init__(self, testsetup):
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout

    @property
    def is_the_current_page(self):
        if self._page_title:
            page_title = self.page_title
            Assert.equal(page_title, self._page_title,
                         "Expected page title: %s. Actual page title: %s" % \
                         (self._page_title, page_title))

    @property
    def url_current_page(self):
        return(self.selenium.current_url)

    @property
    def page_title(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: s.title)
        return self.selenium.title

    def get_relative_path(self, url):
        self.selenium.get(self.base_url + url)

    def is_element_present(self, by, value):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(by, value)
            return True
        except NoSuchElementException:
            # this will return a snapshot, which takes time.
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def is_element_visible(self, by, value):
        try:
            return self.selenium.find_element(by, value).is_displayed()
        except NoSuchElementException, ElementNotVisibleException:
            # this will return a snapshot, which takes time.
            return False

    def wait_for_ajax(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: s.execute_script("return $.active == 0"),
                    "Wait for AJAX timed out after %s seconds" % self.timeout)
