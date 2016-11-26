from __future__ import absolute_import, division, print_function, unicode_literals

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Key(object):
    backend = default_backend()

    def __init__(self, key):
        self.key = key

    @classmethod
    def load(cls, fo):
        return cls(cls.backend.load_pem_private_key(fo, None))

    def sign(self, data):
        signer = self.key.signer(padding.PKCS1v15(), hashes.SHA512())
        signer.update(data)
        return signer.finalize()
