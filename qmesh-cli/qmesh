#!/usr/bin/env python3

#    Copyright (C) 2013 Alexandros Avdis and others. See the AUTHORS file for a full list of copyright holders.
#
#    This file is part of qmesh-cli.
#
#    qmesh-cli is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    qmesh-cli is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QMesh.  If not, see <http://www.gnu.org/licenses/>.

import os
import numpy as np
import argparse
import sys
import logging
import qmesh3 as qmesh
LOG = logging.getLogger('qmesh')

def outputGridShapeArgument(s):
    #TODO: What is the argument 's' here?
    '''Definition used in argument parsing, to facilitate
    argument specification. It allows the resolution
    of the output mesh to be specified as a slash-delimited
    pair.'''
    try:
        outputXiLength, outputEtaLength = list(map(int , s.split('/')))
        return outputXiLength, outputEtaLength
    except:
        raise argparse.ArgumentTypeError('Output grid shape must be specified as a slash-delimited pair.')

def main():
    """ Parse command-line arguments and execute the user-chosen subcommand. """
    
    parser = argparse.ArgumentParser(prog="qmesh", description="Create meshes from GIS data")
                     
    # General qmesh options, to be specified before any sub-commands.
    parser.add_argument("-l", "--log_file", action="store", type=str, metavar="PATH", default=None, help="Log to a file with a given path.")
    parser.add_argument("-v", "--verbosity", action="store", type=str, metavar="LEVEL", default="info", choices=['critical', 'error', 'warning', 'info', 'debug'], help="Log verbosity level.")
    
    # The available sub-commands.
    subparsers = parser.add_subparsers(help='sub-command help',dest='cmd')
    subparsers.required=True
    
    # Add a subparser for shapefile-to-gmsh conversion, with some help and a command
    parser_cm_generate_mesh = subparsers.add_parser('generate_mesh', help='Create a geo and mesh files from line and polygon shapefiles and raster files')
    parser_cm_generate_mesh.add_argument('input_file', 
                           type=str, 
                           help='Name of line-shapefile containing all domain boundaries.')
    parser_cm_generate_mesh.add_argument('output_file', 
                           type=str, 
                           help='Output stub name. .msh, .geo and .fld files will be created accordingly.')
    parser_cm_generate_mesh.add_argument('--tcs',
                           '-t',
                           dest='tcs', 
                           default=None,
                           help='Coordinate Reference System of target file (output). Default is PCC')
    parser_cm_generate_mesh.add_argument('--radius', 
                           dest='surfaceRadius', 
                           action='store', 
                           type=float, 
                           default=6.37101e+6, 
                           help='Planet surface radius, to be used in conjuction with planet-centred Cartesian coordinate systems, otherwise ignored.')
    parser_cm_generate_mesh.add_argument('--default_PhysID', 
                           dest='default_PhysID',
                           type=int,
                           default=666,
                           help='Default Physical ID of lines without one. Default is 666')
    parser_cm_generate_mesh.add_argument('--isGlobal', 
                           default=False,
                           action='store_true',
                           help='Global domain? If so, this will ensure the edges are wrapped up nicely')
    parser_cm_generate_mesh.add_argument('--onlyWrite', 
                           default=False,
                           action='store_true',
                           help='Only write the geo and fld file. No mesh is generated.')
    parser_cm_generate_mesh.add_argument('--gmshAlgo', 
                           default='del2d',
                           action='store',
                           choices=['del2d','frontal','adapt'],
                           help='Only write the geo and fld file. No mesh is generated.')
    parser_cm_generate_mesh.add_argument('--smallestMeshArea', 
                           '-s',
                           type=float, 
                           default=0.0, 
                           help='The smallest surface to mesh. Set this high to not mesh lakes.')
    parser_cm_generate_mesh.add_argument('--surfacePhysID', 
                           type=int,
                           default=1,
                           help='Physical ID of the physical surface(s). Default is 1')
    parser_cm_generate_mesh.add_argument('--qgis-install-path', 
                           dest='qgis_install_path', 
                           action='store', 
                           default='/usr', 
                           help='Prefix-path used in QGIS installation. Usually "/usr"')
    parser_cm_generate_mesh.add_argument('--raster-crs','-rcrs', 
                           dest='rasterInputCRS', 
                           action='store', 
                           default=None, 
                           help='Coordinate Reference System of the mesh-metric raster')
    parser_cm_generate_mesh.add_argument('--mesh-metric-raster','-r', 
                           dest='meshMetricRasterFile', 
                           action='store', 
                           default=None, 
                           help='Raster file storing the mesh-element-size.')
    parser_cm_generate_mesh.add_argument('--polygon','-p',
                           dest='polygon', 
                           action='store', 
                           default='', 
                           help='Polygon file containing surface IDs. Must match line-shapefile exactly.')
    parser_cm_generate_mesh.set_defaults(func=generate_mesh)

    # Add subparser for conversion of rasters to gmsh-fieds
    parser_cm_rst2fld = subparsers.add_parser('rst2fld',
            help = 'Convert raster file into gmsh field')
    parser_cm_rst2fld.add_argument('inputRasterFilename', 
                            metavar='inputRasterFilename', 
                            type=str, 
                            help='Name of raster file.')
    parser_cm_rst2fld.add_argument('outputFilename', 
                           metavar='outputFilename', 
                           type=str, 
                           help='Name of gmsh field file')
    parser_cm_rst2fld.add_argument('--scs', 
                           '-s',
                           dest='sourceCoordReferenceSystem', 
                           action='store', 
                           help='Coordinate Reference System of source files (input)')
    parser_cm_rst2fld.add_argument('--tcs', 
                           '-t',
                           dest='targetCoordReferenceSystem', 
                           action='store', 
                           help='Coordinate Reference System of target file (output)')
    parser_cm_rst2fld.add_argument('--qgis-install-path', 
                           dest='qgis_install_path', 
                           action='store', 
                           default='/usr', 
                           help='Prefix-path used in QGIS installation. Usually "/usr"')
    parser_cm_rst2fld.set_defaults(func=rst2fld)
 
    #Add subparser for displaying license.
    parser_cm_display_license = subparsers.add_parser('license',
            help = 'Display the license.')
    parser_cm_display_license.set_defaults(func=display_license)

    #Add subparser for displaying version.
    parser_cm_display_version = subparsers.add_parser('version',
            help = 'Display the version.')
    parser_cm_display_version.set_defaults(func=display_version)

    #Add subparser for displaying git sha key.
    parser_cm_display_git_sha_key = subparsers.add_parser('git_sha_key',
            help = 'Display the git sha key, of the installed copy.')
    parser_cm_display_git_sha_key.set_defaults(func=display_git_sha_key)

    # Parse the arguments, and strip out the common options
    args = parser.parse_args()
    
    # Set up the log file handler, if necessary.
    if(args.log_file):
      LOG.set_output_file(args.log_file)
      
    # Set the log verbosity level to something other than the default, if necessary.
    if(args.verbosity):
      LOG.setLevel(args.verbosity.upper())
      
    # All of the rest may or may not apply to the command chosen
    # The rest of this function is effectively checking all of the arguments
    # against the command specified
    # Each command is given a function to execute via the "set_default" argument
    func = args.func
    func(args)

