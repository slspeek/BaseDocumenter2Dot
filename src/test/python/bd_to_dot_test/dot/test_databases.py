""" Provides fixuture for DATABASES table from repository """
import pickle

from pytest import fixture
from bd_to_dot_test.dot.resource import FIXTURE_DIR


def load_databases_from_file():
    """ loads Databases from fixuture """
    with open(FIXTURE_DIR.format('databases.pickle'), 'rb') as file:
        dbs = pickle.load(file)
    return dbs


@fixture(scope="module")
def databases():
    """ Returns a list of Database objects """
    yield load_databases_from_file()


def test_load_databases(databases):  # pylint: disable=redefined-outer-name
    """ Two test databases """
    assert len(databases) == 2
