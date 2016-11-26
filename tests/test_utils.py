from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

import pytest

from transip.utils import uniqid, url_encode, url_encode_parameters


class TestUrlEncode(object):
    def test_unreserved(self):
        unreserved = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'
        assert url_encode(unreserved) == unreserved

    def test_gen_delims(self):
        assert url_encode(b':/?#[]@') == b'%3A%2F%3F%23%5B%5D%40'

    def test_sub_delims(self):
        assert url_encode(b"!$&'()*+,;=") == b'%21%24%26%27%28%29%2A%2B%2C%3B%3D'

    def test_double_quote(self):
        assert url_encode(b'"') == b'%22'

    def test_utf8(self):
        assert url_encode('\u20ac') == b'%E2%82%AC'

    def test_none(self):
        assert url_encode(None) == b''

    def test_false(self):
        assert url_encode(False) == b''

    def test_true(self):
        assert url_encode(True) == b'1'

    def test_zero(self):
        assert url_encode(0) == b'0'


class TestUrlEncodeParameters(object):
    def test_simple(self):
        assert url_encode_parameters({'key': 'value'}) == b'key=value'

    def test_text(self):
        assert url_encode_parameters('test') == b'test'

    def test_escape(self):
        assert url_encode_parameters({'key': 'a=1&b=2'}) == b'key=a%3D1%26b%3D2'

    def test_nested(self):
        assert (
            url_encode_parameters(OrderedDict([
                ('nested', OrderedDict([('hello', 'world'), ('goodbye', 'friend')])),
                ('other', 'something'),
                ('third', {'second': {'one': 'zero'}})
            ])) == b'nested[hello]=world&nested[goodbye]=friend&other=something&third[second][one]=zero'
        )

    def test_numeric_key(self):
        assert (url_encode_parameters(OrderedDict([
                    (123, 'abc'),
                    (3.14, 'def')
            ])) == b'123=abc&3.14=def')

    def test_list(self):
        assert url_encode_parameters(['a', 'b', 'c']) == b'0=a&1=b&2=c'

    def test_tuple(self):
        assert url_encode_parameters(('a', 'b', 'c')) == b'0=a&1=b&2=c'

    def test_bytes(self):
        assert url_encode_parameters({'binary': b'\xde\xad\xbe\xef'}) == b'binary=%DE%AD%BE%EF'

    def test_none(self):
        assert url_encode_parameters({'none': None}) == b'none='

    def test_zero(self):
        assert url_encode_parameters({'zero': 0}) == b'zero=0'

    def test_false(self):
        assert url_encode_parameters({'false': False}) == b'false='

    def test_true(self):
        assert url_encode_parameters({'true': True}) == b'true=1'


@pytest.fixture(scope='function')
def fixed_random_and_time(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 1 - 1e-9)
    monkeypatch.setattr('time.time', lambda: 1468354889.999999)


class TestUniqId(object):
    def test_default(self, fixed_random_and_time):
        assert uniqid() == '57855149f423f'

    def test_more_entropy(self, fixed_random_and_time):
        assert uniqid('', True) == '57855149f423f' + '9.' + 8 * '9'

    def test_prefix(self, fixed_random_and_time):
        assert uniqid('abc') == 'abc57855149f423f'
