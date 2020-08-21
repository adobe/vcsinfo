"""
Copyright (C) 2020 Adobe
"""

from __future__ import absolute_import

import email.parser
import io
import os
import re
import sys

import vcsinfo


class VCSPyInfo(vcsinfo.VCS):
    """Minimal class for querying Python info files"""

    VERSION_RE = re.compile(r'(?P<coarse>[.\d]*\d)\.(?P<number>\d+)(.dev(?P<modified>\d+))?')

    def __init__(self, dirname):
        vcsinfo.VCS.__init__(self)

        # Look for a specific .egg-info subdirectory which will contain more information
        # than just a PKG-INFO in dirname.
        files = os.listdir(dirname)
        contents = [ent for ent in files if ent.endswith('.egg-info')]
        if contents:
            _dirname = os.path.join(dirname, contents[0])
        else:
            # Didn't find a .egg-info - stick with dirname
            _dirname = dirname
        self.detect_source_root(_dirname)


    def detect_source_root(self, dirname):
        '''Identify if a directory might be an .info-info directory.'''

        dirname = os.path.realpath(dirname)
        try:
            pi_path = os.path.join(dirname, 'PKG-INFO')
            with io.open(pi_path, encoding='utf-8', errors='replace') as piobj:
                raw_pi = piobj.read()
            self.pkg_info = email.parser.Parser().parsestr(raw_pi)
        except (ValueError, IOError) as err:
            raise TypeError("Directory '{}' is not an pkg_info directory: {}".format(dirname, err))
        self.source_root = dirname
        sources_txt = os.path.join(dirname, 'SOURCES.txt')
        try:
            with io.open(sources_txt, encoding='utf-8', errors='replace') as st_obj:
                self.files = st_obj.readlines()
        except IOError:
            # FIXME: walk directory looking for files
            self.files = None


    def _get_version(self):
        return self.pkg_info.get('Version')


    def _match_version(self):
        try:
            mobj = self._ver_mobj
        except AttributeError:
            mobj = self._ver_mobj = re.match(self.VERSION_RE, self._get_version())
        return mobj


    @property
    def name(self):
        return self.pkg_info.get('Name')


    @property
    def branch(self):
        mobj = self._match_version()
        if mobj:
            branch = mobj.groupdict().get('coarse', '0') or '0'
        else:
            branch = '0'
        return branch


    @property
    def user(self):
        return None


    @property
    def id(self):
        mobj = self._match_version()
        if mobj:
            ids = '.'.join((
                mobj.groupdict().get('coarse', '0') or '0',
                mobj.groupdict().get('number', '0') or '0',
            ))
        else:
            ids = '0'
        return ids


    @property
    def id_short(self):
        return self.id


    @property
    def number(self):
        mobj = self._match_version()
        if mobj:
            number = mobj.groupdict().get('number', '0') or '0'
        else:
            number = '0'
        return int(number)


    def list_files(self):
        return self.files


    @property
    def modified(self):
        mobj = re.match(self.VERSION_RE, self.id)
        if mobj:
            mod = mobj.groupdict().get('modified', '0') or '0'
        else:
            mod = '0'
        return int(mod)


VCS = VCSPyInfo


# Local Variables:
# fill-column: 100
# End:
