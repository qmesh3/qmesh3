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
''' Module with setuptools.Command-derived classes, checking for a functional gmsh installation.
'''

import subprocess
import platform
import tempfile
from setuptools import Command
from setuptools import distutils
from ..dist import assert_path

class CheckGmsh(Command):
    '''Check gmsh is installed, by trying to find out installed version.

    qmesh requires a functional installation of the gmsh mesh generator to be present on the host
    system. Gmsh is not available through the Python Package Index (PyPI), so the user is required
    to install it separately, perhaps through another package manager. The purpose of this class
    is to ensure gmsh has been installed on the host system and verify the location of the gmsh
    binary (executable). The location of the gmsh binary can be specified by the user as an option.
    Thus, multiple versions of gmsh can be present in the host system, and the user can choose
    which one to use with a qmesh installation. If the location of the gmsh binary is not
    specified, methods in this class will attempt to locate it. Note that the location of the gmsh
    binary is subsequently stored in an egg-info file (see the documentation of
    ``setuptools_qmesh.command.egg-info.write_gmsh_bin_path``). This class is derived from the
    ``setuptools`` Command class, to implement the necessary functionality in a way consistent to
    the ``setuptools`` packaging and distribution design, and to make the necessary checks at
    particular stages during the installation of qmesh packages.

    Technically it is possible to allow a particular command to be run separately, with a
    terminal command, after including a declaration of an entry-point in the call to
    ``setuptools.setup()``. The call arguments include a dictionary ``entry_points`` where a key
    ``distutils.commands`` is mapped to the custom commands. Such commands are specified as a
    list, where each list item bounds a custom command to a class: <command> = <module>:<class>
    The <class> is a derivative of the ``setuptools.Command`` class and the command can be run
    as ``python setup.py <command> <command-options>``. However, pip is a package management tool
    and it runs a very specific set of commands. While it is possible to run custom commands at the
    terminal with pip, it is elaborate to do so. Therefore the present command is intended to be
    run by other methods during installation. Nonetheless, the appropriate declarations in
    ``distutils.commands`` are made, for completeness. A command option named ``gmsh-bin-path`` is
    also introduced, via the ``user_options`` attribute. pip does not seem to facilitate passing
    command-line options to commands when the command is not explicitly run by the user. The user
    option is here included only for completeness and debugging. Otherwise, it is circumvented by
    the ``setuptools-qmesh`` package as follows: The value given with this command-line option
    (``--gmsh-bin-path=/path/to/gmsh``) is stored in a ``setuptools.Command`` attribute named
    ``gmsh_bin_path``, not be confused with the similarly named Distribution object attribute.
    Projects that use setuptools-qmesh are built to look for the command-line option
    ``--gmsh-bin-path``, remove it from the options list and and pass its value to the ``setup()``
    call, setting the value of the Distribution object attribute, also named ``gmsh_bin_path``.
    Methods in this class will then copy the value of the Distribution attribute, or attempt to
    detect a valid gmsh path if the option is absent.
    '''
    description = 'Check gmsh is installed, by trying to find out installed version.'
    user_options = [('gmsh-bin-path=', None, "Path to gmsh binary (executable)"),]
    gmsh_bin_path = None

    def initialize_options(self):
        '''Set command options to default values.

        In addition to the ``setuptools.Command`` attributes, the ``CheckGmsh`` class also defines
        the attribute ``gmsh_bin_path``. According to ``setuptools`` standard practice, a method
        named ``initialize_options`` must initialise all attributes. Therefore, the attribute
        ``gmsh_bin_path`` is initialised in this method, and assigned a ``None`` value.
        '''
        self.gmsh_bin_path = None

    def finalize_options(self):
        '''Set command options to final values, before running.

        The attribute ``gmsh_bin_path`` is set and checked by this method. The attribute
        ``gmsh_bin_path`` of this class should not be confused with the similarly named attribute
        of the distribution object. Packages that use ``setuptools-qmesh`` must scan the command
        line for the option ``--gmsh-bin-path`` and pass its value to the ``setup()`` call, thus
        assigning the distribution ``gmsh_bin_path`` attribute value. The present method will then
        assign the distribution attribute value to the Command (present class) attribute, using the
        following procedure: If the distribution object attribute is not ``None``, its value is
        assigned to the Command object attribute. Otherwise, the host system is probed for a gmsh
        installation. If during probing a gmsh installation is not found an exception is raised.
        The specification of the gmsh binary path is allowed to be the absolute path to the
        directory containing the gmsh binary, or the absolute path including the gmsh binary
        filename at the end. This method will ensure the path including the filename is stored in
        ``gmsh_bin_path`` (e.g. ``/path/to/gmsh``) and then check the path exists.
        '''
        #If the command-line option is not present, try to locate gmsh.
        if self.gmsh_bin_path is None:
            if self.distribution.gmsh_bin_path is None:
                self.announce("No specification of gmsh path is present."+
                              " Will try to detect a gmsh installation", level=distutils.log.ERROR)
                #Raise an exception if gmsh is not found.
                try:
                    if platform.system() == 'Linux' or platform.system() == 'Darwin':
                        gmsh_bin_path = subprocess.check_output(['which', 'gmsh']).decode('utf-8')
                    if platform.system() == 'Windows':
                        gmsh_bin_path = \
                                    subprocess.check_output(['where.exe', 'gmsh']).decode('utf-8')
                except subprocess.CalledProcessError:
                    msg = 'Could not locate a gmsh installation.'
                    self.announce(msg, level=distutils.log.FATAL)
                    msg = 'Qmesh uses gmsh as a mesh generator, hence gmsh must be installed. ' + \
                        msg
                    raise distutils.errors.DistutilsSetupError(msg)
                self.gmsh_bin_path = gmsh_bin_path.strip()
            else:
                self.gmsh_bin_path = self.distribution.gmsh_bin_path
        #Check that given gmsh path is a valid path
        assert_path(self.distribution, 'gmsh_bin_path', self.gmsh_bin_path)

    def run(self):
        '''Run check to ensure gmsh is installed on host system.

        An attempt to find the gmsh version is used as a check, to ensure a functional gmsh
        installation. The location of the gmsh binary is specified through the ``gmsh_bin_path``
        attribute of this Command object and the Distribution object, see the documentation of the
        ``finalize_options`` method.
        '''
        #If the path does not include the filename (gmsh) add it, and check if it exists
        if subprocess.os.path.isdir(self.gmsh_bin_path):
            self.gmsh_bin_path = subprocess.os.path.join(self.gmsh_bin_path, 'gmsh')
            if not subprocess.os.path.isfile(self.gmsh_bin_path):
                msg = 'Could not find gmsh at ' + self.gmsh_bin_path
                self.announce(msg, distutils.log.FATAL)
                raise distutils.errors.DistutilsSetupError(msg)
        #Call `/path/to/gmsh --version` to verify a functional gmsh installation.
        gmsh_stdout = tempfile.TemporaryFile(mode='w+b')
        gmsh_found = subprocess.Popen([self.gmsh_bin_path, '--version'],
                                      stdout=gmsh_stdout, stderr=gmsh_stdout)
        gmsh_found.wait()
        if gmsh_found.returncode != 0:
            msg = 'Could not find gmsh at ' + self.gmsh_bin_path
            self.announce(msg, distutils.log.FATAL)
            raise distutils.errors.DistutilsSetupError(msg)
        gmsh_stdout.seek(0)
        gmsh_version = gmsh_stdout.readline().decode("utf-8")
        self.announce("Found gmsh version " + gmsh_version.strip() +
                      " at " + self.gmsh_bin_path,
                      level=distutils.log.INFO)
        gmsh_stdout.close()
        #Assign the path to self.distribution.gmsh_bin_path, so that the egg writer
        # writes the path.
        self.distribution.gmsh_bin_path = self.gmsh_bin_path
