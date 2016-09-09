#! /usr/bin/env python
#
# Mixpanel, Inc. -- http://mixpanel.com/
#
# Python API client library to consume mixpanel.com analytics data.
#
# Copyright 2010-2013 Mixpanel, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import urllib
import urllib2
import time
import demjson
try:
    import json
except ImportError:
    import simplejson as json
from mixpanel_query.utils import _totext

class Mixpanel_api(object):

    ENDPOINT = 'https://data.mixpanel.com/api'
    # ENDPOINT = 'http://mixpanel.com/api'
    VERSION = '2.0'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    
    def request(self, methods, params, format='json'):
        """
            methods - List of methods to be joined, e.g. ['events', 'properties', 'values']
                      will give us http://mixpanel.com/api/2.0/events/properties/values/
            params - Extra parameters associated with method
        """
        params['api_key'] = self.api_key
        params['expire'] = int(time.time()) + 600   # Grant this request 10 minutes.
        params['format'] = format
        if 'sig' in params: del params['sig']
        params['sig'] = self.hash_args(params)

        request_url = '/'.join([self.ENDPOINT, str(self.VERSION)] + methods) + '/?' + self.unicode_urlencode(params)

        request = urllib2.urlopen(request_url, timeout=120)
        data = request.read()
        print data
        return json.loads(data)
    
    def unicode_urlencode(self, params):
        """
            Convert lists to JSON encoded strings, and correctly handle any
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        return urllib.urlencode(
            [(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params]
        )

    def hash_args(self, args, secret=None):
        """
            Hashes arguments by joining key=value pairs, appending a secret, and
            then taking the MD5 hex digest.
        """
        for a in args:
            if isinstance(args[a], list): args[a] = json.dumps(args[a])

        args_joined = ''
        for a in sorted(args.keys()):
            if isinstance(a, unicode):
                args_joined += a.encode('utf-8')
            else:
                args_joined += str(a)

            args_joined += '='

            if isinstance(args[a], unicode):
                args_joined += args[a].encode('utf-8')
            else:
                args_joined += str(args[a])

        hash = hashlib.md5(args_joined)

        if secret:
            hash.update(secret)
        elif self.api_secret:
            hash.update(self.api_secret)
        return hash.hexdigest()

if __name__ == '__main__':
    api = Mixpanel_api(
        api_key = '862a8448704d584ce149704707a0e4e7',
        api_secret = '59bf255504e02918c9dc83eb7640144c'
    )
    query = {
        'event' : ['latencyMetric'],
        'name': 'experiment_id',
        'from_date': '2016-03-01',
        'to_date': '2016-03-16',
        'where': 'properties["component"]=="facebook-wall" and properties["version"]=="stable"'
    }

    data = api.request(['export'], query)
    # print data 
    
    # params1={'event':["latencyMetric"], 
    #     'name':'requestDuration',
    #         'type':"general",
    #         'from_date':'2016-03-01',
    #         'to_date':'2016-06-15',
    #         'unit':"day", 
    #         'interval':1}


    # params1_post={'event':["latencyMetric"], 
    #         'name':'experiment_id',
    #         'type':"general",
    #         'from_date':'2016-04-01',
    #         'to_date':'2016-06-15',
    #         'unit':"day", 
    #         'interval':1}
    # params2_post = {'event':["latencyMetric"], 
    #         'name':'component-id',
    #         'type':"general",
    #         'from_date':'2016-04-01',
    #         'to_date':'2016-06-15',
    #         'unit':"day", 
    #         'interval':1}

    # respuesta_post=api.request(['events/properties/values'], params1, format='json')
    # respuesta_post_sort=sorted(respuesta_post)

    # respuesta_post1=api.request(['events/properties/values'], params1_post, format='json')
    # respuesta_post_sort1=sorted(respuesta_post1)

    # listapost=zip(respuesta_post_sort1,respuesta_post_sort)
    # print listapost