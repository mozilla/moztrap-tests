#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MockCase(dict):

    def __init__(self, **kwargs):
        # set your default values

        self['name'] = 'Test Case'
        self['product'] = 'Test Product'
        self['version'] = 'Test Version'
        self['suite'] = None
        self['desc'] = 'This is a test case'
        self['step1_instruction'] = 'Test Case step 1 instruction'
        self['step1_result'] = 'Test Case step 1 expected result'
        self['status'] = 'active'

        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
