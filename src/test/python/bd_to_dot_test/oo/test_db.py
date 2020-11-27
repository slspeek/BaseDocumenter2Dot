import logging
import subprocess
import shlex
import os

from pytest import fixture

from bd_to_dot import graph
from bd_to_dot.oo.db import _int_list, loadObjects
from bd_to_dot_test.oo.connect import datasource

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


SOFFICE_CMD = '/opt/libreoffice6.4/program/soffice '\
              '--accept="socket,host=localhost,port=2002;urp;" '\
              '--norestore --nologo --nodefault  --headless'\
              ' {}'
DEFAULT_TESTDB = 'src/test/resources/testdb/BaseDocumenter.odb'


@fixture
def libreoffice():
    testdb = os.getenv("BD_TESTDB", DEFAULT_TESTDB)
    args = shlex.split(SOFFICE_CMD.format(testdb))
    office_proc = subprocess.Popen(args, shell=False)
    logger.debug("LibreOffice started")
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


def test_connection(libreoffice):
    logger.debug(dir(datasource()))
    assert datasource().Name.endswith("BaseDocumenter.odb")


def test_load_objects(libreoffice):
    connection = datasource().getConnection("sa", "")
    objs = loadObjects(connection)
    assert len(objs) == 34
    import pickle
    with open('src/test/resources/objects.pickle', 'wb') as file:
        pickle.dump(objs, file)


def test_view_graph(libreoffice):
    ds = datasource()
    conn = ds.getConnection("sa", "")
    g = graph(conn)
    g.save("src/test/resources/testdb.gv")
    if os.getenv("BD_VIEW", 0):
        g.view()


def test__int_list():
    assert [1, 2, 3] == _int_list("1|2|3")


def test__int_list_empty():
    assert [] == _int_list("")
