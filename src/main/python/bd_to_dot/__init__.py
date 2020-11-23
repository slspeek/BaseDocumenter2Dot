from bd_to_dot.oo.db import loadObjects
from bd_to_dot.dot.renderer import build_graph


def graph(connection):
    dictObjs = loadObjects(connection)
    g = build_graph(dictObjs)
    return g
