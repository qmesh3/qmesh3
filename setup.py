#!/usr/bin/env python
#
#    Copyright (C) 2013 Alexandros Avdis and others.
#    See the AUTHORS.md file for a full list of copyright holders.
#
#    This file is part of QMesh.
#
#    QMesh is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    QMesh is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QMesh.  If not, see <http://www.gnu.org/licenses/>.

import os
import io
from setuptools import setup
import platform
from setuptools import distutils
import importlib
import subprocess

# Suppress verbose debugging Qt messages
os.environ['QT_LOGGING_RULES'] = "qt5ct.debug=false"
# Make sure qmesh can run in environments without graphics
os.environ["QT_QPA_PLATFORM"] = "offscreen"

def main():
    current_directory = os.path.dirname(__file__)
    # Read version from file. The variable storing the
    # version identifier is passed into a standardised argument of 
    # setuptools.setup
    ##version_path = os.path.join(current_directory, 'VERSION')
    ##with io.open(version_path, encoding='utf-8') as version_file:
        ##qmesh_version = version_file.readline().strip()
    # Read long description from file. The variable storing the
    # long description is passed into a standardised argument of 
    # setuptools.setup
    readme_path = os.path.join(current_directory, 'README.rst')
    with io.open(readme_path, encoding='utf-8') as readme_file:
        long_description = readme_file.read()
    check_env()
        
    setup(
          name='qmesh3',
          version='1.0.4',
          description = "Finite Element meshes from GIS data.",
          long_description = long_description,
          author = "The QMesh Development Team.",
          author_email = "develop@qmesh.org",
          url = "http://www.qmesh.org",
          download_url = 'https://github.com/acse-ra2617/qmesh3/releases/tag/1.0.3',
          packages = ['qmesh3',
                      'qmesh3.lib',
                      'qmesh3.vector',
                      'qmesh3.mesh',
                      'qmesh3.raster',
                      'qmesh3.publish',
                     ],
          package_dir = {
              'qmesh3': 'qmesh3',
              'qmesh3.lib':'qmesh3/lib',
              'qmesh3.vector':'qmesh3/vector',
              'qmesh3.meshg':'qmesh3/mesh',
              'qmesh3.raster':'qmesh3/raster',
              'qmesh3.publish':'qmesh3/publish',
              'setuptools_qmesh': 'setuptools_qmesh',
              },
          scripts=["qmesh-cli/qmesh"],
          provides=['qmesh3'],
          install_requires=['gitpython'],
          setup_requires=['setuptools>=35.0.0'],
          include_git_sha_key=True,
          include_full_license=True,
          include_author_ids=True,
          license='GPLv3',
          test_suite = "tests",
          keywords = ['GIS', 'mesh generation'],
        )

# check the right tools are installed
def check_env():
    msg = ""
    try:
        qgis = importlib.import_module('qgis')
        qgis_python_path = qgis.__path__[0]
        qgis_path = '/'
    except ModuleNotFoundError:
        msg = 'Host system does not appear to have a qgis installation.'
        msg = 'Qmesh uses qgis for GIS operations, hence qgis must be installed. ' + msg
        raise distutils.errors.DistutilsPlatformError(msg)

    try:
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            gmsh_bin_path = subprocess.check_output(['which', 'gmsh']).decode('utf-8')
        if platform.system() == 'Windows':
            gmsh_bin_path = subprocess.check_output(['where.exe', 'gmsh']).decode('utf-8')
    except subprocess.CalledProcessError:
        msg = 'Could not locate a gmsh installation.'
        msg = 'Qmesh uses gmsh as a mesh generator, hence gmsh must be installed. ' + msg
        raise distutils.errors.DistutilsSetupError(msg)

if __name__=='__main__':
    main()
