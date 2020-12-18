from bd_to_dot import verify_queries, generate_graphs


def run_generate_graphs():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return
    conn = db.getConnection("", "")
    generate_graphs(conn)
    conn.close()
    conn.dispose()


def run_verify_queries():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return

    errors = verify_queries(db)
    if len(errors) > 0:
        raise Exception(str(errors))


g_exportedScripts = (run_generate_graphs, run_verify_queries)
