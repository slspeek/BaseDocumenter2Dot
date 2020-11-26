from graphviz import Digraph

TYPE_ATTRS = {
    "Table": {"shape": "cylinder", "fillcolor": "#a7c3eb", "style": "filled"},
    "View": {"shape": "hexagon"},
    "Query": {"shape": "ellipse"},
    "Form": {"shape": "house"},
    "Report": {"shape": "rectangle"},
    "Dialog": {"shape": "trapezium"},
    "Module": {"shape": "component"},
    "Toolbar": {"shape": "tab"},
    "Field": {"shape": "invhouse"},
    "SubForm": {"shape": "pentagon"},
    "Grid": {"shape": "Mdiamond"},
    "Control": {"shape": "parallelogram"},
    "Event": {"shape": "square"},
    "Procedure": {"shape": "component"},
    "Toolbarcontrol": {"shape": "Msquare"}}

EXCLUDED_TYPES = ["Control", "Database", "Field"]


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
    if obj.TYPE in EXCLUDED_TYPES\
       or obj.SHORTNAME == "MainForm_Grid":
        return
    graph.node(str(obj.INDEX),
               label=obj.SHORTNAME,
               _attributes=TYPE_ATTRS[obj.TYPE])


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
        if o.TYPE in EXCLUDED_TYPES:
            continue
        for u in o.USES:
            uO = dictObjs[u]
            if uO.TYPE not in EXCLUDED_TYPES:
                res.append((o, uO))
    return res


def parent_relations(dictObjs):
    res = []
    for obj in dictObjs.values():
        if obj.TYPE in EXCLUDED_TYPES:
            continue
        pi = obj.PARENTINDEX
        if obj.PARENTTYPE != "Database":
            res.append((obj, dictObjs[pi]))
    return res
