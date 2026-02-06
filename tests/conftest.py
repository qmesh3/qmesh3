import pytest
from qgis.core import QgsApplication
import qmesh3

# scope='session' means this runs ONCE for the entire test suite
# autouse=True means it runs automatically, even for unittest classes
@pytest.fixture(scope='session', autouse=True)

def qgis_setup():
    print("Initializing QGIS for testing...", flush=True)
    
    # Explicitly ensure QMesh is started. 
    # Even though 'import qmesh3' did this, being explicit documents 
    # that this fixture relies on the application being active.
    qmesh3.start_qmesh()

    # Yield control back to the tests
    yield
    
