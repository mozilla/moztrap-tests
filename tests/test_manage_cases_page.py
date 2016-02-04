# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from mocks.mock_case import MockCase
from mocks.mock_tag import MockTag
from pages.base_test import BaseTest
from pages.manage_cases_page import MozTrapManageCasesPage


class TestManageCasesPage(BaseTest):

    @pytest.mark.moztrap([142, 137])
    def test_that_user_can_create_and_delete_case(self, mozwebqa, login, product):
        manage_cases_pg = MozTrapManageCasesPage(mozwebqa)

        case = self.create_case(mozwebqa, product)

        manage_cases_pg.filter_form.filter_by(lookup='name', value=case['name'])

        assert manage_cases_pg.is_element_present(*case['locator'])

        manage_cases_pg.delete_case(name=case['name'])

        assert not manage_cases_pg.is_element_present(*case['locator'])

    def test_that_deleting_single_version_of_case_does_not_delete_all_versions(self, api, mozwebqa, login, product):
        # prerequisites
        test_case = self.create_case(mozwebqa, product=product, api=api)

        first_version = product['version']
        second_version = self.create_version(mozwebqa, product=product)
        product_versions = [u'%s %s' % (product['name'], version['name'])
                            for version in (first_version, second_version)]

        manage_cases_pg = MozTrapManageCasesPage(mozwebqa)
        manage_cases_pg.go_to_manage_cases_page()
        filter_item = manage_cases_pg.filter_form.filter_by(lookup='product', value=product['name'])
        test_cases = manage_cases_pg.test_cases

        # remember case version and delete case
        deleted_version = test_cases[0].product_version
        product_versions.remove(deleted_version)
        test_cases[0].delete()

        filter_item.remove_filter()
        manage_cases_pg.filter_form.filter_by(lookup='name', value=test_case['name'])
        test_cases = manage_cases_pg.test_cases

        # check that there is only one test case left and ensure its version equals to second version
        assert 1 == len(test_cases)
        assert test_case['name'] == test_cases[0].name
        assert product_versions[0] == test_cases[0].product_version

    def test_that_manage_cases_list_shows_all_case_versions_individually(self, api, mozwebqa, login, product):
        # prerequisites
        test_case = self.create_case(mozwebqa, product=product, api=api)
        first_version = product['version']
        second_version = self.create_version(mozwebqa, product=product)
        product_versions = [u'%s %s' % (product['name'], version['name'])
                            for version in (first_version, second_version)]

        manage_cases_pg = MozTrapManageCasesPage(mozwebqa)
        manage_cases_pg.go_to_manage_cases_page()
        manage_cases_pg.filter_form.filter_by(lookup='name', value=test_case['name'])
        filtered_cases = manage_cases_pg.test_cases

        for case in filtered_cases:
            assert test_case['name'] == case.name

        # check that both product versions are displayed
        assert sorted(product_versions) == sorted([case.product_version for case in filtered_cases])

    def test_that_creates_tag_during_test_case_creation(self, mozwebqa, login, product):
        mock_tag = MockTag()
        mock_case = MockCase(tag=mock_tag)
        test_case = self.create_case(mozwebqa, product=product, mock_case=mock_case)

        manage_cases_pg = MozTrapManageCasesPage(mozwebqa)
        manage_cases_pg.filter_form.filter_by(lookup='name', value=test_case['name'])
        filtered_cases = manage_cases_pg.test_cases

        assert 1 == len(filtered_cases)
        assert mock_tag['name'].lower() == filtered_cases[0].tag_name
