from __future__ import absolute_import, division, print_function, unicode_literals

import time
from base64 import b64encode
from collections import OrderedDict

import six
import zeep
from lxml import etree

from .__about__ import __uri__, __version__
from .utils import uniqid, url_encode, url_encode_parameters


class UserAgentPlugin(zeep.Plugin):
    def __init__(self):
        self.user_agent = 'TransIP/{0} ({1})'.format(__version__, __uri__)

    def egress(self, envelope, http_headers, *args):
        http_headers['user-agent'] = self.user_agent
        return envelope, http_headers


class SignPlugin(zeep.Plugin):
    version = '5.2'

    def __init__(self, service, key, login, mode):
        self.service = service
        self.key = key
        self.login = login
        self.mode = mode

    def egress(self, envelope, http_headers, operation, binding_options):
        timestamp = int(time.time())
        nonce = uniqid('', True)

        cookies = OrderedDict()
        cookies['login'] = self.login
        cookies['mode'] = self.mode
        cookies['timestamp'] = timestamp
        cookies['nonce'] = nonce
        cookies['serviceVersion'] = self.version

        params = self._collect_params(envelope)
        params['__method'] = operation.name
        params['__service'] = self.service.name
        params['__hostname'] = self.service.endpoint
        params['__timestamp'] = timestamp
        params['__nonce'] = nonce

        signature = self.key.sign(url_encode_parameters(params))
        cookies['signature'] = url_encode(b64encode(signature)).decode('ascii')
        http_headers['cookie'] = ';'.join('{}={}'.format(key, value) for key, value in six.iteritems(cookies))
        return envelope, http_headers

    @classmethod
    def _collect_params(cls, envelope):
        params = OrderedDict()
        for i, item in enumerate(envelope[0][0]):
            params[i] = etree.tostring(item, method='text')

        return params
