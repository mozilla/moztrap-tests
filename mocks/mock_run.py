# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class MockRun(dict):

    def __init__(self, **kwargs):
        # set your default values

        self['name'] = 'Test Run'
        self['product_version'] = 'Test Product Test Version'
        self['desc'] = 'This is a test run'
        self['start_date'] = '2011-01-01'
        self['end_date'] = '2012-12-31'
        self['suite_list'] = None

        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
