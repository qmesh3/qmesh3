qmesh3 
=======
Qmesh3 has been created as a temporary solution to allow qmesh to function with python3 and QGIS3 within a functional pip install to facilitate users access until the original qmesh updates are released. This repository has been created by `Raul Adriaensen <https://www.linkedin.com/in/rauladriaensen/>`_ , contact email can be found `here <https://www.imperial.ac.uk/people/raul.adriaensen17>`_

qmesh is a software package for creating high-quality meshes using `QGIS <https://www.qgis.org>`_ and `Gmsh <https://geuz.org/gmsh>`_.
The meshes can be used in finite element numerical models such as `TELEMAC <http://www.opentelemac.org>`_, `Fluidity <https://www.fluidity-project.org>`_ and `Thetis <https://thetisproject.org/>`_.
For more information please visit the project `website <https://www.qmesh.org>`_.



Development, Maintenance and Licence
------------------------------------

qmesh was developed and is maintained by `Alexandros Avdis <https://orcid.org/0000-0002-2695-3358>`_ and `Jon Hill  <https://orcid.org/0000-0003-1340-4373>`_.
Please see file `AUTHORS.md <https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/AUTHORS.md>`_ for more information.

qmesh is an open-source project distributed under the GNU General Public Licence v3 (`GPL v3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_).
The file `LICENCE <https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/LICENSE>`_ contains a complete copy of the licence.

The source code is freely available to download and adapt, under the conditions stated in the `LICENCE <https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/LICENSE>`_ file.

If you wish to contribute, please fork the main repository, create a branch, make your alterations and additions, then create a pull request with your changes. The team will then review the code and commit it to the main respitory.

Documentation 
---------------

You can access relevant documentation through the following avenues:

* The `qmesh website <https://www.qmesh.org>`_.
* The `qmesh synoptic manual <https://qmesh-synoptic-manual.readthedocs.io/en/latest>`_.

Walk Through
---------------

*Installation*:

1. install `GD-basisChangeTools/ <https://pypi.org/project/GFD-basisChangeTools/>`_
2. install `gmsh <https://installati.one/ubuntu/20.04/gmsh/>`_
3. install `qgis <https://qgis.org/en/site/forusers/alldownloads.html>`_, this installs the newest stable version of QGIS 
   
   - some people seem to have more success first doing "sudo apt update"\" and then "Sudo apt install qgis", this installs the available QGIS version on the system, which for WSL currently seems to be 3.10.14, for version info pre installation see `here <https://itsfoss.com/apt-install-specific-version/>`_, 
4. install `qmesh3 <https://pypi.org/project/qmesh3/>`_
   
   - not found QGIS errors, likely caused by multiple python versions installed locally, can be solved by adding /usr/bin (or the location where your qgis installation lives) to your Pythonpath
5. testing installation (optional) > "python -m unittest discover <test_directory>"

*tutorials*:

All key data files and videos have been placed together under this `Onedrive <https://1drv.ms/u/s!AglgFElvf_OWl8gIx0FxAIcdOhUv8g?e=VrIak0>`_. . A brief description of the files:

-   `Semi automated Mesh Generation of the Coastal Oceans with Engineering Structures Using Satellite Data <https://www.dropbox.com/s/1bwrwjl51cnhhju/Semi-automated%20Mesh%20Generation%20of%20the%20Coastal%20Oceans%20with%20Engineering%20Structures%20Using%20Satellite%20Data.pdf?dl=0>`_
   - great tutorial to get started, this was originally run on docker but can now be done without if the above installation is followed
- additioanl_tutorials_and_docker_installation
   - this material helped me to get going and explore all the options from the docker, qmesh-cli and learn some qgis tricks
- installating_qmesh_manually
   - in case the pip install breaks, instructions on how to setup qmesh manually can be found here
- tutorials_Angeloudis_Athnasios
   - an additional set of tutorials shared 
  
Please read the relevant readme files in the OneDrive and the email chains to find the full information and names of those who kindly put all this content together

bugs to fix
---------------
- Currently runs until it saves the created mesh, but fails to convert this mesh into a shapefile again. This is due it being build on gmsh 2 and not 4 which uses a fileformat which maybe cannot be read by the program anymore,  possible solutions are:
   - remove assert satement on line 927 in qmesh/mesh/mesh.py and hope the rest of the code can deal with the new mesh format
   - fix implementation adapted for the new file format version
