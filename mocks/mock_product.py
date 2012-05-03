#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MockProduct(dict):

    def __init__(self, **kwargs):
        # set your default values

        self['name'] = 'Test Product'
        self['version'] = 'Test Version'
        self['desc'] = 'This is a test product'
        self['profile'] = None

        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
