"""
Copyright (C) 2020 Adobe
"""

from __future__ import absolute_import, print_function

import os

import pkg_resources
import vcsinfo


class VCSPyEgg(vcsinfo.VCS):
    """Minimal class for queryin a Python egg"""


    def __init__(self, dirname):
        vcsinfo.VCS.__init__(self)
        try:
            self.dist = self.detect_source_root(dirname)
        except TypeError:
            contents = [ent for ent in os.listdir(dirname) if ent.endswith('.egg-info')]
            subdirname = os.path.join(dirname, contents[0])
            self.dist = self.detect_source_root(subdirname)


    def detect_source_root(self, dirname):
        '''Identify if a directory might be an .egg-info directory.'''

        egg_info = os.path.realpath(dirname)
        base_dir = os.path.dirname(egg_info)
        metadata = pkg_resources.PathMetadata(base_dir, egg_info)
        dist_name = os.path.splitext(os.path.basename(egg_info))[0]
        dist = pkg_resources.Distribution(base_dir, project_name=dist_name, metadata=metadata)
        try:
            _ = dist.version
        except ValueError:
            raise TypeError("Directory '%s' is not an egg_info directory." % dirname)
        self.source_root = base_dir
        self.dist = dist
        sources_txt = os.path.join(base_dir, 'SOURCES.txt')
        try:
            with open(sources_txt, 'r') as src_txt_obj:
                self.files = src_txt_obj.readlines()
        except IOError:
            self.files = None
        return dist


    @property
    def name(self):
        return self.dist.project_name


    @property
    def branch(self):
        return None


    @property
    def user(self):
        return None


    @property
    def id(self):
        return self.dist.version


    @property
    def id_short(self):
        return self.id


    @property
    def number(self):
        pass


    def status(self):
        pass


    def list_files(self):
        return self.files


    @property
    def modified(self):
        return 0


VCS = VCSPyEgg


# Local Variables:
# fill-column: 100
# End:
