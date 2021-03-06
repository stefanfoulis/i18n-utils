#!/usr/bin/env python

import io
import os
import re
import sys
import ast

from setuptools import setup, find_packages


PACKAGE = 'i18n_utils'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class Setup(object):
    @staticmethod
    def read(fname, fail_silently=False):
        """
        Read the content of the given file. The path is evaluated from the
        directory containing this file.
        """
        try:
            filepath = os.path.join(os.path.dirname(__file__), fname)
            with io.open(filepath, 'rt', encoding='utf8') as f:
                return f.read()
        except:
            if not fail_silently:
                raise
            return ''

    @staticmethod
    def requirements(fname):
        """
        Create a list of requirements from the output of the pip freeze command
        saved in a text file.
        """
        packages = Setup.read(fname, fail_silently=True).split('\n')
        packages = (p.strip() for p in packages)
        packages = (p for p in packages if p and not p.startswith('#'))
        packages = (p for p in packages if p and not p.startswith('https://'))
        return list(packages)

    @staticmethod
    def get_files(*bases):
        """
        List all files in a data directory.
        """
        for base in bases:
            basedir, _ = base.split('.', 1)
            base = os.path.join(os.path.dirname(__file__), *base.split('.'))

            rem = len(os.path.dirname(base)) + len(basedir) + 2

            for root, dirs, files in os.walk(base):
                for name in files:
                    yield os.path.join(basedir, root, name)[rem:]

    @staticmethod
    def version():
        data = Setup.read(os.path.join(PACKAGE, '__init__.py'))
        version = (re.search(u"__version__\s*=\s*u?'([^']+)'", data)
                   .group(1).strip())
        return version

    @staticmethod
    def url():
        data = Setup.read(os.path.join(PACKAGE, '__init__.py'))
        version = (re.search(u"__url__\s*=\s*u?'([^']+)'", data)
                   .group(1).strip())
        return version

    @staticmethod
    def shortdesc():
        filename = os.path.join(PACKAGE, '__init__.py')
        data = Setup.read(filename)
        node = ast.parse(data, filename)
        docstring = ast.get_docstring(node)
        desc = docstring.strip().split('\n\n', 1)[0]
        return desc.replace('\n', ' ')

    @staticmethod
    def longdesc():
        return Setup.read('README.rst') + '\n\n' + Setup.read('HISTORY.rst')

    @staticmethod
    def test_links():
        # Test if hardlinks work. This is a workaround to
        # http://bugs.python.org/issue8876 (fixed on 2014-10-30)
        if hasattr(os, 'link'):
            tempfile = __file__ + '.tmp'
            try:
                os.link(__file__, tempfile)
            except OSError as e:
                if e.errno == 1:  # Operation not permitted
                    del os.link
                else:
                    raise
            finally:
                if os.path.exists(tempfile):
                    os.remove(tempfile)


Setup.test_links()

setup(name=PACKAGE,
      version=Setup.version(),
      author='Jonathan Stoppani',
      author_email='jonathan@stoppani.name',
      include_package_data=True,
      zip_safe=False,
      url=Setup.url(),
      license='MIT',
      packages=find_packages(),
      package_dir={PACKAGE: PACKAGE},
      description=Setup.shortdesc(),
      install_requires=Setup.requirements('requirements.txt'),
      long_description=Setup.longdesc(),
      entry_points=Setup.read('entry-points.ini', True),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ])
