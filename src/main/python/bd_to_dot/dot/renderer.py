from graphviz import Digraph
from bd_to_dot.oo.db import Object

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
    "Control": {"shape": "octagon", "style": "filled", "fillcolor": "#d3d3d3"},
    "Event": {"shape": "square"},
    "Procedure": {"shape": "component"},
    "Toolbarcontrol": {"shape": "Msquare"}
}

RELATION_ATTR = {
    ("Table", "Table"): {},
    ("Procedure", "Procedure"): {"arrowhead": "dot", "color": "#90EE90"},
    ("Form", "Table"): {"arrowhead": "box", "color": "red"},
    ("View", "Table"): {"arrowhead": "dot"},
    ("Form", "View"): {"arrowhead": "dot"},
    ("Form", "Query"): {"arrowhead": "dot"},
    ("Query", "Table"): {"arrowhead": "dot"},
    ("Query", "Query"): {"arrowhead": "dot"}
}

TYPE_HREF = {
    "Table": "Tables",
    "View": "Tables",
    "Query": "Queries",
    "Form": "ControlsByForm",
    "Report": "FullIndex",
    "Dialog": "FullIndex",
    "Module": "Modules",
    "Toolbar": "FullIndex",
    "Field": "FullIndex",
    "SubForm": "FullIndex",
    "Grid": "FullIndex",
    "Control": "ControlsByForm",
    "Event": "FullIndex",
    "Procedure": "ProceduresByModule",
    "Toolbarcontrol": "FullIndex"
}

EXCLUDED_TYPES = ["Database", "Field", "Module"]


def build_graph(name, dictObjs):
    gr = GraphRenderer(name, dictObjs, EXCLUDED_TYPES)
    graph = gr.render_graph()
    return graph


def id(obj):
    return "%05.d" % obj.INDEX


def href(obj: Object):
    file = TYPE_HREF[obj.TYPE]
    return "../{}.html#{}".format(file, id(obj))


class GraphRenderer(object):

    def __init__(self, name, dictObjs, excluded_types):
        self.dictObjs = dictObjs
        self._verify_relationships()
        self.excluded_types = excluded_types
        self.name = name
        self._filter_objs()
        self.graph = Digraph(self.name)
        self.graph.attr("graph", rankdir="LR")
        self.graph.attr("graph", label=self.name,
                        labelloc="top", fontsize="24")

    def _filter_objs(self):
        self.objs = list(
            filter(lambda x: x.TYPE not in self.excluded_types,
                   self.dictObjs.values())
        )

        def relevant_control_filter(obj):
            if obj.TYPE != "Control":
                return True
            else:
                return len(obj.USES) > 0

        self.objs = list(
            filter(relevant_control_filter,
                   self.objs)
        )

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
        if obj.TYPE == "Control" and "Caption" in obj.PROPERTIES:
            label = obj.PROPERTIES["Caption"]
        else:
            label = obj.SHORTNAME
        self.graph.node(str(obj.INDEX),
                        label=label,
                        href=href(obj),
                        id=id(obj),
                        _attributes=TYPE_ATTRS[obj.TYPE])

    def _render_parent_relation(self, startObj, endObj):
        types = (startObj.TYPE, endObj.TYPE)
        attrs = {}
        if types in RELATION_ATTR:
            attrs = RELATION_ATTR[types]
        attrs["edgetooltip"] = "{} is child of {}"\
            .format(startObj.NAME, endObj.NAME)
        attrs["style"] = "dashed"
        attrs["color"] = "#ffcc99"
        attrs["arrowhead"] = "none"
        self.graph.edge(str(startObj.INDEX),
                        str(endObj.INDEX),
                        _attributes=attrs)

    def _render_relation(self, startObj, endObj):
        types = (startObj.TYPE, endObj.TYPE)
        attrs = {}
        if types in RELATION_ATTR:
            attrs = RELATION_ATTR[types]
        attrs["edgetooltip"] = "{} -> {}".format(startObj.NAME, endObj.NAME)
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
            self._render_parent_relation(startObj, endObj)
        return self.graph
