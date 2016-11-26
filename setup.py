import os

from setuptools import find_packages, setup


base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, 'src')

install_require = [
    'six >= 1.10.0, < 2.0',
    'cryptography >= 1.0, < 2.0',
    'zeep == 0.23.0',
]

tests_require = [
    'pytest >= 3.0.0, < 4.0.0',
    'tox',
]

about = {}
with open(os.path.join(src_dir, 'transip', '__about__.py')) as fo:
    exec(fo.read(), {}, about)

with open(os.path.join('README.rst')) as fo:
    readme = fo.read()

setup(
    name=about['__title__'],
    version=about['__version__'],

    description=about['__summary__'],
    long_description=readme,
    license=about['__license__'],
    url=about['__uri__'],

    author=about['__author__'],
    author_email=about['__email__'],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,

    install_requires=install_require,
    tests_require=tests_require,
    extras_require={'test': tests_require},

    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
    zip_safe=False,
)
