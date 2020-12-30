""" Integrations tests for oo.db module """
import logging

import os
import pickle
from pytest import fixture

from bd_to_dot.oo.db import _int_list, load_objects, load_databases
from bd_to_dot import open_connection
from bd_to_dot_test.oo.connect import datasource, start_office
from bd_to_dot_test.dot.resource import TEST_OUTPUT, DEFAULT_TESTDB

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


@fixture(scope="module")
def libreoffice():
    """ A libreoffice running on a test repository """
    testdb = os.getenv("BD_TESTDB", DEFAULT_TESTDB)
    office_proc = start_office(testdb)
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


# pylint: disable=unused-argument,redefined-outer-name
def test_load_objects(libreoffice):
    """ Creates a objects fixture """
    with open_connection(datasource()) as conn:
        objs = load_objects(conn)
    print(objs)
    with open(TEST_OUTPUT.format('objects.pickle'), 'wb') as file:
        pickle.dump(objs, file)
    assert len(objs) == 69


# pylint: disable=unused-argument,redefined-outer-name
def test_load_databases(libreoffice):
    """ Creates a databases fixture """
    with open_connection(datasource()) as conn:
        dbs = load_databases(conn)
    with open(TEST_OUTPUT.format('databases.pickle'), 'wb') as file:
        pickle.dump(dbs, file)
    assert len(dbs) == 2


def test__int_list():
    """ test no empty list """
    assert [1, 2, 3] == _int_list("1|2|3")


def test__int_list_empty():
    """ test empty list """
    assert [] == _int_list("")
