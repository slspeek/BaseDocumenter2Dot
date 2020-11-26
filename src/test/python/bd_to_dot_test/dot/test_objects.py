import pickle
import graphviz
import os

from pytest import fixture
from bd_to_dot.dot.renderer import verify_relationships, render_graph


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


def test_view(objects):
    g = graphviz.Digraph("testdb")
    render_graph(objects, g)
    g.save("src/test/resources/testdb.gv")
    if os.getenv("BD_VIEW", 0):
        g.view()
