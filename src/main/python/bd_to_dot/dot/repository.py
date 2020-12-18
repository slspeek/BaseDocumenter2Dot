from bd_to_dot.dot.renderer import build_graph


def build_graphs(databases, objects):
    graphs = []
    for db in databases.values():
        graphs.append(build_database(db, objects))
    return graphs


def build_database(database, objects):
    id = database.ID
    objs = list(filter(lambda o: o.DATABASEID == id, objects.values()))
    objsDict = {}
    for o in objs:
        objsDict[o.INDEX] = o
    graph = build_graph(database.NAME, objsDict)
    return graph
