import logging

import os

from pytest import fixture

from bd_to_dot.oo.db import _int_list, loadObjects, loadDatabases
from bd_to_dot import open_connection
from bd_to_dot_test.oo.connect import datasource, startOffice
from bd_to_dot_test.dot.resource import TEST_OUTPUT, DEFAULT_TESTDB

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


@fixture(scope="module")
def libreoffice():
    testdb = os.getenv("BD_TESTDB", DEFAULT_TESTDB)
    office_proc = startOffice(testdb)
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


def test_load_objects(libreoffice):
    with open_connection(datasource()) as conn:
        objs = loadObjects(conn)
    print(objs)
    import pickle
    with open(TEST_OUTPUT.format('objects.pickle'), 'wb') as file:
        pickle.dump(objs, file)
    assert len(objs) == 69


def test_load_databases(libreoffice):
    with open_connection(datasource()) as conn:
        dbs = loadDatabases(conn)
    import pickle
    with open(TEST_OUTPUT.format('databases.pickle'), 'wb') as file:
        pickle.dump(dbs, file)
    assert len(dbs) == 2


def test__int_list():
    assert [1, 2, 3] == _int_list("1|2|3")


def test__int_list_empty():
    assert [] == _int_list("")
