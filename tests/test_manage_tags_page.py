#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert

from mocks.mock_tag import MockTag
from pages.base_test import BaseTest
from pages.manage_tags_page import MozTrapManageTagsPage


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
