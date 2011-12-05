#!/usr/bin/env python
#
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Case Conductor
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Jonny Gerig Meyer <jonny@oddbird.net>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from create_case_page import CaseConductorCreateCasePage
from manage_cases_page import CaseConductorManageCasesPage
from create_suite_page import CaseConductorCreateSuitePage
from manage_suites_page import CaseConductorManageSuitesPage
from create_run_page import CaseConductorCreateRunPage
from manage_runs_page import CaseConductorManageRunsPage
from create_cycle_page import CaseConductorCreateCyclePage
from manage_cycles_page import CaseConductorManageCyclesPage
from create_product_page import CaseConductorCreateProductPage
from manage_products_page import CaseConductorManageProductsPage


class BaseTest(object):
    '''
    Base class for all Tests
    '''

    def create_product(self, mozwebqa, login=False):
        create_product_pg = CaseConductorCreateProductPage(mozwebqa)

        create_product_pg.go_to_create_product_page(login=login)
        product = create_product_pg.create_product()

        return product

    def delete_product(self, mozwebqa, product):
        manage_products_pg = CaseConductorManageProductsPage(mozwebqa)

        manage_products_pg.go_to_manage_products_page()
        manage_products_pg.filter_products_by_name(name=product['name'])
        manage_products_pg.delete_product(name=product['name'])

    def create_cycle(self, mozwebqa, product=None, login=False):
        create_cycle_pg = CaseConductorCreateCyclePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa, login=login)
            login = False

        create_cycle_pg.go_to_create_cycle_page(login=login)
        cycle = create_cycle_pg.create_cycle(product=product['name'])
        cycle['product'] = product

        return cycle

    def delete_cycle(self, mozwebqa, cycle, delete_product=False):
        manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa)

        manage_cycles_pg.go_to_manage_cycles_page()
        manage_cycles_pg.filter_cycles_by_name(name=cycle['name'])
        manage_cycles_pg.delete_cycle(name=cycle['name'])

        if delete_product:
            self.delete_product(mozwebqa, cycle['product'])

    def create_run(self, mozwebqa, cycle=None, login=False):
        create_run_pg = CaseConductorCreateRunPage(mozwebqa)

        if cycle is None:
            cycle = self.create_cycle(mozwebqa, login=login)
            login = False

        create_run_pg.go_to_create_run_page(login=login)
        run = create_run_pg.create_run(cycle=cycle['name'])
        run['cycle'] = cycle

        return run

    def delete_run(self, mozwebqa, run, delete_cycle=False, delete_product=False):
        manage_runs_pg = CaseConductorManageRunsPage(mozwebqa)

        manage_runs_pg.go_to_manage_runs_page()
        manage_runs_pg.filter_runs_by_name(name=run['name'])
        manage_runs_pg.delete_run(name=run['name'])

        if delete_cycle:
            self.delete_cycle(mozwebqa, run['cycle'], delete_product=delete_product)

    def create_suite(self, mozwebqa, product=None, login=False):
        create_suite_pg = CaseConductorCreateSuitePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa, login=login)
            login = False

        create_suite_pg.go_to_create_suite_page(login=login)
        suite = create_suite_pg.create_suite(product=product['name'])
        suite['product'] = product

        return suite

    def delete_suite(self, mozwebqa, suite, delete_product=False):
        manage_suites_pg = CaseConductorManageSuitesPage(mozwebqa)

        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_suites_by_name(name=suite['name'])
        manage_suites_pg.delete_suite(name=suite['name'])

        if delete_product:
            self.delete_product(mozwebqa, suite['product'])

    def create_case(self, mozwebqa, product=None, login=False):
        create_case_pg = CaseConductorCreateCasePage(mozwebqa)

        if product is None:
            product = self.create_product(mozwebqa, login=login)
            login = False

        create_case_pg.go_to_create_case_page(login=login)
        case = create_case_pg.create_case(product=product['name'])
        case['product'] = product

        return case

    def delete_case(self, mozwebqa, case, delete_product=False):
        manage_cases_pg = CaseConductorManageCasesPage(mozwebqa)

        manage_cases_pg.go_to_manage_cases_page()
        manage_cases_pg.filter_cases_by_name(name=case['name'])
        manage_cases_pg.delete_case(name=case['name'])

        if delete_product:
            self.delete_product(mozwebqa, case['product'])
