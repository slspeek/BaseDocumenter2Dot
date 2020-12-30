""" e2e-test that runs against the installed oxt """
from bd_to_dot_test.oo.connect import get_context
# pylint: disable=unused-import
from bd_to_dot_test.oo.test_db import libreoffice
from bd_to_dot.util.util import invoke_macro


MACRO = "vnd.sun.star.script:bd2dot.oxt|python|main.py$run_generate_graphs?"\
        "language=Python&location=user:uno_packages"


# pylint: disable=unused-argument,redefined-outer-name
def test_run_oxt(libreoffice):
    """ Run generate graphs """
    ctx = get_context()
    invoke_macro(ctx, MACRO)
