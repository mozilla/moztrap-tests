#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from pages.create_product_page import MozTrapCreateProductPage


class MockProduct(dict):

    def __init__(self, mozwebqa, name='Test Product', version='Test Version', description='This is a test product', profile=None):

        # we need the MozTrapCreateProductPage in order to get the locators
        create_product_page = MozTrapCreateProductPage(mozwebqa)

        dt_string = datetime.utcnow().isoformat()
        self['id'] = None
        self['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        self['description'] = u'%(desc)s created on %(dt_string)s' % {'desc': description, 'dt_string': dt_string}
        self['locator'] = (create_product_page._product_locator[0], create_product_page._product_locator[1] % {'product_name': self['name']})
        self['version'] = {}
        self['version']['name'] = u'%(version)s %(dt_string)s' % {'version': version, 'dt_string': dt_string}
        self['version']['manage_locator'] = (create_product_page._version_manage_locator[0], create_product_page._version_manage_locator[1] % {'product_name': self['name'], 'version_name': self['version']['name']})
        self['version']['homepage_locator'] = (create_product_page._version_homepage_locator[0], create_product_page._version_homepage_locator[1] % {'product_name': self['name'], 'version_name': self['version']['name']})
        self['profile'] = profile

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
