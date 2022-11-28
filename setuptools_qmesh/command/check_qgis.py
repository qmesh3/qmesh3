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
''' Module with setuptools.Command-derived classes, checking for a functional qgis installation.
'''

import os
import subprocess
import importlib
from setuptools import Command
from setuptools import distutils
from ..dist import assert_path

class CheckQgis(Command):
    '''Check qgis is installed.

    qmesh requires a functional installation of Qgis and the Qgis Python API to be present on the
    host system. Qgis and its Python API are not available through the Python Package Index
    (PyPI), so the user has to install them separately, perhaps through another package manager.
    The purpose of this class is to ensure Qgis and its Python API have been installed on the host
    system, and to verify their installation path, during installation of qmesh packages. The qgis
    installation path can be specified by the user as an option. If the path is not specified,
    methods in this class will attempt to locate it. Note that the qgis installation path is
    subsequently stored in an egg-info file (see the documentation of
    ``setuptools_qmesh.command.egg-info.write_qgis_path``). This class is derived from the
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
    ``distutils.commands`` are made, for completeness. A command option named ``qgis-path`` is
    also introduced, via the ``user_options`` attribute. pip does not seem to facilitate passing
    command-line options to commands when the command is not explicitly run by the user. The user
    option is here included only for completeness and debugging. Otherwise, it is circumvented by
    the ``setuptools-qmesh`` package as follows: The value given with this command-line option
    (``--qgis-path=/path/to/qgis``) is stored in a ``setuptools.Command`` attribute named
    ``qgis_path``, not be confused with the similarly named Distribution object attribute.
    Projects that use setuptools-qmesh are built to look for the command-line option
    ``--qgis-path``, remove it from the options list and and pass its value to the ``setup()``
    call, setting the value of the Distribution object attribute, also named ``qgis_path``.
    Methods in this class will then copy the value of the Distribution attribute, or attempt to
    detect a valid qgis path if the option is absent.
    '''
    description = 'Check qgis is installed.'
    user_options = [('qgis-path=', None, "Path to qgis installation"),]
    qgis_path = None

    def initialize_options(self):
        '''Set command options to default values.

        In addition to the ``setuptools.Command`` attributes, the ``CheckQgis`` class also defines
        the attribute ``qgis_path``. According to ``setuptools`` standard practice, a method
        named ``initialize_options`` must set all attributes to an acceptable value. Therefore,
        the attribute ``qgis_path`` is given its default value in this method, ``None``.
        '''
        self.qgis_path = None

    def finalize_options(self):
        '''Set command options to final values, before running.

        The attribute ``qgis_path`` is set and checked by this method. The attribute
        ``qgis_path`` of this class should not be confused with the similarly named attribute
        of the distribution object. Packages that use ``setuptools-qmesh`` must scan the command
        line for the option ``--qgis-path`` and pass its value to the ``setup()`` call, thus
        assigning the distribution ``qgis_path`` attribute value. The present method will then
        assign the distribution attribute value to the Command (present class) attribute, using the
        following procedure: If the distribution object attribute is not ``None``, its value is
        assigned to the Command object attribute. Otherwise, the host system is probed for a qgis
        installation. If during probing a qgis installation is not found an exception is raised.
        '''
        #If the qgis_path attribute is not set, use the path specified by the distribution
        # attribute (via the setup.py file). If the distribution attribute is also None, try to
        # import qgis and figure out the path to the qgis installation tree.
        if self.qgis_path is None:
            if self.distribution.qgis_path is None:
                self.announce("No specification of qgis path is present."+
                              " Will try to detect a qgis installation", level=distutils.log.ERROR)
                try:
                    qgis = importlib.import_module('qgis')
                    qgis_python_path = qgis.__path__[0]
                    qgis_bin_path = subprocess.check_output(['which', 'qgis']).decode('utf-8')
                    qgis_path = '/'
                    for python_element, bin_element in zip(qgis_python_path.split('/'),
                                                           qgis_bin_path.split('/')):
                        if python_element == bin_element:
                            qgis_path = subprocess.os.path.join(qgis_path, python_element)
                        else:
                            break
                    self.qgis_path = qgis_path
                except ModuleNotFoundError:
                    msg = 'Host system does not appear to have a qgis installation.'
                    self.announce(msg, level=distutils.log.FATAL)
                    msg = 'Qmesh uses qgis for GIS operations, hence qgis must be installed. ' + msg
                    raise distutils.errors.DistutilsPlatformError(msg)
            else:
                self.qgis_path = self.distribution.qgis_path
        #Check that given qgis_path is a valid path
        assert_path(self.distribution, 'qgis-path', self.qgis_path)

    def run(self):
        '''Run check to ensure qgis is installed on host system.

        An attempt to find the qgis version is used as a check, to ensure a functional qgis
        installation. The location of the qgis installation tree is specified through the
        ``qgis_path`` attribute of this Command object and the Distribution object, see
        ``finalize_options`` doc-string.
        '''
        self.distribution.announce('Looking for qgis installation at ' + self.qgis_path,
                                   level=distutils.log.INFO)
        try:
            # Suppress verbose debugging Qt messages
            os.environ['QT_LOGGING_RULES'] = "qt5ct.debug=false"
            # Make sure qmesh can run in environments without graphics
            os.environ["QT_QPA_PLATFORM"] = "offscreen"
            # Import and initialise qgis. We are not using a simple import statement to
            # import qgis as it is not a dependency
            qgis_core = importlib.import_module('qgis.core')
            qgis_app = qgis_core.QgsApplication([], False)
            qgis_app.setPrefixPath(self.qgis_path, True)
            qgis_app.initQgis()
            #From qgis2 to qgis3 the location of QGIS_VERSION changed
            try:
                qgis_version = qgis_core.QGis.QGIS_VERSION
            except AttributeError:
                qgis_version = qgis_core.Qgis.QGIS_VERSION
            self.distribution.announce('Found QGIS version ' + qgis_version + ' at ' +
                                       self.qgis_path, level=distutils.log.INFO)
        except ModuleNotFoundError:
            msg = 'Could not find qgis at ' + self.qgis_path
            self.announce(msg, level=distutils.log.FATAL)
            distutils.errors.DistutilsPlatformError(msg)
        #Assign the path to self.distribution.qgis_path, so that the egg writer
        # writes the path.
        self.distribution.qgis_path = self.qgis_path
