import logging
from pytest import fixture

from bd_to_dot import verify_queries
from bd_to_dot_test.oo.connect import datasource, startOffice

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


BROKEN_DB = 'src/test/resources/testdb/testdb_broken_query.odb'
TEST_DB = 'src/test/resources/testdb/testdb.odb'


@fixture
def broken_db():
    office_proc = startOffice(BROKEN_DB)
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


@fixture
def normal_testdb():
    office_proc = startOffice(TEST_DB)
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


def test_verify_queries_broken(broken_db):
    assert len(verify_queries(datasource())) == 1


def test_verify_queries(normal_testdb):
    assert len(verify_queries(datasource())) == 0
