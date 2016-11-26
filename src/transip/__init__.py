from __future__ import absolute_import, division, print_function, unicode_literals

from .__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__, __uri__, __version__
)
from .crypt import Key
from .errors import *  # noqa
from .service import Service


class DomainService(Service):
    pass


__all__ = [
    '__title__', '__summary__', '__uri__', '__version__', '__author__', '__email__', '__license__', '__copyright__',
    'TransIpError', 'Key', 'DomainService'
]
