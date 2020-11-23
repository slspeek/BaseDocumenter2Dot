
typeToShape = {"Table": "cylinder",
               "View": "hexagon",
               "Query": "ellipse",
               "Form": "rectangle"}


def render_object(obj, graph):
    graph.node(str(obj.INDEX),
               label=obj.SHORTNAME,
               shape=typeToShape[obj.TYPE])


def render_relation(startObj, endObj, graph):
    graph.edge(startObj.INDEX, endObj.INDEX)


def verify_relationships(dictObjs):
    for key in dictObjs.keys():
        o = dictObjs[key]
        for u in o.USES:
            usedObj = dictObjs[u]
            assert key in usedObj.USEDBY
        for u in o.USEDBY:
            usedByObj = dictObjs[u]
            assert key in usedByObj.USES
