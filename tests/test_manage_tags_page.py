#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from mocks.mock_tag import MockTag
from pages.base_test import BaseTest
from pages.manage_tags_page import MozTrapManageTagsPage
from pages.manage_cases_page import MozTrapManageCasesPage


class TestManageTagsPage(BaseTest):

    def test_creating_a_tag_with_no_product_value_set(self, mozwebqa_logged_in):
        manage_tags_pg = MozTrapManageTagsPage(mozwebqa_logged_in)
        manage_tags_pg.go_to_manage_tags_page()

        create_tag_pg = manage_tags_pg.click_create_tag_button()
        Assert.false(create_tag_pg.is_multiselect_widget_visible,
                     'multiselect widget should be hidden until product is not selected')

        tag = MockTag()
        create_tag_pg.create_tag(tag)

        manage_tags_pg.filter_form.filter_by(lookup='name', value=tag['name'])
        displayed_tags = manage_tags_pg.tags()

        Assert.true(tag['name'] in [t.name for t in displayed_tags],
                    'tag with "%s" name is not displayed on the page' % tag['name'])

    def test_creating_a_tag_with_a_product_value_and_no_cases(self, mozwebqa_logged_in, product):
        manage_tags_pg = MozTrapManageTagsPage(mozwebqa_logged_in)
        manage_tags_pg.go_to_manage_tags_page()

        create_tag_pg = manage_tags_pg.click_create_tag_button()
        tag = MockTag(product=product['name'])
        create_tag_pg.create_tag(tag, save_tag=False)

        Assert.true(create_tag_pg.is_multiselect_widget_visible,
                    'multiselect widget should be visible after product was selected')

        create_tag_pg.save_tag()
        manage_tags_pg.filter_form.filter_by(lookup='name', value=tag['name'])
        displayed_tags = manage_tags_pg.tags()

        Assert.true(tag['name'] in [t.name for t in displayed_tags],
                    'tag with "%s" name is not displayed on the page' % tag['name'])

    def test_creating_a_tag_with_a_product_value_and_cases(self, mozwebqa_logged_in, product):
        # create some cases for product
        cases = self.create_bulk_cases(mozwebqa_logged_in, product, use_API=True)
        manage_tags_pg = MozTrapManageTagsPage(mozwebqa_logged_in)
        manage_tags_pg.go_to_manage_tags_page()

        create_tag_pg = manage_tags_pg.click_create_tag_button()
        tag = MockTag(product=product['name'])
        create_tag_pg.create_tag(tag, save_tag=False)

        expected_case_names = [case.name for case in cases]
        actual_case_names = [case.name for case in create_tag_pg.available_caseversions]

        Assert.equal(sorted(expected_case_names), sorted(actual_case_names),
                     'list of expected caseversions differs from actually displayed')

        create_tag_pg.include_caseversions_to_tag(expected_case_names)

        manage_cases_page = MozTrapManageCasesPage(mozwebqa_logged_in)
        manage_cases_page.go_to_manage_cases_page()
        manage_cases_page.filter_form.filter_by(lookup='tag', value=tag['name'])

        displayed_case_names = [case.name for case in manage_cases_page.test_cases]

        Assert.equal(sorted(expected_case_names), sorted(displayed_case_names),
                     'list of test cases attached to a tag differs from expected')
