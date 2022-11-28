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

'''Various functions bound to keyword arguments in setup.py

The map ``entry_points`` in ``setuptools.setup`` contains a ``distutils.setup_keywords``
key, to allow additions of custom keyword arguments. The key ``distutils.setup_keywords``
maps to a list of strings, written as ``<keyword> = <module.function>``. Evidently these
strings define the new keyword arguments and bound each argument to a function. The
functions are defined in the present module. Typically, the functions perform checks on the
keyword value, and then run instances of ``setuptools.Command``, as needed.
'''

from os import path
from setuptools import distutils

def assert_path(dist, attr, value):
    '''Assert attribute describes a valid path.

       Various keyword variables, in calls to ``setuptools.setup``, allow the specification
       of paths where other qmesh packages should look for resources, such as third-party
       packages. This function asserts the value of such keywords is a string describing a
       valid path.

       Args:
           dist (setuptools.Distribution): The ``Distribution`` instance of ``setuptools``,
               orchestrating the installation or packaging procedure.
           attr (str): The name of the attribute, specified as a keyword argument in
               ``setuptools.setup`` calls.
           value (str): The value of the attribute (keyword), which should be a gmsh path.
       Raises:
           DistutilsSetupError: If the keyword value is not a valid path.
    '''
    if not path.exists(value):
        msg = "%r must be a path (%r is not a path)" % (attr, value)
        dist.announce(msg, distutils.log.FATAL)
        raise distutils.errors.DistutilsSetupError(msg)
