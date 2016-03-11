# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter


class MozTrapManageTagsPage(MozTrapBasePage):

    _page_title = 'Manage-Tags'

    _create_tag_button_locator = (By.CSS_SELECTOR, '#managetags .create.single')
    _tag_item_locator = (By.CSS_SELECTOR, '.listitem')

    @property
    def filter_form(self):
        return Filter(self.base_url, self.selenium)

    def go_to_manage_tags_page(self):
        self.get_relative_path('/manage/tags/')
        self.is_the_current_page

    def click_create_tag_button(self):
        self.find_element(*self._create_tag_button_locator).click()
        from pages.create_tag_page import MozTrapCreateTagPage
        return MozTrapCreateTagPage(self.base_url, self.selenium)

    def tags(self):
        return [TagItem(self.base_url, self.selenium, web_element) for web_element
                in self.find_elements(*self._tag_item_locator)]


class TagItem(PageRegion):

    _tag_name_locator = (By.CSS_SELECTOR, '.title')

    @property
    def name(self):
        return self.find_element(*self._tag_name_locator).text
