""" Does the rendereing for all databases """
from bd_to_dot.dot.renderer import build_graph


def build_graphs(databases, objects):
    """ build the graphs and writes them """
    graphs = _build_graphs(databases, objects)
    write_graphs(graphs)
    return graphs


def _build_graphs(databases, objects):
    return [(database_obj, build_database(database_obj, objects)) for
            database_obj in databases]


def build_database(database, objects):
    """ Make the graph for one documented database """
    db_index = database.ID
    objs = list(filter(lambda obj: obj.DATABASEID == db_index, objects))
    objs_dict = {}
    for obj in objs:
        objs_dict[obj.INDEX] = obj
    graph = build_graph(database.NAME, objs_dict)
    return graph


def write_graphs(dbgraphs):
    """ Write graphs in configured output directory """
    for database, graph in dbgraphs:
        output = database.SETTINGS["DocumenterOutputDir"]\
            + "/{}/graphs".format(database.NAME)
        graph.save(directory=output)
        graph.render(format="svg")
