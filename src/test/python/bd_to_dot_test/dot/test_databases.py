import pickle

from pytest import fixture


def loadDatabases():
    with open('src/test/resources/fixtures/databases.pickle', 'rb') as file:
        dbs = pickle.load(file)
    return dbs


@fixture(scope="module")
def databases():
    yield loadDatabases()


def test_load_databases(databases):
    assert 2 == len(databases)
