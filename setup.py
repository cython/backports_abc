
import io
from setuptools import setup


with io.open('README.rst', encoding='utf8') as _f:
    long_description = _f.read().strip()


with io.open('CHANGES.rst', encoding='utf8') as _f:
    long_description += '\n\n' + _f.read().strip() + '\n'


setup(
    name='backports_abc',
    version="0.3",
    url='https://github.com/cython/backports_abc',
    author='Stefan Behnel et al.',
    author_email='cython-devel@python.org',
    description="A backport of recent additions to the 'collections.abc' module.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],

    py_modules=["backports_abc"],
)
