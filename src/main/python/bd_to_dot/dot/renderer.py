from graphviz import Digraph

typeToShape = {
    "Table": "cylinder",
    "View": "hexagon",
    "Query": "ellipse",
    "Form": "house",
    "Report": "rectangle",
    "Dialog": "trapezium",
    "Module": "component",
    "Toolbar": "tab",
    "Field": "invhouse",
    "SubForm": "pentagon",
    "Grid": "Mdiamond",
    "Control": "parallelogram",
    "Event": "square",
    "Procedure": "component",
    "Toolbarcontrol": "Msquare"}


def build_graph(dictObjs):
    graph = Digraph("")
    render_graph(dictObjs, graph)
    return graph


def render_graph(dictObjs, graph):
    relations = related_objects(dictObjs)
    parent_rel = parent_relations(dictObjs)
    for obj in dictObjs.values():
        render_object(obj, graph)
    for (startObj, endObj) in relations:
        render_relation(startObj, endObj, graph)
    for (startObj, endObj) in parent_rel:
        render_relation(startObj, endObj, graph)


def render_object(obj, graph):
    if obj.TYPE == "Database" or obj.TYPE == "Grid"\
       or obj.SHORTNAME == "MainForm_Grid":
        return
    graph.node(str(obj.INDEX),
               label=obj.SHORTNAME,
               shape=typeToShape[obj.TYPE])


def render_relation(startObj, endObj, graph):
    graph.edge(str(startObj.INDEX), str(endObj.INDEX))


def verify_relationships(dictObjs):
    for key in dictObjs.keys():
        o = dictObjs[key]
        for u in o.USES:
            usedObj = dictObjs[u]
            assert key in usedObj.USEDBY
        for u in o.USEDBY:
            usedByObj = dictObjs[u]
            assert key in usedByObj.USES


def related_objects(dictObjs):
    res = []
    for idx in dictObjs:
        o = dictObjs[idx]
        for u in o.USES:
            uO = dictObjs[u]
            if uO.TYPE != "Grid":
                res.append((o, uO))
    return res


def parent_relations(dictObjs):
    res = []
    for obj in dictObjs.values():
        pi = obj.PARENTINDEX
        if obj.PARENTTYPE != "Database":
            res.append((obj, dictObjs[pi]))
    return res
