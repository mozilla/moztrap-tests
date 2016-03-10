# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mocks.mock_tag import MockTag
from pages.base_test import BaseTest
from pages.manage_tags_page import MozTrapManageTagsPage
from pages.manage_cases_page import MozTrapManageCasesPage


class TestManageTagsPage(BaseTest):

    def test_creating_a_tag_with_no_product_value_set(self, base_url, selenium, login):
        manage_tags_pg = MozTrapManageTagsPage(base_url, selenium)
        manage_tags_pg.go_to_manage_tags_page()

        create_tag_pg = manage_tags_pg.click_create_tag_button()
        assert not create_tag_pg.is_multiselect_widget_visible

        tag = MockTag()
        create_tag_pg.create_tag(tag)

        manage_tags_pg.filter_form.filter_by(lookup='name', value=tag['name'])
        displayed_tags = manage_tags_pg.tags()

        assert tag['name'] in [t.name for t in displayed_tags]

    def test_creating_a_tag_with_a_product_value_and_no_cases(self, base_url, selenium, login, product):
        manage_tags_pg = MozTrapManageTagsPage(base_url, selenium)
        manage_tags_pg.go_to_manage_tags_page()

        create_tag_pg = manage_tags_pg.click_create_tag_button()
        tag = MockTag(product=product['name'])
        create_tag_pg.create_tag(tag, save_tag=False)

        assert create_tag_pg.is_multiselect_widget_visible

        create_tag_pg.save_tag()
        manage_tags_pg.filter_form.filter_by(lookup='name', value=tag['name'])
        displayed_tags = manage_tags_pg.tags()

        assert tag['name'] in [t.name for t in displayed_tags]

    def test_creating_a_tag_with_a_product_value_and_cases(self, api, base_url, selenium, login, product):
        # create some cases for product
        cases = self.create_bulk_cases(base_url, selenium, product, api=api)
        manage_tags_pg = MozTrapManageTagsPage(base_url, selenium)
        manage_tags_pg.go_to_manage_tags_page()

        create_tag_pg = manage_tags_pg.click_create_tag_button()
        tag = MockTag(product=product['name'])
        create_tag_pg.create_tag(tag, save_tag=False)

        expected_case_names = [case.name for case in cases]
        actual_case_names = [case.name for case in create_tag_pg.available_caseversions]

        assert sorted(expected_case_names) == sorted(actual_case_names)

        create_tag_pg.include_caseversions_to_tag(expected_case_names)

        manage_cases_page = MozTrapManageCasesPage(base_url, selenium)
        manage_cases_page.go_to_manage_cases_page()
        manage_cases_page.filter_form.filter_by(lookup='tag', value=tag['name'])

        displayed_case_names = [case.name for case in manage_cases_page.test_cases]

        assert sorted(expected_case_names) == sorted(displayed_case_names)
