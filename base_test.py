#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from home_page import CaseConductorHomePage
from run_tests_page import CaseConductorRunTestsPage
from create_case_page import CaseConductorCreateCasePage
from manage_cases_page import CaseConductorManageCasesPage
from create_suite_page import CaseConductorCreateSuitePage
from manage_suites_page import CaseConductorManageSuitesPage
from create_run_page import CaseConductorCreateRunPage
from manage_runs_page import CaseConductorManageRunsPage
from create_version_page import CaseConductorCreateVersionPage
from manage_versions_page import CaseConductorManageVersionsPage
from create_product_page import CaseConductorCreateProductPage
from manage_products_page import CaseConductorManageProductsPage


class BaseTest(object):
    '''
    Base class for all Tests
    '''

    def create_product(self, mozwebqa):
        create_product_pg = CaseConductorCreateProductPage(mozwebqa)

        create_product_pg.go_to_create_product_page()
        product = create_product_pg.create_product()

        return product

    def delete_product(self, mozwebqa, product):
        manage_products_pg = CaseConductorManageProductsPage(mozwebqa)

        manage_products_pg.go_to_manage_products_page()
        manage_products_pg.filter_products_by_name(name=product['name'])
        manage_products_pg.delete_product(name=product['name'])

    def create_version(self, mozwebqa, product=None):
        create_version_pg = CaseConductorCreateVersionPage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)
            version = product['version']
            manage_versions_pg = CaseConductorManageVersionsPage(mozwebqa)
            manage_versions_pg.go_to_manage_versions_page()
        else:
            create_version_pg.go_to_create_version_page()
            version = create_version_pg.create_version(product_name=product['name'])

        version['product'] = product

        return version

    def delete_version(self, mozwebqa, version, delete_product=False):
        manage_versions_pg = CaseConductorManageVersionsPage(mozwebqa)

        manage_versions_pg.go_to_manage_versions_page()
        manage_versions_pg.filter_versions_by_name(name=version['name'])
        manage_versions_pg.delete_version(name=version['name'], product_name=version['product']['name'])

        if delete_product:
            self.delete_product(mozwebqa, product=version['product'])

    def create_run(self, mozwebqa, activate=False, version=None, suite_name_list=None):
        create_run_pg = CaseConductorCreateRunPage(mozwebqa)

        if version is None:
            version = self.create_version(mozwebqa)

        create_run_pg.go_to_create_run_page()
        product_version = u'%(product_name)s %(version_name)s' % {'product_name': version['product']['name'], 'version_name': version['name']}
        run = create_run_pg.create_run(product_version=product_version, suite_list=suite_name_list)
        run['version'] = version

        if activate:
            manage_runs_pg = CaseConductorManageRunsPage(mozwebqa)
            manage_runs_pg.filter_runs_by_name(name=run['name'])
            manage_runs_pg.activate_run(name=run['name'])

        return run

    def delete_run(self, mozwebqa, run, delete_version=False, delete_product=False):
        manage_runs_pg = CaseConductorManageRunsPage(mozwebqa)

        manage_runs_pg.go_to_manage_runs_page()
        manage_runs_pg.filter_runs_by_name(name=run['name'])
        manage_runs_pg.delete_run(name=run['name'])

        if delete_version:
            self.delete_version(mozwebqa, version=run['version'], delete_product=delete_product)

    def create_suite(self, mozwebqa, status='active', product=None, case_name_list=None):
        create_suite_pg = CaseConductorCreateSuitePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)

        create_suite_pg.go_to_create_suite_page()
        suite = create_suite_pg.create_suite(product=product['name'], status=status, case_list=case_name_list)
        suite['product'] = product

        return suite

    def delete_suite(self, mozwebqa, suite, delete_product=False):
        manage_suites_pg = CaseConductorManageSuitesPage(mozwebqa)

        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_suites_by_name(name=suite['name'])
        manage_suites_pg.delete_suite(name=suite['name'])

        if delete_product:
            self.delete_product(mozwebqa, product=suite['product'])

    def create_case(self, mozwebqa, activate=False, product=None, suite_name=None):
        create_case_pg = CaseConductorCreateCasePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa)

        create_case_pg.go_to_create_case_page()
        case = create_case_pg.create_case(product=product['name'], suite=suite_name)
        case['product'] = product

        if activate:
            manage_cases_pg = CaseConductorManageCasesPage(mozwebqa)
            manage_cases_pg.filter_cases_by_name(name=case['name'])
            manage_cases_pg.activate_case(name=case['name'])

        return case

    def delete_case(self, mozwebqa, case, delete_product=False):
        manage_cases_pg = CaseConductorManageCasesPage(mozwebqa)

        manage_cases_pg.go_to_manage_cases_page()
        manage_cases_pg.filter_cases_by_name(name=case['name'])
        manage_cases_pg.delete_case(name=case['name'])

        if delete_product:
            self.delete_product(mozwebqa, case['product'])

    def create_and_run_test(self, mozwebqa):
        home_pg = CaseConductorHomePage(mozwebqa)
        manage_suites_pg = CaseConductorManageSuitesPage(mozwebqa)
        run_tests_pg = CaseConductorRunTestsPage(mozwebqa)

        suite = self.create_suite(mozwebqa)
        case = self.create_case(mozwebqa, activate=True, product=suite['product'], suite_name=suite['name'])

        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_suites_by_name(name=suite['name'])
        manage_suites_pg.activate_suite(name=suite['name'])

        cycle = self.create_cycle(mozwebqa, activate=True, product=suite['product'])
        run = self.create_run(mozwebqa, activate=True, cycle=cycle, suite_name=suite['name'])

        home_pg.go_to_homepage_page()
        home_pg.go_to_run_test(product_name=run['cycle']['product']['name'], cycle_name=run['cycle']['name'], run_name=run['name'])

        return case
