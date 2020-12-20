import pickle

from pytest import fixture
from bd_to_dot_test.dot.resource import FIXTURE_DIR


def loadDatabases():
    with open(FIXTURE_DIR.format('databases.pickle'), 'rb') as file:
        dbs = pickle.load(file)
    return dbs


@fixture(scope="module")
def databases():
    yield loadDatabases()


def test_load_databases(databases):
    assert 2 == len(databases)
