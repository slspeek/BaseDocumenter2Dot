import logging

import os

from pytest import fixture

from bd_to_dot import graph
from bd_to_dot.oo.db import _int_list, loadObjects
from bd_to_dot_test.oo.connect import datasource, startOffice

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


DEFAULT_TESTDB = 'src/test/resources/testdb/BaseDocumenter.odb'


@fixture(scope="module")
def libreoffice():
    testdb = os.getenv("BD_TESTDB", DEFAULT_TESTDB)
    office_proc = startOffice(testdb)
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


def test_connection(libreoffice):
    ds = datasource()
    logger.debug(dir(ds))
    assert ds.Name.endswith("BaseDocumenter.odb")


def test_load_objects(libreoffice):
    connection = datasource().getConnection("sa", "")
    objs = loadObjects(connection)
    import pickle
    with open('src/test/resources/fixtures/objects.pickle', 'wb') as file:
        pickle.dump(objs, file)
    assert len(objs) == 34


def test_view_graph(libreoffice):
    ds = datasource()
    conn = ds.getConnection("sa", "")
    g = graph(conn)
    g.save("src/test/resources/fixtures/testdb.gv")
    if os.getenv("BD_VIEW", 0):
        g.view()


def test__int_list():
    assert [1, 2, 3] == _int_list("1|2|3")


def test__int_list_empty():
    assert [] == _int_list("")
