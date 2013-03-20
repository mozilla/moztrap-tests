#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from unittestzero import Assert
import requests


class MoztrapAPI:

    def __init__(self, mozwebqa):
        user = mozwebqa.credentials['default']
        self.params = {
            u'username': unicode(user['name']),
            u'api_key': unicode(user['api_key']),
            u'format': u'json',
        }
        self.base_url = mozwebqa.base_url
        self.headers = {"content-type": "application/json"}

    def _do_post(self, uri, post_data):
        response = requests.post(
            "%s/%s" % (self.base_url, uri),
            params=self.params,
            data=json.dumps(post_data),
            headers=self.headers)
        response.raise_for_status()
        return response

    def _do_delete(self, uri, id):
        response = requests.delete(
            "%s/%s/%s" % (self.base_url, uri, id),
            params=self.params,
            headers=self.headers)
        response.raise_for_status()
        return response

    def create_product(self, product, profile=None):

        uri = "api/v1/product/"
        post_data = {
            u'name': unicode(product['name']),
            u'description': unicode(product['description']),
            u'productversions': [{u'version': unicode(product['version']['name'])}]
        }
        response = self._do_post(uri, post_data)
        text = json.loads(response.text)

        if response.status_code == 201:
            print "Created product %s." % post_data['name']
            product['id'] = text['id']
        else:
            print "Failed to create %s with %s.\n%s" % (
                post_data['name'], response.status_code, response.text)

        Assert.greater(product['id'], 0, 'No product was created.')
        return product

    def delete_product(self, product):

        uri = "api/v1/product"
        self.params['permanent'] = True
        response = self._do_delete(uri, product['id'])
        if response.status_code == 204:
            print "Deleted product %s." % product['name']
        else:
            print "Failed to delete %s with %s.\n%s" % (
                product['name'], response.status_code, response.text)
