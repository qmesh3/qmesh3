#    Copyright (C) 2013 Alexandros Avdis and others. See the AUTHORS file for a full list of copyright holders.
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
from  qgis.core import QgsApplication
import qmesh3.GFD_basisChangeTools as GFD_basisChangeTools
import qmesh3.vector
import qmesh3.raster
import qmesh3.mesh
import qmesh3.publish
import qmesh3.lib
from qmesh3.config import *
import atexit
import importlib.metadata


# Suppress verbose debugging Qt messages
os.environ['QT_LOGGING_RULES'] = "qt5ct.debug=false"
# Make sure qmesh can run in environments without graphics
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import sys
import shutil
import importlib
import platform


def _check_env():
    # Check for QGIS
    try:
        importlib.import_module('qgis')
    except ModuleNotFoundError:
        print("Error: Host system does not appear to have a qgis installation.")
        print("Qmesh uses qgis for GIS operations.")
        # In runtime, we usually exit or warn rather than raising Distutils errors
        sys.exit(1)

    # Check for GMSH
    gmsh_path = shutil.which("gmsh")
    if not gmsh_path and platform.system() == 'Windows':
        # Fallback check for Windows if not in PATH
        gmsh_path = shutil.which("gmsh.exe")

    if not gmsh_path:
        print("Error: Could not locate a gmsh installation.")
        print("Qmesh uses gmsh as a mesh generator.")
        sys.exit(1)

_check_env()

#Set the version attribute
try:
    __version__ = importlib.metadata.version("qmesh3")
except importlib.metadata.PackageNotFoundError:
    __version__ = "local"
    LOG.warning('Could not find qmesh version information. Provenance information is incomplete.')
# Retrieve the distribution metadata object
try:
    dist = importlib.metadata.distribution("qmesh3")
except importlib.metadata.PackageNotFoundError:
    dist = None
# Set the git-sha-key attribute
__git_sha_key__ = dist.read_text("GIT_SHA_KEY") if dist else None
if not __git_sha_key__:
    __git_sha_key__ = "local"
    LOG.warning('Could not find qmesh origin git SHA key. Provenance information is incomplete.')

# Set the license attribute
__license__ = dist.read_text("LICENSE") if dist else None
if not __license__:
    __license__ = ""
    LOG.warning('Could not find complete license statement. Provenance information is incomplete.')
    LOG.warning('Qmesh is distributed under GPLv3. Please observe the license at .')

# Set the authors attribute
__authors__ = dist.read_text("AUTHORS.md") if dist else None
if not __authors__:
    __authors__ = ""
    LOG.warning('Could not find qmesh authors information. Provenance information is incomplete.')

# Set the gmsh-path attribute
__gmsh_bin_path__ = dist.read_text("GMSH_BIN_PATH") if dist else None
if not __gmsh_bin_path__:
    __gmsh_bin_path__ = "/usr/bin"
    LOG.warning('Could not find gmsh binary path specification. Mesh generation might fail.')

# Set the qgis-install-path attribute
__qgis_path__ = dist.read_text("QGIS_PATH") if dist else None
if not __qgis_path__:
    __qgis_path__ = "/usr/local/"
    LOG.warning('Could not find qgis path specification. qgis initialisation might fail.')
    
#__version__ = "local"
#__git_sha_key__ = "local"
#__license__ = ""
#__authors__ = ""
#__gmsh_bin_path__ = "/usr/bin"
#__qgis_path__ = "/usr/local/"

qgs = None

def _cleanup_qmesh():
    """
    Internal cleanup function. 
    Safe to call multiple times (idempotent).
    """
    global qgs
    # If qgs is already None, we have already cleaned up. Do nothing.
    if qgs is None:
        return

    # Otherwise, shut it down and clear the variable
    qgs.exitQgis()
    qgs = None

def start_qmesh():
    """
    Internal function to auto-start QGIS on import,
    BUT only if it isn't already running.
    """
    global qgs

    # CHECK: Is QGIS already running? (e.g., started by pytest or another lib)
    if QgsApplication.instance():
        qgs = QgsApplication.instance()
        # We do NOT register an exit handler here, because we didn't start it.
        # The test runner or the other library is responsible for closing it.
        return

    # START: If not running, start it now.
    qgs = QgsApplication([], False)
    qgis_install_path='/usr'
    qgs.setPrefixPath(__qgis_path__, True)
    qgs.initQgis()

    # REGISTER CLEANUP: Ensure it closes when the script ends
    atexit.register(qgs.exitQgis)

def stop_qmesh():
    """
    Manually stops QGIS (e.g. for testing teardown).
    """
    # Simply call the safe internal cleanup
    _cleanup_qmesh()


start_qmesh()

