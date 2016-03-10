# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.home_page import MozTrapHomePage
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
from mocks.mock_suite import MockSuite
from mocks.mock_case import MockCase


class BaseTest(object):
    '''
    Base class for all Tests
    '''

    def create_product(self, base_url, selenium, profile=None):
        create_product_pg = MozTrapCreateProductPage(base_url, selenium)

        create_product_pg.go_to_create_product_page()
        product = create_product_pg.create_product(profile=profile)

        return product

    def delete_product(self, base_url, selenium, product):
        manage_products_pg = MozTrapManageProductsPage(base_url, selenium)

        manage_products_pg.go_to_manage_products_page()
        manage_products_pg.filter_form.filter_by(lookup='name', value=product['name'])
        manage_products_pg.delete_product(name=product['name'])

    def create_version(self, base_url, selenium, product):
        create_version_pg = MozTrapCreateVersionPage(base_url, selenium)

        create_version_pg.go_to_create_version_page()
        version = create_version_pg.create_version(product_name=product['name'])

        version['product'] = product

        return version

    def delete_version(self, base_url, selenium, version):
        manage_versions_pg = MozTrapManageVersionsPage(base_url, selenium)

        manage_versions_pg.go_to_manage_versions_page()
        manage_versions_pg.filter_form.filter_by(lookup='version', value=version['name'])
        manage_versions_pg.delete_version(name=version['name'], product_name=version['product']['name'])

    def create_run(self, base_url, selenium, product, activate=False, version=None, suite_name_list=None):
        create_run_pg = MozTrapCreateRunPage(base_url, selenium)

        if version is None:
            version = self.create_version(base_url, selenium, product=product)

        create_run_pg.go_to_create_run_page()
        product_version = u'%(product_name)s %(version_name)s' % {'product_name': product['name'], 'version_name': version['name']}
        run = create_run_pg.create_run(product_version=product_version, suite_list=suite_name_list)
        run['version'] = version

        if activate:
            manage_runs_pg = MozTrapManageRunsPage(base_url, selenium)
            manage_runs_pg.filter_form.filter_by(lookup='name', value=run['name'])
            manage_runs_pg.activate_run(name=run['name'])

        return run

    def delete_run(self, base_url, selenium, run, delete_version=False):
        manage_runs_pg = MozTrapManageRunsPage(base_url, selenium)

        manage_runs_pg.go_to_manage_runs_page()
        manage_runs_pg.filter_form.filter_by(lookup='name', value=run['name'])
        manage_runs_pg.delete_run(name=run['name'])

        if delete_version:
            self.delete_version(base_url, selenium, version=run['version'])

    def create_suite(self, base_url, selenium, product, api=None, status='active', case_list=[], **kwargs):
        if api is not None:
            suite = MockSuite()
            api.create_suite(suite, product, case_list)
        else:
            create_suite_pg = MozTrapCreateSuitePage(base_url, selenium)
            create_suite_pg.go_to_create_suite_page()
            suite = create_suite_pg.create_suite(product=product['name'], status=status, case_list=case_list, **kwargs)
            suite['product'] = product
        return suite

    def delete_suite(self, base_url, selenium, suite):
        manage_suites_pg = MozTrapManageSuitesPage(base_url, selenium)

        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])
        manage_suites_pg.delete_suite(name=suite['name'])

    def create_case(self, base_url, selenium, product, api=None, mock_case=None):
        if api is not None:
            case = MockCase()
            api.create_case(case, product)
        else:
            mock_case = mock_case or MockCase()
            mock_case['product'] = product
            mock_case['version'] = product['version']

            create_case_pg = MozTrapCreateCasePage(base_url, selenium)
            create_case_pg.go_to_create_case_page()
            case = create_case_pg.create_case(mock_case)

        return case

    def delete_case(self, base_url, selenium, case):
        manage_cases_pg = MozTrapManageCasesPage(base_url, selenium)

        manage_cases_pg.go_to_manage_cases_page()
        manage_cases_pg.filter_form.filter_by(lookup='name', value=case['name'])
        manage_cases_pg.delete_case(name=case['name'])

    def create_profile(self, base_url, selenium):
        create_profile_pg = MozTrapCreateProfilePage(base_url, selenium)

        create_profile_pg.go_to_create_profile_page()
        profile = create_profile_pg.create_profile()

        return profile

    def delete_profile(self, base_url, selenium, profile):
        create_profile_pg = MozTrapCreateProfilePage(base_url, selenium)
        manage_profiles_pg = MozTrapManageProfilesPage(base_url, selenium)

        manage_profiles_pg.go_to_manage_profiles_page()
        manage_profiles_pg.filter_form.filter_by(lookup='name', value=profile['name'])
        manage_profiles_pg.delete_profile(name=profile['name'])
        create_profile_pg.go_to_create_profile_page()
        create_profile_pg.delete_environment_category(category_name=profile['category'])

    def create_and_run_test(self, api, base_url, selenium, product, element):
        home_pg = MozTrapHomePage(base_url, selenium)

        self.connect_product_to_element(base_url, selenium, product, element)
        case = self.create_case(base_url, selenium, product, api=api)
        suite = self.create_suite(base_url, selenium, product=product, api=api, case_list=[case])
        run = self.create_run(base_url, selenium, activate=True, product=product, version=product['version'], suite_name_list=[suite['name']])

        home_pg.go_to_home_page()
        home_pg.go_to_run_test(product_name=product['name'], version_name=product['version']['name'], run_name=run['name'], env_category_name=element['category']['name'], env_element_name=element['name'])

        return case, suite, run

    def create_bulk_cases(self, base_url, selenium, product, api=None, cases_amount=2, status='active', version=None, suite_name=None, **kwargs):
        if api is not None:
            cases = []
            for i in xrange(cases_amount):
                case = MockCase()
                if 'name' in kwargs:
                    case['name'] = kwargs['name']
                api.create_case(case, product)
                cases.append(case)
        else:
            create_bulk_cases_pg = MozTrapCreateBulkCasesPage(base_url, selenium)

            if version is None:
                version = product['version']

            create_bulk_cases_pg.go_to_create_bulk_cases_page()
            cases = create_bulk_cases_pg.create_bulk_cases(
                product=product['name'], version=version['name'], status=status,
                suite=suite_name, cases_amount=cases_amount, **kwargs)

            # add product to dictionary to ensure that output of this method
            # is similar to create_case method
            for case in cases:
                case['product'] = product

        return cases

    def connect_product_to_element(self, base_url, selenium, product, element):
        manage_versions_pg = MozTrapManageVersionsPage(base_url, selenium)

        manage_versions_pg.go_to_manage_versions_page()
        manage_versions_pg.filter_form.filter_by(lookup='version', value=product['version']['name'])
        manage_environments_pg = manage_versions_pg.select_environments()
        manage_environments_pg.add_element_to_environment(element)
