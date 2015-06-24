from distutils.core import setup

setup(
    name='backports_abc',
    version="0.1",
    url='https://github.com/cython/backports_abc',
    author='Stefan Behnel et al.',
    author_email='cython-devel@python.org',
    description="A backport of recent additions to the 'collections.abc' module.",
    long_description="""\
Usage::

    import backports_abc

    try:
        from collections.abc import Coroutine, Generator
    except ImportError:
        from collections import Coroutine, Generator
""",
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
