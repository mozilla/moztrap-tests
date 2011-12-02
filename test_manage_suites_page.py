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

from create_suite_page import CaseConductorCreateSuitePage
from manage_suites_page import CaseConductorManageSuitesPage
from create_product_page import CaseConductorCreateProductPage
from manage_products_page import CaseConductorManageProductsPage
from unittestzero import Assert


class TestManageSuitesPage:

    def create_product(self, mozwebqa):
        create_product_pg = CaseConductorCreateProductPage(mozwebqa)

        create_product_pg.go_to_create_product_page(login=True)
        product = create_product_pg.create_product()

        return product

    def delete_product(self, product, mozwebqa):
        manage_products_pg = CaseConductorManageProductsPage(mozwebqa)

        manage_products_pg.go_to_manage_products_page()
        manage_products_pg.filter_products_by_name(name=product['name'])
        manage_products_pg.delete_product(name=product['name'])

    def test_that_user_can_create_and_delete_suite(self, mozwebqa):
        manage_suites_pg = CaseConductorManageSuitesPage(mozwebqa)
        create_suite_pg = CaseConductorCreateSuitePage(mozwebqa)

        product = self.create_product(mozwebqa)

        create_suite_pg.go_to_create_suite_page()

        suite = create_suite_pg.create_suite(product=product['name'])

        manage_suites_pg.filter_suites_by_name(name=suite['name'])

        Assert.true(manage_suites_pg.is_element_present(suite['locator']))

        manage_suites_pg.delete_suite(name=suite['name'])

        Assert.false(manage_suites_pg.is_element_present(suite['locator']))

        self.delete_product(product, mozwebqa)
