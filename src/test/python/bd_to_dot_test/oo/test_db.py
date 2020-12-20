import logging

import os

from pytest import fixture

from bd_to_dot.oo.db import _int_list, loadObjects, loadDatabases
from bd_to_dot_test.oo.connect import datasource, startOffice
from bd_to_dot_test.dot.resource import TEST_OUTPUT

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


DEFAULT_TESTDB = 'src/test/resources/testdb/BaseDocumenter-test-output.odb'


@fixture(scope="module")
def libreoffice():
    testdb = os.getenv("BD_TESTDB", DEFAULT_TESTDB)
    office_proc = startOffice(testdb)
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


def test_load_objects(libreoffice):
    connection = datasource().getConnection("sa", "")
    objs = loadObjects(connection)
    connection.close()
    connection.dispose()
    print(objs)
    import pickle
    with open(TEST_OUTPUT.format('objects.pickle'), 'wb') as file:
        pickle.dump(objs, file)
    assert len(objs) == 69


def test_load_databases(libreoffice):
    connection = datasource().getConnection("sa", "")
    dbs = loadDatabases(connection)
    connection.close()
    connection.dispose()
    import pickle
    with open(TEST_OUTPUT.format('databases.pickle'), 'wb') as file:
        pickle.dump(dbs, file)
    assert len(dbs) == 2


def test__int_list():
    assert [1, 2, 3] == _int_list("1|2|3")


def test__int_list_empty():
    assert [] == _int_list("")
