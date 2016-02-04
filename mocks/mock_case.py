# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime


class MockCase(dict):

    def __init__(self, **kwargs):

        dt_string = datetime.utcnow().isoformat()
        self['id'] = None
        self['name'] = u'Test Case %s' % dt_string
        self['description'] = u'This is a test case created on %s' % dt_string
        self['step1_instruction'] = 'Test Case step 1 instruction %s' % dt_string
        self['step1_result'] = 'Test Case step 1 expected result %s' % dt_string
        self['status'] = 'active'

        # update with any keyword arguments passed
        self.update(**kwargs)

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]

    @property
    def uri(self):
        return 'api/v1/case/%s/' % self['id']
