from __future__ import absolute_import, division, print_function, unicode_literals

import six
import zeep

from .plugins import UserAgentPlugin, SignPlugin


class ServiceMeta(type):
    def __init__(cls, name, bases, dict):
        cls.name = cls.__name__


class Service(six.with_metaclass(ServiceMeta, zeep.Client)):
    def __init__(self, key, login, endpoint='api.transip.nl', mode='readwrite'):
        self.endpoint = endpoint
        super(Service, self).__init__(self.wsdl_url, plugins=[UserAgentPlugin(), SignPlugin(self, key, login, mode)])

    @property
    def wsdl_url(self):
        return 'https://{}/wsdl/?service={}'.format(self.endpoint, self.name)
