import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'vcsinfo/VERSION')) as fobj:
    version = fobj.read().strip()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fobj:
    long_description = fobj.read().strip()

# pylint: disable=C0301
setup(
    name='vcsinfo',
    version=version,
    author='Adobe',
    author_email='noreply@adobe.com',
    license='MIT',
    url='https://github.com/adobe/vcsinfo',
    description='Utilities to normalize working with different Version Control Systems',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=find_packages(exclude=("tests",)),
    scripts=[
        'bin/vcsinfo',
    ],
    install_requires=[
        'GitPython<4',
        'gitdb<5',
    ],
    extras_require={
        # Make everything except git an optional dependency
        'hg': ['mercurial'],
        'p4': ['p4python'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
