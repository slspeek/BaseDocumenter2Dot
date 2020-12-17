import logging
import subprocess
import shlex

from pytest import fixture

from bd_to_dot import verify_queries
from bd_to_dot_test.oo.connect import datasource

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


SOFFICE_CMD = '/opt/libreoffice6.4/program/soffice '\
              '--accept="socket,host=localhost,port=2002;urp;" '\
              '--norestore --nologo --nodefault  --headless'\
              ' {}'
BROKEN_DB = 'src/test/resources/testdb/testdb_broken_query.odb'


@fixture(scope="module")
def broken_db():
    args = shlex.split(SOFFICE_CMD.format(BROKEN_DB))
    office_proc = subprocess.Popen(args, shell=False)
    logger.debug("LibreOffice started")
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


def test_verify_queries_broken(broken_db):
    assert len(verify_queries(datasource())) == 1
