import logging
import subprocess
import shlex

from pytest import fixture

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


SOFFICE_CMD = '/opt/libreoffice6.4/program/soffice '\
              '--accept="socket,host=localhost,port=2002;urp;" '\
              '--norestore --nologo --nodefault  --headless'\
              ' src/test/resources/testdb/BaseDocumenter.odb'


@fixture
def libreoffice():
    office_proc = subprocess.Popen(shlex.split(SOFFICE_CMD), shell=False)
    logger.debug("LibreOffice started")
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


def test_connection(libreoffice):
    from connect import datasource
    logger.debug(dir(datasource()))
    assert datasource().Name.endswith("BaseDocumenter.odb")


def test_load_objects(libreoffice):
    from connect import datasource
    connection = datasource().getConnection("sa", "")
    from bd_to_dot.oo.db import loadObjects
    objs = loadObjects(connection)
    assert len(objs) == 34
    import pickle
    with open('src/test/resources/objects.pickle', 'wb') as file:
        pickle.dump(objs, file)
