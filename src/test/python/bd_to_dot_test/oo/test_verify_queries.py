""" Integration tests for the querie verification """
import logging
from pytest import fixture

from bd_to_dot import verify_queries
from bd_to_dot_test.oo.connect import datasource, start_office

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


BROKEN_DB = 'src/test/resources/testdb/testdb_broken_query.odb'
TEST_DB = 'src/test/resources/testdb/testdb.odb'


@fixture
def broken_db():
    """ LibreOffice on a broken database """
    office_proc = start_office(BROKEN_DB)
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


@fixture
def normal_testdb():
    """ LibreOffice on a working database """
    office_proc = start_office(TEST_DB)
    yield office_proc
    office_proc.terminate()
    logger.debug("LibreOffice killed")


# pylint: disable=unused-argument,redefined-outer-name
def test_verify_queries_broken(broken_db):
    """ Find the error in the broken test database """
    assert len(verify_queries(datasource())) == 1


# pylint: disable=unused-argument,redefined-outer-name
def test_verify_queries(normal_testdb):
    """ See that all queries run without errors """
    assert len(verify_queries(datasource())) == 0
