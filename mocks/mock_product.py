#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime


class MockProduct(dict):

    def __init__(self, name='Test Product', version='Test Version', description='This is a test product', profile=None):

        dt_string = datetime.utcnow().isoformat()
        self['id'] = None
        self['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        self['description'] = u'%(desc)s created on %(dt_string)s' % {'desc': description, 'dt_string': dt_string}
        self['version'] = {}
        self['version']['name'] = u'%(version)s %(dt_string)s' % {'version': version, 'dt_string': dt_string}
        self['profile'] = profile

    # allow getting items as if they were attributes
    def __getattr__(self, attr):
        return self[attr]
