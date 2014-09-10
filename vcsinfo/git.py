"""
Copyright (C) 2014 Adobe
"""

from __future__ import absolute_import

import os
import vcsinfo

try:
    import git
except ImportError:
    raise vcsinfo.VCSUnsupported("GIT VCS module requires GitPython")


class VCSGit(vcsinfo.VCS):
    """
    Class used to retrieve information about a Git managed source tree.
    """


    git_to_vcsinfo_status = {
        'M' : vcsinfo.ST_MOD,
        'A' : vcsinfo.ST_ADD,
        'D' : vcsinfo.ST_REM,
        # FIXME - don't know how the below maps
        #'' : vcsinfo.ST_DEL,
        #'' : vcsinfo.ST_UNK,
        #'' : vcsinfo.ST_IGN,
        #'' : vcsinfo.ST_CLN,
    }


    def __init__(self, directory):
        """Constructor"""
        vcsinfo.VCS.__init__(self, directory)
        try:
            self.vcs_obj = git.Repo(directory)
        except git.exc.InvalidGitRepositoryError:
            raise TypeError("Source tree '%s' not managed by %s" % (
                directory,
                self.vcs,
            ))
        try:
            self.source_root = self.vcs_obj.working_tree_dir
        except AssertionError as exc:
            raise TypeError("Source tree '%s' not a working %s checkout" % (
                directory,
                self.vcs,
            ))


    def detect_source_root(self, directory):
        """
        This looks for a '.git' directory in directory and any parent
        directories.
        """
        self.repo_dir = vcsinfo.search_parent_dirs(directory, '.git')
        if not self.repo_dir:
            raise TypeError("Directory '%s' is not managed by git" % directory)
        self.source_root = os.path.dirname(self.repo_dir)


    @property
    def upstream_repo(self):
        """The location of the up-stream VCS repository."""
        try:
            return self.vcs_obj.remotes.origin.url
        except AttributeError:
            return None


    @property
    def name(self):
        if not self._name:
            if self.vcs_obj.remotes:
                # There's an upstream - use the basename for the name
                path = self.vcs_obj.remotes.origin.url
            else:
                path = self.source_root
            self._name = os.path.splitext(os.path.basename(path))[0]
        return self._name


    @property
    def branch(self):
        found_branch = None

        try:
            found_branch = self.vcs_obj.active_branch.name
        except TypeError:
            commits = {}
            branches = {}
            master_branch = None

            for branch in self.vcs_obj.branches:
                if 'master' == branch.name:
                    master_branch = branch
                else:
                    branches[branch.name] = branch

            def set_branch_info(branch, git_obj):
                if commits.has_key(git_obj.hexsha):
                    return False
                commits[git_obj.hexsha] = {
                    'branch' : branch,
                    'object' : git_obj,
                    }
                return True

            class _Branch_discovery_done(Exception): pass

            try:
                # Prime commit with 'master' branch first
                for branch in [master_branch] + branches.values():
                    # The reference isn't at the head of a branch else it
                    # would be .active_branch.name
                    if not set_branch_info(branch.name, branch.object):
                        # This object is already on another branch
                        continue
                    # Cannot follow branch name through a merge
                    if 1 < len(branch.object.parents):
                        continue
                    for git_obj in branch.object.iter_parents():
                        if git_obj.hexsha == self.vcs_obj.head.object.hexsha:
                            found_branch = branch.name
                            raise _Branch_discovery_done()
                        if not set_branch_info(branch.name, git_obj):
                            # This object is already on another branch
                            break
                        if 1 < len(git_obj.parents):
                            # Cannot follow branch name through a merge
                            break

            except _Branch_discovery_done, e:
                pass

        return found_branch


    @property
    def user(self):
        user = ''
        if self.vcs_obj.heads:
            user = self.vcs_obj.rev_parse(self.vcs_obj.head.name).committer.email
        return user.replace('@adobe.com', '')


    @property
    def id(self):
        idn = '0'
        if self.vcs_obj.heads:
            idn = self.vcs_obj.rev_parse(self.vcs_obj.head.name).hexsha
        return idn


    @property
    def id_short(self):
        return self.id[:6]


    @property
    def number(self):
        """
        Simulate the commit number.  This is done by looking at the commit
        offset from the base of the tree with respect to the branch where
        the commit is found.  This will return a number that should be
        unique to the branch and fairly stable across future commits
        (provided a branch is not rebased).
        """
        number = 0
        if not self.vcs_obj.heads:
            # There are no commits in this tree
            return number

        commit_id = self.id
        branch_name = self.branch
        try:
            branch = getattr(self.vcs_obj.branches, branch_name)
            # The below "sum(1 . . .)" counts the "length" of the
            # iter_parents() generator - so branch_count is the tree height
            # of the branch object (which is a HEAD).
            branch_count = 1 + sum(1 for _ in branch.object.iter_parents())

            # Branches are only HEADs
            if commit_id == branch.object.hexsha:
                # The commit is the HEAD of the branch.
                number = branch_count
            else:
                # The commit is not the HEAD, but we want the commit number
                # so step back how far below the head it is.
                for git_obj in branch.object.iter_parents():
                    branch_count -= 1
                    if git_obj.hexsha == commit_id:
                        number = branch_count
                        break
                else:
                    # The commit wasn't found on the branch line where it
                    # is located - unpossible!
                    raise Exception(
                        "Internal error: commit %s not on commit's branch %s"
                            % (commit_id, branch_name)
                    )
        except TypeError, e:
            pass

        return number


    def status(self):
        status = [[], [], [], [], [], [], []]

        for line in self.vcs_obj.git.status(porcelain=True).split('\n'):
            if not line:
                continue
            (change, filename) = line.split()[0:2]
            if change in self.git_to_vcsinfo_status:
                status[self.git_to_vcsinfo_status[change]].append(filename)

        vcs_files = set([
            fn
            for fn
            in self.vcs_obj.git.ls_files().split('\n')
            if fn
        ])

        clean_files = set(vcs_files)
        clean_files -= set(status[vcsinfo.ST_MOD])
        clean_files -= set(status[vcsinfo.ST_ADD])
        clean_files -= set(status[vcsinfo.ST_REM])
        clean_files = list(clean_files)
        clean_files.sort()
        status[vcsinfo.ST_CLN] = clean_files

        return status


    def list_files(self):
        status = self.status()
        vcs_files = list(
            set(status[vcsinfo.ST_CLN])
            | set(status[vcsinfo.ST_ADD])
            | set(status[vcsinfo.ST_MOD])
            )
        vcs_files.sort()
        return vcs_files


    pass


VCS = VCSGit