#--------------------------------------------------------------------#
# ----------     Functions proper from here on in       -------------#
#--------------------------------------------------------------------#
def generate_mesh(args):
    """ Generate the Gmsh mesh. """
    
    LOG.info("Generating mesh...")

    # Initialise QGIS
    boundary_file = args.input_file
    polygon_file = args.polygon
    default_PhysID = args.default_PhysID
    isGlobal = args.isGlobal
    smallestMeshArea = args.smallestMeshArea
    surfacePhysID = args.surfacePhysID
    outputFilename = args.output_file
    tcs = args.tcs
    meshMetricRasterFile = args.meshMetricRasterFile
    onlyWriteFiles = args.onlyWrite
    gmshAlgo = args.gmshAlgo

    # Read in and sort-out the domain boundary geometry
    boundaries = qmesh.vector.Shapes()
    boundaries.fromFile(boundary_file)
    boundaries.writeInfo()
    if polygon_file == "":
        loopShapes = qmesh.vector.identifyLoops(boundaries,
                    isGlobal=isGlobal, defaultPhysID=default_PhysID,
                    fixOpenLoops=True)
        polygonShapes = qmesh.vector.identifyPolygons(loopShapes,
            isGlobal=isGlobal, smallestMeshedArea=smallestMeshArea, 
            meshedAreaPhysID = surfacePhysID)
    else:
        polygonShapes = boundaries.fromFile(polygon_file)
        
    # Read in the mesh-element-size metric, if provided
    if meshMetricRasterFile != None:
        meshMetricRaster = qmesh.raster.raster()
        meshMetricRaster.fromFile(meshMetricRasterFile)
        
    # Create domain object.
    domain = qmesh.mesh.Domain()
    domain.setGeometry(loopShapes, polygonShapes)
    geoFilename = outputFilename+'.geo'
    if tcs != None:
        domain.setTargetCoordRefSystem(tcs)
    else:
        msg = 'Please specify output Reference Coordinate System.\n'
        raise Exception(msg)
    if meshMetricRasterFile != None:
        domain.setMeshMetricField(meshMetricRaster)
        fldFilename = outputFilename+'.fld'
    else:
        fldFilename = None
        
    # Write gmsh files and generate mesh
    LOG.info("Writing gmsh files...")
    if onlyWriteFiles == True:
        domain.writeGmshFiles(geoFilename, \
                              fldFilename)
    else:
        mshFilename= outputFilename+'.msh'
        domain.gmsh(geoFilename, \
                    fldFilename, \
                    mshFilename, \
                    gmshAlgo)
       

def rst2fld(args):
    """ Write raster data to a field. """
    # Initialise QGIS
    inputRasterFilename = args.inputRasterFilename
    outputFilename = args.outputFilename
    sourceCoordReferenceSystem = args.sourceCoordReferenceSystem
    targetCoordReferenceSystem = args.targetCoordReferenceSystem
    qgis_install_path = args.qgis_install_path

    raster = qmesh.raster.meshMetricTools.raster()
    raster.fromFile(inputRasterFilename)
    if not targetCoordReferenceSystem == None:
        if (sourceCoordReferenceSystem == None and
            raster.getCoordRefSystem() == None):
                LOG.exception("You need to specify a source coordinate system using -s_crs")
                return
        else:
            raster.changeCoordRefSystem(targetCoordReferenceSystem)
    
    # Write the field to file. 
    raster.writefld(outputFilename,targetCoordReferenceSystem)
    return

def display_license(args):
    """ Print out the license. """
    license = qmesh.get_license()
    LOG.info(license)

def display_version(args):
    """ Print out the version of qmesh currently in use. """
    version = qmesh.get_version()
    LOG.info(version)

def display_git_sha_key(args):
    """ Print out the Git SHA-1 hash of the qmesh Git repository. """
    git_sha_key = qmesh.get_git_sha_key()
    LOG.info(git_sha_key)

if __name__=='__main__':
    main()
