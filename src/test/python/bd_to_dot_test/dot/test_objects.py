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
    assert 34 == len(objects)


def test_verify_relationships(objects):
    GraphRenderer("test", objects, [])


def test_view(objects):
    gr = GraphRenderer("test", objects, EXCLUDED_TYPES)
    g = gr.render_graph()
    g.save("src/test/resources/testdb.gv")
    if os.getenv("BD_VIEW", 0):
        g.view()
