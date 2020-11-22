import pickle
from pytest import fixture
from bd_to_dot.dot.renderer import verify_relationships

from bd_to_dot import Object, TYPE


def test_type_view():
    obj = Object(1, 'Table', "vwPlant",
                 "vwPlant", 0, 0, [2], [4, 5], {'TableIsView': True})
    assert "View" == TYPE(obj)


def test_type_field():
    obj = Object(1, 'Field', "vwPlant",
                 "vwPlant", 0, 0, [2], [4, 5], {'TableIsView': True})
    assert "Field" == TYPE(obj)


def loadObjects():
    with open('src/test/resources/objects.pickle', 'rb') as file:
        objs = pickle.load(file)
    return objs


@fixture
def objects():
    yield loadObjects()


def test_load_objects(objects):
    assert 34 == len(objects)


def test_verify_relationships(objects):
    verify_relationships(objects)
