from bd_to_dot import verify_queries, generate_graphs, open_connection


def run_generate_graphs():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return
    with open_connection(db) as conn:
        generate_graphs(conn)


def run_verify_queries():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return

    errors = verify_queries(db)
    if len(errors) > 0:
        raise Exception(str(errors))


g_exportedScripts = (run_generate_graphs, run_verify_queries)
