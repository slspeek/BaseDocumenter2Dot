from bd_to_dot_test.oo.connect import get_context
from bd_to_dot_test.oo.test_db import libreoffice  # NOQA: F401
from bd_to_dot.util.util import invokeMacro


MACRO = "vnd.sun.star.script:bd2dot.oxt|python|main.py$run_generate_graphs?"\
        "language=Python&location=user:uno_packages"


def test_run_oxt(libreoffice):  # NOQA: F811
    ctx = get_context()
    invokeMacro(ctx, MACRO)
