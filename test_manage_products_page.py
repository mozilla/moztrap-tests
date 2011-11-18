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

from create_product_page import CaseConductorCreateProductPage
from manage_products_page import CaseConductorManageProductsPage
from unittestzero import Assert


class TestManageProductsPage:

    def test_that_user_can_create_and_delete_product(self, mozwebqa):
        manage_products_pg = CaseConductorManageProductsPage(mozwebqa)
        create_product_pg = CaseConductorCreateProductPage(mozwebqa)

        create_product_pg.go_to_create_product_page(login=True)

        product = create_product_pg.create_product()

        manage_products_pg.filter_products_by_name(name=product['name'])

        Assert.true(manage_products_pg.is_element_present(product['locator']))

        manage_products_pg.delete_product(name=product['name'])

        Assert.false(manage_products_pg.is_element_present(product['locator']))

    def test_that_user_can_filter_product_by_name(self, mozwebqa):
        manage_products_pg = CaseConductorManageProductsPage(mozwebqa)
        create_product_pg = CaseConductorCreateProductPage(mozwebqa)

        create_product_pg.go_to_create_product_page(login=True)

        product = create_product_pg.create_product()

        manage_products_pg.filter_products_by_name(name='Another Product')

        Assert.false(manage_products_pg.is_element_present(product['locator']))

        manage_products_pg.remove_name_filter(name='Another Product')
        manage_products_pg.filter_products_by_name(name=product['name'])

        Assert.true(manage_products_pg.is_element_present(product['locator']))

        manage_products_pg.delete_product(name=product['name'])

    def test_that_user_can_filter_product_by_name_without_mouse(self, mozwebqa):
        manage_products_pg = CaseConductorManageProductsPage(mozwebqa)
        create_product_pg = CaseConductorCreateProductPage(mozwebqa)

        create_product_pg.go_to_create_product_page(login=True)

        product = create_product_pg.create_product()

        manage_products_pg.filter_products_by_name_without_mouse(name='Another Product')

        Assert.false(manage_products_pg.is_element_present(product['locator']))

        manage_products_pg.remove_name_filter(name='Another Product')
        manage_products_pg.filter_products_by_name_without_mouse(name=product['name'])

        Assert.true(manage_products_pg.is_element_present(product['locator']))

        manage_products_pg.delete_product(name=product['name'])
