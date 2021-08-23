"""
Copyright (C) 2014-2020 Adobe
"""

import os
import sys
from setuptools import setup, find_packages
import vcsinfo

VERSION = '1.0'
THIS_DIR = os.path.dirname(__file__)
BUILD_NR = None
try:
    VCS = None
    # Only use py_info if git or something else is not available.
    for _vcs in vcsinfo.detect_vcss(THIS_DIR):
        if _vcs.vcs == 'pyinfo':
            VCS = _vcs
            # keep looking for a real VCS
        else:
            VCS = _vcs
            break
    if VCS and VCS.number:
        BUILD_NR = VCS.number
        if VCS.modified:
            BUILD_NR = f'{BUILD_NR}.dev{VCS.modified}'
except vcsinfo.VCSUnsupported:
    pass

if BUILD_NR:
    VERSION = f'{VERSION}.{BUILD_NR}'

REQ_FILE = 'requirements.txt'
REQUIRES = []
try:
    with open(os.path.join(THIS_DIR, REQ_FILE)) as robj:
        for line in robj.readlines():
            _line = line.strip()
            if _line and _line[0].isalpha():
                REQUIRES.append(_line)
except IOError as err:
    # pylint: disable=C0301
    sys.stderr.write(f'Python build requirements must be specified in "{REQ_FILE}": {err}\n')
    sys.exit(err.errno)

with open(join(dirname(__file__), 'README.rst')) as fobj:
    LONG_DESCRIPTION = fobj.read().strip()

# pylint: disable=C0301
setup(
    name='vcsinfo',
    version=VERSION,
    author='Adobe',
    author_email='noreply@adobe.com',
    license='MIT',
    url='https://github.com/adobe/vcsinfo',
    description='Utilities to normalize working with different Version Control Systems',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    scripts=[
        'bin/vcsinfo',
    ],
    install_requires=REQUIRES,
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
