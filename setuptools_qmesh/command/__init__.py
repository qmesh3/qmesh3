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
''' Command sub-module of the setuptools-qmesh package.

Module with extensions to setuptools.setup package. The extensions also
enable command-line extensions to the setup.py scripts. This module
includes commands that:
Check for a qgis installation
Check for a gmsh installation
Check and install non-PyPI Python packages (currently pyrdm)
Egg-info (file) writers that contain the qmesh licence, version number,
author/maintainer details and git sha key.
'''
