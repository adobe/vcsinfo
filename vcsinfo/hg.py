"""
Copyright (C) 2012-2013 Adobe
"""

import os
import vcsinfo

try:
    from mercurial import (
        hg,
        ui,
        )
except ImportError as err:
    raise vcsinfo.VCSUnsupported("Mercurial VCS module requires mercurial: {0}".format(err))


class VCSHg(vcsinfo.VCS):
    """Minimal class for querying a source tree managed by Mercurial (Hg)"""


    def __init__(self, dirname):
        vcsinfo.VCS.__init__(self)

        hgui = ui.ui()
        self.detect_source_root(dirname)

        self.vcs_obj = hg.repository(hgui, path=self.source_root, create=False)


    def detect_source_root(self, dirname):
        """Find the top-most source directory"""
        repo_dir = vcsinfo.search_parent_dirs(dirname, '.hg')
        if not repo_dir:
            raise TypeError("Directory '%s' is not managed by hg" % dirname)
        self.source_root = os.path.dirname(repo_dir)


    @property
    def upstream_repo(self):
        """The location of the up-stream VCS repository."""
        return self.vcs_obj.ui.config('paths', 'default')


    @property
    def name(self):
        if not self._name:
            if self.vcs_obj.ui.config('paths', 'default'):
                # There's an upstream - use the basename for the name
                path = self.vcs_obj.ui.config('paths', 'default')
            else:
                # No upstream - the directory is the repo - use the
                # directory basename (without "dot" extensions) as
                # the name.
                path = self.source_root
            self._name = os.path.splitext(os.path.basename(path))[0]
        return self._name


    @property
    def branch(self):
        return self.vcs_obj['.'].branch()


    @property
    def id(self):
        return self.vcs_obj['.'].hex()


    @property
    def id_short(self):
        return self.id[:6]


    @property
    def number(self):
        return int(self.vcs_obj['.'].rev())


    def status(self):
        return self.vcs_obj.status(ignored=True, clean=True, unknown=True)


    def list_files(self):
        status = self.status()
        vcs_files = list(
            set(status[vcsinfo.ST_CLN])
            | set(status[vcsinfo.ST_ADD])
            | set(status[vcsinfo.ST_MOD])
        )
        vcs_files.sort()
        return vcs_files


VCS = VCSHg
