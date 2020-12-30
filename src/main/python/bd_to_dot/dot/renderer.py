"""" Responsible for graph generation via graphviz lib """
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
    "SubForm": {"shape": "doubleoctagon",
                "style": "filled", "fillcolor": "#d3d3d3"},
    "Grid": {"shape": "Mdiamond"},
    "Control": {"shape": "octagon", "style": "filled", "fillcolor": "#d3d3d3"},
    "Event": {"shape": "square"},
    "Procedure": {"shape": "component"},
    "Toolbarcontrol": {"shape": "Msquare"}
}

RELATION_ATTR = {
    ("Table", "Table"): {},
    ("Control", "Table"): {"arrowhead": "box", "color": "red"},
    ("Control", "Query"): {"arrowhead": "dot"},
    ("SubForm", "Table"): {"arrowhead": "box", "color": "red"},
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


def build_graph(name, objs_dict):
    """ makes Digraph of the database object `objs_dict` """
    renderer = GraphRenderer(name, objs_dict, EXCLUDED_TYPES)
    graph = renderer.render_graph()
    return graph


def html_id(obj: Object):
    """ returns the value for the id html attribute """
    return "%05.d" % obj.INDEX


def href(obj):
    """ returns the value for a href html attribute """
    file = TYPE_HREF[obj.TYPE]
    return "../{}.html#{}".format(file, html_id(obj))


class GraphRenderer:  # pylint: disable=too-few-public-methods
    """ fills in a Digraph from `objs_dict` """

    def __init__(self, name, objs_dict, excluded_types):
        self.objs_dict = objs_dict
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
                   self.objs_dict.values())
        )

        def relevant_control_filter(obj):
            if obj.TYPE != "Control":
                return True
            return len(obj.USES) > 0

        self.objs = list(
            filter(relevant_control_filter,
                   self.objs)
        )

    def _related_objs(self):
        res = []
        for obj in self.objs:
            for use_ref in obj.USES:
                use = self.objs_dict[use_ref]
                if use in self.objs:
                    res.append((obj, use))
        return res

    def _parent_relations(self):
        res = []
        for obj in self.objs:
            parent_index = obj.PARENTINDEX
            if parent_index in self.objs_dict.keys():
                parent_obj = self.objs_dict[parent_index]
                if parent_obj in self.objs:
                    res.append((obj, parent_obj))
        return res

    def _verify_relationships(self):
        for key in self.objs_dict.keys():
            obj = self.objs_dict[key]
            for used_ref in obj.USES:
                used_obj = self.objs_dict[used_ref]
                assert key in used_obj.USEDBY
            for used_by_ref in obj.USEDBY:
                used_by_obj = self.objs_dict[used_by_ref]
                assert key in used_by_obj.USES

    def _render_object(self, obj):
        if obj.TYPE == "Control" and "Caption" in obj.PROPERTIES:
            label = obj.PROPERTIES["Caption"]
        else:
            label = obj.SHORTNAME
        self.graph.node(str(obj.INDEX),
                        label=label,
                        tooltip="{} ({})".format(obj.NAME, obj.TYPE),
                        href=href(obj),
                        id=html_id(obj),
                        _attributes=TYPE_ATTRS[obj.TYPE])

    def _render_parent_relation(self, start_obj, end_obj):
        types = (start_obj.TYPE, end_obj.TYPE)
        attrs = RELATION_ATTR.get(types, {})
        attrs["edgetooltip"] = "{} is child of {}"\
            .format(start_obj.NAME, end_obj.NAME)
        attrs["style"] = "dashed"
        attrs["color"] = "#ffcc99"
        attrs["arrowhead"] = "none"
        self.graph.edge(str(start_obj.INDEX),
                        str(end_obj.INDEX),
                        _attributes=attrs)

    def _render_relation(self, start_obj, end_obj):
        types = (start_obj.TYPE, end_obj.TYPE)
        attrs = RELATION_ATTR.get(types, {})
        attrs["edgetooltip"] = "{} -> {}".format(start_obj.NAME, end_obj.NAME)
        self.graph.edge(str(start_obj.INDEX),
                        str(end_obj.INDEX),
                        _attributes=attrs)

    def render_graph(self):
        """ Draw the objects and relationships """
        relations = self._related_objs()
        parent_rel = self._parent_relations()
        for obj in self.objs:
            self._render_object(obj)
        for (start_obj, end_obj) in relations:
            self._render_relation(start_obj, end_obj)
        for (start_obj, end_obj) in parent_rel:
            self._render_parent_relation(start_obj, end_obj)
        return self.graph
