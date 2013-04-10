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

    def _do_get(self, uri, get_params):
        """Get to an API method and return the resulting content."""
        get_params.update(self.params)
        response = requests.get(
            "%s/%s" % (self.base_url, uri),
            params=get_params,
            headers=self.headers)
        response.raise_for_status()
        text = json.loads(response.text)
        objects = text["objects"]
        return objects

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

    def get_profile(self, name):

        uri = "api/v1/profile/"
        get_params = {
            u'name': unicode(name)
        }
        profile = self._do_get(uri, get_params)

        Assert.greater(profile['id'], 0, 'No profile was created.')

    def create_profile(self, profile):

        uri = "api/v1/profile/"
        post_data = {
            u'name': unicode(profile['name'])
        }
        profile['id'] = self._do_post(uri, post_data)

        Assert.greater(profile['id'], 0, 'No profile was created.')

    def delete_profile(self, profile):

        uri = "api/v1/profile"
        self.params['permanent'] = True
        Assert.true(self._do_delete(uri, profile['id']), 'Deletion of product %s failed' % profile['name'])

    def get_category(self, name):

        uri = "api/v1/category/"
        get_params = {
            u'name': unicode(name)
        }
        category = self._do_get(uri, get_params)

        Assert.greater(category['id'], 0, 'No category was created.')

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

    def create_environment(self, profile, element):

        uri = "api/v1/environment/"
        post_data = {
            u'profile': unicode('/%s' % profile.uri),
            u'elements': [unicode('/%s' % element.uri)]
        }
        id = self._do_post(uri, post_data)

        Assert.greater(id, 0, 'No environment was created.')

    def delete_environment(self, id):

        uri = "api/v1/environment"
        self.params['permanent'] = True
        Assert.true(self._do_delete(uri, id), 'Deletion of environment %s failed' % id)
