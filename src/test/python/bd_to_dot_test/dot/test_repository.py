""" repository module unittests """
from bd_to_dot.dot.repository import build_graphs

# pylint: disable=unused-import
from bd_to_dot_test.dot.test_objects import objects
# pylint: disable=unused-import
from bd_to_dot_test.dot.test_databases import databases


# pylint: disable=unused-argument,redefined-outer-name
def test_build_graphs(objects, databases):
    """ See that two graphs are producted from fixtures """
    assert len(build_graphs(databases, objects)) == 2
