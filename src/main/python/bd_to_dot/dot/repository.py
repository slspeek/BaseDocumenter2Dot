from bd_to_dot.dot.renderer import build_graph


def build_graphs(databases, objects):
    gs = _build_graphs(databases, objects)
    write_graphs(gs)
    return gs


def _build_graphs(databases, objects):
    graphs = []
    for db in databases:
        graphs.append((db, build_database(db, objects)))
    return graphs


def build_database(database, objects):
    id = database.ID
    objs = list(filter(lambda o: o.DATABASEID == id, objects))
    objsDict = {}
    for o in objs:
        objsDict[o.INDEX] = o
    graph = build_graph(database.NAME, objsDict)
    return graph


def write_graphs(dbgraphs):
    for db, g in dbgraphs:
        output = db.SETTINGS["DocumenterOutputDir"] + "/graphs"
        g.save(directory=output)
        g.render(format="svg")
