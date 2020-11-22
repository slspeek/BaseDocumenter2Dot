import pickle
from pytest import fixture


@fixture
def objects():
    with open('src/test/resources/objects.pickle', 'rb') as file:
        objs = pickle.load(file)

    yield objs


def test_load_objects(objects):
    assert 34 == len(objects)
