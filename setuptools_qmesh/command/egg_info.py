#
#    Copyright (C) 2013 Alexandros Avdis and others.
#    See the AUTHORS.md file for a full list of copyright holders.
#
#    This file is part of setuptools-qmesh.
#
#    setuptools-qmesh is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    setuptools-qmesh is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with setuptools-qmesh.  If not, see <http://www.gnu.org/licenses/>.

'''Functions writing egg-info files.

The map ``entry_points`` in ``setuptools.setup`` contains a ``egg_info.writers`` key, to
allow writing of custom egg-info files. The key ``egg_info.writers`` maps to a list of
strings, written as ``<FILENAME> = <module.function>``. Evidently these strings define the
new egg-info files and bound each file to a function. It is the job of the function to
write the file. The functions are defined in the present module.
'''

import os
import git

def write_git_sha_key(cmd, basename, filename):
    '''Store the git sha key to an egg-info file.

    Write the repository's git sha key to an egg-info file when the distribution attribute
    ``include_git_sha_key`` is ``True``. The attribute value is typically set by argument
    ``include_git_sha_key`` in ``setuptools.setup()``. Intended for use by setuptools only.

    Args:
       cmd (setuptools.command.egg_info.egg_info): Object creating a distribution's
           egg-info directory and contents.
       basename (str): Filename to write.
       filename (str): Complete path, with filename, to write.
    '''
    if cmd.distribution.include_git_sha_key:
        try:
            try:
                repo = git.Repo(".")
                git_sha_key = repo.head.object.hexsha
                if repo.is_dirty():
                    git_sha_key += " + uncommited changes (built from dirty repository)."
            except git.InvalidGitRepositoryError:
                git_sha_key = 'Could not obtain git sha key.'
        except ImportError:
            git_sha_key = 'Could not obtain git sha key.'
        argname = os.path.splitext(basename)[0]
        cmd.write_or_delete_file(argname, filename, git_sha_key)

def write_full_license(cmd, basename, filename):
    '''Store the licence statement to an egg-info file.

    Copy the full licence statement from a local file into an egg-info file, when the
    distribution attribute ``include_full_license`` is ``True``. The attribute value
    is typically set by argument ``include_full_license`` in ``setuptools.setup()``.
    Intended for use by setuptools only.

    Args:
       cmd (setuptools.command.egg_info.egg_info): Object creating a distribution's
           egg-info directory and contents.
       basename (str): Filename to write.
       filename (str): Complete path, with filename, to write.
    '''
    if cmd.distribution.include_full_license:
        argname = os.path.splitext(basename)[0]
        full_license_statement = open(basename).read()
        cmd.write_or_delete_file(argname, filename, full_license_statement)

def write_author_ids(cmd, basename, filename):
    '''Write the author IDs to an egg-info file.

    Copy the author IDs from a local file into an egg-info file, when the distribution
    attribute ``include_author_ids`` is ``True``. The attribute value is typically
    set by argument ``include_author_ids`` in ``setuptools.setup()``. Intended for use
    by setuptools only.

    Args:
       cmd (setuptools.command.egg_info.egg_info): Object creating a distribution's
           egg-info directory and contents.
       basename (str): Filename to write.
       filename (str): Complete path, with filename, to write.
    '''
    if cmd.distribution.include_author_ids:
        argname = os.path.splitext(basename)[0]
        author_ids = open(basename).read()
        cmd.write_or_delete_file(argname, filename, author_ids)

def write_qgis_path(cmd, basename, filename):
    '''Write the qgis path to an egg-info file.

    Write the qgis installation path to an egg-info file when the distribution attribute
    ``qgis_path`` is ``True``. The attribute value is typically set by argument ``qgis_path``
    in ``setup.py``. Intended for use by setuptools only.

    Args:
       cmd (setuptools.command.egg_info.egg_info): Object creating a distribution's
           egg-info directory and contents.
       basename (str): Filename to write.
       filename (str): Complete path, with filename, to write.
    '''
    if cmd.distribution.qgis_path:
        argname = os.path.splitext(basename)[0]
        cmd.write_or_delete_file(argname, filename, cmd.distribution.qgis_path)

def write_gmsh_bin_path(cmd, basename, filename):
    '''Write the gmsh binary path to an egg-info file.

    Write the gmsh binary installation path to an egg-info file when the distribution
    attribute ``gmsh_bin_path`` is ``True``. The attribute value is typically set by
    argument ``gmsh_bin_path`` in ``setup.py``. Intended for use by setuptools only.

    Args:
       cmd (setuptools.command.egg_info.egg_info): Object creating a distribution's
           egg-info directory and contents.
       basename (str): Filename to write.
       filename (str): Complete path, with filename, to write.
    '''
    if cmd.distribution.gmsh_bin_path:
        argname = os.path.splitext(basename)[0]
        cmd.write_or_delete_file(argname, filename, cmd.distribution.gmsh_bin_path)
