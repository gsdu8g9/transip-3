from __future__ import absolute_import, division, print_function, unicode_literals

import binascii
import calendar
import collections
import random
import re
import time

import six


_re_url_encode = re.compile(b'[^A-Za-z0-9._~-]')


def _url_encode_callback(match):
    return b'%' + binascii.hexlify(match.group(0)).upper()


def url_encode(component):
    """Same as PHP's rawurlencode, which conforms to RFC 3986.

    Supports bytes text objects. Text objects are encoded with UTF-8 as required.
    Also supports number like objects, boolean, None type
    and all other types that implement __str__
    """

    if component is None or component is False:
        value = b''
    elif component is True:
        value = b'1'
    elif isinstance(component, six.binary_type):
        value = component
    else:
        value = six.text_type(component).encode('utf-8')
    return _re_url_encode.sub(_url_encode_callback, value)


def url_encode_parameters(params):
    """Encode dictionary and array like objects PHP style conforming to RFC 3986."""

    queue = collections.deque()
    queue.append((b'', params))

    parts = collections.deque()
    while len(queue):
        prefix, component = queue.pop()
        if isinstance(component, collections.Mapping):
            items = six.iteritems(component)
        elif isinstance(component, (six.binary_type, six.text_type)):
            items = None
        elif isinstance(component, collections.Sequence):
            items = enumerate(component)
        else:
            items = None

        if items is None:
            value = url_encode(component)
            parts.append(prefix + b'=' + value if len(prefix) else value)
            continue

        for key, value in reversed(list(items)):
            encoded_key = url_encode(key)
            if len(prefix):
                encoded_key = prefix + b'[' + encoded_key + b']'
            queue.append((encoded_key, value))

    return b'&'.join(parts)


def uniqid(prefix='', more_entropy=False):
    """Generates uniq id with same characteristics as PHP."""

    now = time.time()
    seconds = int(now)
    microns = int(round((now - seconds)*1000000))
    seconds = calendar.timegm(time.gmtime(seconds))

    simple = '{}{:08x}{:05x}'.format(prefix, seconds, microns)
    if more_entropy:
        return '{}{:.8f}'.format(simple, random.random() * 10)
    else:
        return simple
