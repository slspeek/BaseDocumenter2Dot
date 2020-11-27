from graphviz import Digraph

TYPE_ATTRS = {
    "Table": {"shape": "cylinder", "fillcolor": "#a7c3eb", "style": "filled"},
    "View": {"shape": "hexagon"},
    "Query": {"shape": "ellipse"},
    "Form": {"shape": "rect", "style": "filled", "fillcolor": "#ffcc99"},
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

RELATION_ATTR = {
    ("Table", "Table"): {},
    ("Form", "Table"): {"arrowhead": "box", "color": "red"},
    ("View", "Table"): {"arrowhead": "dot"},
    ("Form", "View"): {"arrowhead": "dot"},
    ("Form", "Query"): {"arrowhead": "dot"},
    ("Query", "Table"): {"arrowhead": "dot"},
    ("Query", "Query"): {"arrowhead": "dot"}
}

EXCLUDED_TYPES = ["Control", "Database", "Field", "Module"]


def build_graph(dictObjs):
    gr = GraphRenderer(dictObjs, EXCLUDED_TYPES)
    graph = gr.render_graph()
    return graph


class GraphRenderer(object):

    def __init__(self, dictObjs, excluded_types):
        self.dictObjs = dictObjs
        self._verify_relationships()
        self.excluded_types = excluded_types
        self.name = self._name()
        self.objs = list(
            filter(lambda x: x.TYPE not in excluded_types, dictObjs.values())
        )
        self.graph = Digraph(self.name)
        self.graph.attr("graph", rankdir="LR")
        self.graph.attr("graph", label=self.name,
                        labelloc="top", fontsize="24")

    def _name(self):
        objs = self.dictObjs.values()
        dbs = [o for o in objs if o.TYPE == "Database"]
        if len(dbs) > 1:
            raise ValueError("Too many Database objects in list")
        if len(dbs) < 1:
            raise ValueError("No Database objects in list")
        return dbs[0].NAME

    def _related_objs(self):
        res = []
        for o in self.objs:
            for u in o.USES:
                uO = self.dictObjs[u]
                if uO in self.objs:
                    res.append((o, uO))
        return res

    def _parent_relations(self):
        res = []
        for obj in self.objs:
            pi = obj.PARENTINDEX
            if pi in self.dictObjs.keys():
                pObj = self.dictObjs[obj.PARENTINDEX]
                if pObj in self.objs:
                    res.append((obj, pObj))
        return res

    def _verify_relationships(self):
        for key in self.dictObjs.keys():
            o = self.dictObjs[key]
            for u in o.USES:
                usedObj = self.dictObjs[u]
                assert key in usedObj.USEDBY
            for u in o.USEDBY:
                usedByObj = self.dictObjs[u]
                assert key in usedByObj.USES

    def _render_object(self, obj):
        self.graph.node(str(obj.INDEX),
                        label=obj.SHORTNAME,
                        _attributes=TYPE_ATTRS[obj.TYPE])

    def _render_relation(self, startObj, endObj):
        types = (startObj.TYPE, endObj.TYPE)
        attrs = {}
        if types in RELATION_ATTR:
            attrs = RELATION_ATTR[types]
        self.graph.edge(str(startObj.INDEX),
                        str(endObj.INDEX),
                        _attributes=attrs)

    def render_graph(self):
        relations = self._related_objs()
        parent_rel = self._parent_relations()
        for obj in self.objs:
            self._render_object(obj)
        for (startObj, endObj) in relations:
            self._render_relation(startObj, endObj)
        for (startObj, endObj) in parent_rel:
            self._render_relation(startObj, endObj)
        return self.graph
