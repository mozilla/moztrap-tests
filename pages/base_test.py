#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import json

from mocks.mock_product import MockProduct
from mocks.moztrap_api import MoztrapAPI
from pages.home_page import MozTrapHomePage
from pages.run_tests_page import MozTrapRunTestsPage
from pages.create_case_page import MozTrapCreateCasePage
from pages.manage_cases_page import MozTrapManageCasesPage
from pages.create_suite_page import MozTrapCreateSuitePage
from pages.manage_suites_page import MozTrapManageSuitesPage
from pages.create_run_page import MozTrapCreateRunPage
from pages.manage_runs_page import MozTrapManageRunsPage
from pages.create_version_page import MozTrapCreateVersionPage
from pages.manage_versions_page import MozTrapManageVersionsPage
from pages.create_product_page import MozTrapCreateProductPage
from pages.manage_products_page import MozTrapManageProductsPage
from pages.create_profile_page import MozTrapCreateProfilePage
from pages.manage_profiles_page import MozTrapManageProfilesPage
from pages.create_bulk_cases_page import MozTrapCreateBulkCasesPage


class BaseTest(object):
    '''
    Base class for all Tests
    '''

    def create_product_via_API(self, mozwebqa, profile=None):

        api = MoztrapAPI(mozwebqa)
        product = MockProduct(mozwebqa)
        product = api.create_product(product)
        mozwebqa.product = product
        return product

    def create_product(self, mozwebqa, profile=None):
        create_product_pg = MozTrapCreateProductPage(mozwebqa)

        create_product_pg.go_to_create_product_page()
        product = create_product_pg.create_product(profile=profile)

        return product

    def delete_product(self, mozwebqa, product):
        manage_products_pg = MozTrapManageProductsPage(mozwebqa)

        manage_products_pg.go_to_manage_products_page()
        manage_products_pg.filter_form.filter_by(lookup='name', value=product['name'])
        manage_products_pg.delete_product(name=product['name'])

    def create_version(self, mozwebqa, product=None):
        create_version_pg = MozTrapCreateVersionPage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)
            version = product['version']
            manage_versions_pg = MozTrapManageVersionsPage(mozwebqa)
            manage_versions_pg.go_to_manage_versions_page()
        else:
            create_version_pg.go_to_create_version_page()
            version = create_version_pg.create_version(product_name=product['name'])

        version['product'] = product

        return version

    def delete_version(self, mozwebqa, version, delete_product=False):
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa)

        manage_versions_pg.go_to_manage_versions_page()
        manage_versions_pg.filter_form.filter_by(lookup='version', value=version['name'])
        manage_versions_pg.delete_version(name=version['name'], product_name=version['product']['name'])

        if delete_product:
            self.delete_product(mozwebqa, product=version['product'])

    def create_run(self, mozwebqa, activate=False, product=None, version=None, suite_name_list=None):
        create_run_pg = MozTrapCreateRunPage(mozwebqa)

        if version is None:
            version = self.create_version(mozwebqa, product=product)
        if product is None:
            product = version['product']

        create_run_pg.go_to_create_run_page()
        product_version = u'%(product_name)s %(version_name)s' % {'product_name': product['name'], 'version_name': version['name']}
        run = create_run_pg.create_run(product_version=product_version, suite_list=suite_name_list)
        run['version'] = version

        if activate:
            manage_runs_pg = MozTrapManageRunsPage(mozwebqa)
            manage_runs_pg.filter_form.filter_by(lookup='name', value=run['name'])
            manage_runs_pg.activate_run(name=run['name'])

        return run

    def delete_run(self, mozwebqa, run, delete_version=False, delete_product=False):
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa)

        manage_runs_pg.go_to_manage_runs_page()
        manage_runs_pg.filter_form.filter_by(lookup='name', value=run['name'])
        manage_runs_pg.delete_run(name=run['name'])

        if delete_version:
            self.delete_version(mozwebqa, version=run['version'], delete_product=delete_product)

    def create_suite(self, mozwebqa, status='active', product=None, case_name_list=None, **kwargs):
        create_suite_pg = MozTrapCreateSuitePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)

        create_suite_pg.go_to_create_suite_page()
        suite = create_suite_pg.create_suite(product=product['name'], status=status, case_list=case_name_list, **kwargs)
        suite['product'] = product

        return suite

    def delete_suite(self, mozwebqa, suite, delete_product=False):
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa)

        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])
        manage_suites_pg.delete_suite(name=suite['name'])

        if delete_product:
            self.delete_product(mozwebqa, product=suite['product'])

    def create_case(self, mozwebqa, status='active', product=None, version=None, suite_name=None):
        create_case_pg = MozTrapCreateCasePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)
            version = product['version']
        elif version is None:
            version = product['version']

        create_case_pg.go_to_create_case_page()
        case = create_case_pg.create_case(product=product['name'], version=version['name'], status=status, suite=suite_name)
        case['product'] = product

        return case

    def delete_case(self, mozwebqa, case, delete_product=False):
        manage_cases_pg = MozTrapManageCasesPage(mozwebqa)

        manage_cases_pg.go_to_manage_cases_page()
        manage_cases_pg.filter_form.filter_by(lookup='name', value=case['name'])
        manage_cases_pg.delete_case(name=case['name'])

        if delete_product:
            self.delete_product(mozwebqa, product=case['product'])

    def create_profile(self, mozwebqa):
        create_profile_pg = MozTrapCreateProfilePage(mozwebqa)

        create_profile_pg.go_to_create_profile_page()
        profile = create_profile_pg.create_profile()

        return profile

    def delete_profile(self, mozwebqa, profile):
        create_profile_pg = MozTrapCreateProfilePage(mozwebqa)
        manage_profiles_pg = MozTrapManageProfilesPage(mozwebqa)

        manage_profiles_pg.go_to_manage_profiles_page()
        manage_profiles_pg.filter_form.filter_by(lookup='name', value=profile['name'])
        manage_profiles_pg.delete_profile(name=profile['name'])
        create_profile_pg.go_to_create_profile_page()
        create_profile_pg.delete_environment_category(category_name=profile['category'])

    def create_and_run_test(self, mozwebqa, profile=None):
        home_pg = MozTrapHomePage(mozwebqa)
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa)
        run_tests_pg = MozTrapRunTestsPage(mozwebqa)

        if profile is None:
            profile = self.create_profile(mozwebqa)

        product = self.create_product(mozwebqa, profile=profile['name'])
        suite = self.create_suite(mozwebqa, product=product)
        case = self.create_case(mozwebqa, product=product, version=product['version'], suite_name=suite['name'])
        case['profile'] = profile
        run = self.create_run(mozwebqa, activate=True, product=product, version=product['version'], suite_name_list=[suite['name']])

        home_pg.go_to_home_page()
        home_pg.go_to_run_test(product_name=product['name'], version_name=product['version']['name'], run_name=run['name'], env_category=profile['category'], env_element=profile['element'])

        return case

    def create_bulk_cases(self, mozwebqa, cases_amount=2, status='active', product=None, version=None, suite_name=None, **kwargs):
        create_bulk_cases_pg = MozTrapCreateBulkCasesPage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)
            version = product['version']
        elif version is None:
            version = product['version']

        create_bulk_cases_pg.go_to_create_bulk_cases_page()
        cases = create_bulk_cases_pg.create_bulk_cases(
            product=product['name'], version=version['name'], status=status,
            suite=suite_name, cases_amount=cases_amount, **kwargs)

        #add product to dictionary to ensure that output of this method
        #is similar to create_case method
        for case in cases:
            case['product'] = product

        return cases
