""" Quick view for the objects fixture """
import pickle
import os

from pytest import fixture
from bd_to_dot.dot.renderer import GraphRenderer, EXCLUDED_TYPES
from bd_to_dot_test.dot.resource import TEST_OUTPUT, FIXTURE_DIR


def load_objects():
    """ Returns an array of Objects from the test fixture """
    with open(FIXTURE_DIR.format('objects.pickle'), 'rb') as file:
        objs = pickle.load(file)
    return objs


@fixture(scope="package")
def objects():
    """ Array of all objects from repository """
    yield load_objects()


def test_load_objects(objects):  # pylint: disable=redefined-outer-name
    """ The list 69 long """
    assert len(objects) == 69


def test_verify_relationships(objects):  # pylint: disable=redefined-outer-name
    """ Test GraphRenderer constructor """
    objs_dict = {}
    for obj in filter(lambda x: x.DATABASEID == 2, objects):
        objs_dict[obj.INDEX] = obj
    GraphRenderer("test", objs_dict, [])


def test_view(objects):  # pylint: disable=redefined-outer-name
    """ Make one graph for viewing """
    objects = list(filter(lambda x: x.DATABASEID == 2, objects))
    objs = {}
    for obj in objects:
        objs[obj.INDEX] = obj
    renderer = GraphRenderer("test", objs, EXCLUDED_TYPES)
    graph = renderer.render_graph()
    graph.save(TEST_OUTPUT.format("testdb.gv"))
    if os.getenv("BD_VIEW", ""):
        graph.view()
