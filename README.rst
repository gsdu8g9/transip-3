=============================
TransIP API client for Python
=============================

TransIP_ provides a SOAP API for various services, including the popular DNS service.
Authentication is done by signing the call by a private key.
This library uses the libraries Zeep_ and Cryptography_ and tries to provide a convenience interface for using the API.

Status
------
.. image:: https://travis-ci.org/middagj/transip.svg?branch=master
    :target: https://travis-ci.org/middagj/transip

Example
-------
.. code:: python

  from transip import Key, DomainService
  username = ''
  key_file = ''

  with open(key_file, 'rb') as fo:
      key = Key.load(fo.read())
  ds = DomainService(key, username)
  domains = ds.service.getDomainNames()
  info = ds.service.getInfo(domains[0])

License
-------
This software is licensed under the MIT License. `View the license`_.

.. _TransIP: https://www.transip.nl/transip/api/
.. _Zeep: http://docs.python-zeep.org/en/master/
.. _Cryptography: https://cryptography.io/en/latest/
.. _View the license: LICENSE
