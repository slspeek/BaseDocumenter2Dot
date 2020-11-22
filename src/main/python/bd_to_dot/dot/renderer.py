# from graphviz import Digraph

typeToShape = {1: "cylinder",
               2: "ellipse",
               3: "rectangle"}


def render_object(obj, graph):
    graph.node(str(obj.INDEX),
               label=obj.SHORTNAME,
               shape=typeToShape[obj.TYPE])


def render_relation(startObj, endObj, graph):
    pass
