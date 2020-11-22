import pickle
from pytest import fixture
from bd_to_dot.dot.renderer import verify_relationships


@fixture
def objects():
    with open('src/test/resources/objects.pickle', 'rb') as file:
        objs = pickle.load(file)

    yield objs


def test_load_objects(objects):
    assert 34 == len(objects)


def test_verify_relationships(objects):
    verify_relationships(objects)
