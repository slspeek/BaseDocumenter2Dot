import pickle
import os

from pytest import fixture
from bd_to_dot.dot.renderer import GraphRenderer, EXCLUDED_TYPES


def loadObjects():
    with open('src/test/resources/fixtures/objects.pickle', 'rb') as file:
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
    g.save("src/test/resources/testdb.gv")
    if os.getenv("BD_VIEW", 0):
        g.view()
