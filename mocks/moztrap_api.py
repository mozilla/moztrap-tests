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

    def _do_post(self, uri, post_data, return_response_text=False):
        """Post to an API method and return the resulting id and the response text."""
        response = requests.post(
            "%s/%s" % (self.base_url, uri),
            params=self.params,
            data=json.dumps(post_data),
            headers=self.headers)
        response.raise_for_status()
        text = json.loads(response.text)

        if response.status_code == 201:
            if return_response_text:
                return text['id'], text
            else:
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
        if response.status_code == requests.codes.ok:
            return True
        else:
            print "Failed to delete resource: %s with %s.\n%s" % (
                id, response.status_code, response.text)
            return False

    def _do_get(self, uri, get_params):
        """Get to an API method and return an array of objects."""
        response = requests.get("%s/%s" % (self.base_url, uri), params=get_params)
        response.raise_for_status()
        text = json.loads(response.text)
        objects = text["objects"]
        next = text["meta"]["next"]
        while next:
            response = requests.get("%s/%s" % (self.base_url, next))
            response.raise_for_status()
            text = json.loads(response.text)
            objects.extend(text["objects"])
            next = text["meta"]["next"]
        return objects

    def create_product(self, product):

        uri = "api/v1/product/"
        post_data = {
            u'name': unicode(product['name']),
            u'description': unicode(product['description']),
            u'productversions': [{u'version': unicode(product['version']['name'])}]
        }
        product['id'], response_text = self._do_post(uri, post_data, True)
        product['version']['uri'] = response_text['productversions'][0]['resource_uri']

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

        # First we need to find any Environments that use the element and delete them
        uri = "api/v1/environment"
        self.params['elements'] = element['id']
        environments = self._do_get(uri, self.params)
        for environment in environments:
            self.delete_environment(environment)

        # Next delete the Element
        uri = "api/v1/element"
        self.params['permanent'] = True
        Assert.true(self._do_delete(uri, element['id']), 'Deletion of element %s failed' % element['name'])

        # Finally delete the embedded Category
        uri = "api/v1/category"
        category = element['category']
        Assert.true(self._do_delete(uri, category['id']), 'Deletion of category %s failed' % category['name'])

    def delete_environment(self, environment):

        uri = "api/v1/environment"
        self.params['permanent'] = True
        Assert.true(self._do_delete(uri, environment['id']), 'Deletion of environment %s failed' % environment['id'])

    def create_suite(self, suite, product, case_list=[]):

        uri = "api/v1/suite/"
        post_data = {
            u'name': unicode(suite['name']),
            u'product': unicode('/%s' % product.uri)
        }
        suite['id'] = self._do_post(uri, post_data)

        Assert.greater(suite['id'], 0, 'No suite was created.')

        # add cases to suite
        for i, case in enumerate(case_list):
            self.create_suite_case(suite, case, i)

    def create_suite_case(self, suite, case, order):

        uri = "api/v1/suitecase/"
        post_data = {
            u'suite': unicode('/%s' % suite.uri),
            u'case': unicode('/%s' % case.uri),
            u'order': unicode(order)
        }
        id = self._do_post(uri, post_data)

        Assert.greater(id, 0, 'No suite_case was created.')

    def create_case(self, case, product):

        # First create the case
        uri = "api/v1/case/"
        post_data = {
            u'name': unicode(case['name']),
            u'product': unicode('/%s' % product.uri)
        }
        case['id'] = self._do_post(uri, post_data)

        Assert.greater(case['id'], 0, 'No case was created.')

        # Next create the caseversion
        uri = "api/v1/caseversion/"
        post_data = {
            u'name': unicode(case['name']),
            u'case': unicode('/%s' % case.uri),
            u'productversion': unicode(product['version']['uri'])
        }
        case['version'] = {}
        case['version']['id'], response_text = self._do_post(uri, post_data, True)
        case['version']['uri'] = response_text['resource_uri']

        Assert.greater(case['version']['id'], 0, 'No caseversion was created.')

        # Next create the casestep
        uri = "api/v1/casestep/"
        post_data = {
            u'caseversion': unicode(case['version']['uri']),
            u'number': unicode(1),
            u'instruction': unicode(case['step1_instruction'])
        }
        id = self._do_post(uri, post_data)

        Assert.greater(id, 0, 'No casestep was created.')
