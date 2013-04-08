#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from unittestzero import Assert
import requests


class MoztrapAPI:

    def __init__(self, credentials, base_url):
        user = credentials['default']
        self.params = {
            u'username': unicode(user['username']),
            u'api_key': unicode(user['api_key']),
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

    def create_product(self, product, profile=None):

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
