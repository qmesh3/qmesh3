# qmesh3

Qmesh3 has been created as a temporary solution to allow qmesh to function with python3 and QGIS3 within a functional pip install to facilitate users access until the original qmesh updates are released. This repository has been created by [Raul Adriaensen](https://www.linkedin.com/in/rauladriaensen/), contact email can be found [here](https://www.imperial.ac.uk/people/raul.adriaensen17).

qmesh is a software package for creating high-quality meshes using [QGIS](https://www.qgis.org) and [Gmsh](https://geuz.org/gmsh).
The meshes can be used in finite element numerical models such as [TELEMAC](http://www.opentelemac.org), [Fluidity](https://www.fluidity-project.org) and [Thetis](https://thetisproject.org/).
For more information please visit the project [website](https://www.qmesh.org).

## Development, Maintenance and Licence

qmesh was developed and is maintained by [Alexandros Avdis](https://orcid.org/0000-0002-2695-3358) and [Jon Hill](https://orcid.org/0000-0003-1340-4373).
Please see file [AUTHORS.md](https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/AUTHORS.md) for more information.

qmesh is an open-source project distributed under the GNU General Public Licence v3 ([GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)).
The file [LICENCE](https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/LICENSE) contains a complete copy of the licence.

The source code is freely available to download and adapt, under the conditions stated in the [LICENCE](https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/LICENSE) file.

If you wish to contribute, please fork the main repository, create a branch, make your alterations and additions, then create a pull request with your changes. The team will then review the code and commit it to the main repository.

## Documentation

You can access relevant documentation through the following avenues:

* The [qmesh website](https://www.qmesh.org).
* The [qmesh synoptic manual](https://qmesh-synoptic-manual.readthedocs.io/en/latest).

## Walk Through

### Installation

1. Install [gmsh](https://installati.one/ubuntu/20.04/gmsh/)
2. Install [qgis](https://qgis.org/en/site/forusers/alldownloads.html), this installs the newest stable version of QGIS.
   * Some people seem to have more success first doing `sudo apt update` and then `sudo apt install qgis`. This installs the available QGIS version on the system, which for WSL currently seems to be 3.10.14. For version info pre-installation, see [here](https://itsfoss.com/apt-install-specific-version/).
3. Install qmesh3
   * "Not found QGIS" errors are likely caused by multiple python versions installed locally. This can be solved by adding `/usr/bin` (or the location where your QGIS installation lives) to your `PYTHONPATH`.

```bash
git clone [https://github.com/qmesh3/qmesh3.git](https://github.com/qmesh3/qmesh3.git)
cd qmesh3
python3 -m venv --system-site-packages .qmesh
source .qmesh/bin/activate
pip install .
