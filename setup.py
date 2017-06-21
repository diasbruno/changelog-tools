from __future__ import print_function
import io
import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

import changelogtools

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('readme.md', 'CHANGELOG.md')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='changelog-tools',
    version=changelogtools.__version__,

    description='Tools to help writing a project changelog.',
    long_description=long_description,

    url='http://github.com/diasbruno/changelog-tools/',
    license='Unlicense',

    author='Bruno Dias',
    author_email='dias.h.bruno@gmail.com',

    platforms='any',

    test_suite='changelog.tests',

    cmdclass={'test': PyTest},

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: Unlicense',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='changelog development',

    extras_require={
        'testing': ['pytest']
    }
)
