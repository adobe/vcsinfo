#########
 vcsinfo
#########

Summary
#######

``vcsinfo`` gathers information about a source tree, supporting Git, Mercurial,
and Perforce working directories.

Installation
############

.. code-block::

    pip install vcsinfo

Usage
#####

Example usage using the vcsinfo project itself (git backend):

.. code-block:: python

    import vcsinfo

    data = vcsinfo.detect_vcs(my_path)
    data.name  # project name: 'vcsinfo'
    data.branch  # branch name: 'main'
    data.id  # native commit identification: '4bb323148e43543247afe066db0dbac0fcf45537'
    data.upstream_repo  # upstream repo url: 'git@github.com/adobe/vcsinfo.git'
    data.user  # user who performed the commit: 'saville'
    data.id_short  # a short representation of the id: '4bb323'
    data.number  # same as id if commits have increasing numbers, otherwise simulated an increasing commit number: 77 
    data.modified  # none if no local modifications, otherwise the epoch seconds of the most recently modified file: 1629746987
    data.release  # string representing the current state of the branch: '77.I4bb323.M1629746987'
    data.id_string  # string providing a unique id of branch and release: 'main-77.I4bb323.M1629746987'

    # Retrieves a tuple of lists of modified changes in the changeset, see code
    # for return format 
    data.status()

    # List the files known to the VCS
    data.list_files()

    # Retrieves VCS information as a dict, optionally including full file information
    data.info()
    data.info(include_files=True)

