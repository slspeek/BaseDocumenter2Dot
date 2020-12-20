import pickle
import os

from pytest import fixture
from bd_to_dot.dot.renderer import GraphRenderer, EXCLUDED_TYPES
from bd_to_dot_test.dot.resource import TEST_OUTPUT, FIXTURE_DIR


def loadObjects():
    with open(FIXTURE_DIR.format('objects.pickle'), 'rb') as file:
        objs = pickle.load(file)
    return objs


@fixture(scope="package")
def objects():
    yield loadObjects()


def test_load_objects(objects):
    assert 69 == len(objects)


def test_verify_relationships(objects):
    objects = list(filter(lambda x: x.DATABASEID == 2, objects))
    objs = {}
    for o in objects:
        objs[o.INDEX] = o
    GraphRenderer("test", objs, [])


def test_view(objects):
    objects = list(filter(lambda x: x.DATABASEID == 2, objects))
    objs = {}
    for o in objects:
        objs[o.INDEX] = o
    gr = GraphRenderer("test", objs, EXCLUDED_TYPES)
    g = gr.render_graph()
    g.save(TEST_OUTPUT.format("testdb.gv"))
    if os.getenv("BD_VIEW", 0):
        g.view()
