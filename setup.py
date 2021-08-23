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
    packages=find_packages(),
    scripts=[
        'bin/vcsinfo',
    ],
    install_requires=[
        # This is the last version of GitPython that still works with Python 2.7
        'GitPython==2.1.8',
        # Newer versions of gitdb2 require Python 3.x - not everything has been pulled-up to 3.x
        'gitdb2<=2.0.6',
        'mercurial',
    ],
    extras_require={
        # Perforce is not as common anymore, so make it an optional dependency
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
