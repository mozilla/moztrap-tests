#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from unittestzero import Assert
import requests


class MoztrapAPI:

    def __init__(self, username, api_key, base_url):
        self.params = {
            u'username': unicode(username),
            u'api_key': unicode(api_key),
            u'format': u'json',
        }
        self.base_url = base_url
        self.headers = {"content-type": "application/json"}

    def _do_post(self, uri, post_data):
        """Post to an API method and return the resulting id."""
        response = requests.post(
            "%s/%s" % (self.base_url, uri),
            params=self.params,
            data=json.dumps(post_data),
            headers=self.headers)
        response.raise_for_status()
        text = json.loads(response.text)

        if response.status_code == 201:
            return text['id']
        else:
            print "Failed to create resource: %s with %s.\n%s" % (
                post_data, response.status_code, response.text)
            return None

    def _do_delete(self, uri, id):
        """Delete to an API method and return True or False."""
        response = requests.delete(
            "%s/%s/%s" % (self.base_url, uri, id),
            params=self.params,
            headers=self.headers)
        response.raise_for_status()
        if response.status_code == 204:
            return True
        else:
            print "Failed to delete resource: %s with %s.\n%s" % (
                id, response.status_code, response.text)
            return False

    def create_product(self, product):

        uri = "api/v1/product/"
        post_data = {
            u'name': unicode(product['name']),
            u'description': unicode(product['description']),
            u'productversions': [{u'version': unicode(product['version']['name'])}]
        }
        product['id'] = self._do_post(uri, post_data)

        Assert.greater(product['id'], 0, 'No product was created.')

    def delete_product(self, product):

        uri = "api/v1/product"
        self.params['permanent'] = True
        Assert.true(self._do_delete(uri, product['id']), 'Deletion of product %s failed' % product['name'])

    def create_category(self, category):

        uri = "api/v1/category/"
        post_data = {
            u'name': unicode(category['name'])
        }
        category['id'] = self._do_post(uri, post_data)

        Assert.greater(category['id'], 0, 'No category was created.')

    def delete_category(self, category):

        uri = "api/v1/category"
        self.params['permanent'] = True
        Assert.true(self._do_delete(uri, category['id']), 'Deletion of product %s failed' % category['name'])

    def create_element(self, element):

        category = element['category']
        if category['id'] is None:
            self.create_category(category)

        uri = "api/v1/element/"
        post_data = {
            u'name': unicode(element['name']),
            u'category': unicode('/%s' % element['category'].uri)
        }
        element['id'] = self._do_post(uri, post_data)

        Assert.greater(element['id'], 0, 'No element was created.')

    def delete_element(self, element):

        uri = "api/v1/element"
        self.params['permanent'] = True
        Assert.true(self._do_delete(uri, element['id']), 'Deletion of product %s failed' % element['name'])

    def create_suite(self, suite, product):

        uri = "api/v1/suite/"
        post_data = {
            u'name': unicode(suite['name']),
            u'product': unicode('/%s' % product.uri)
        }
        suite['id'] = self._do_post(uri, post_data)

        Assert.greater(suite['id'], 0, 'No suite was created.')
