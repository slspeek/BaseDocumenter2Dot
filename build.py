#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("pypi:pybuilder_pytest")
use_plugin("python.flake8")


name = "BaseDocumenter2Dot"
default_task = "publish"
version = "0.0.1"

@init
def set_properties(project):
    project.set_property("libreoffice_home", "/opt/libreoffice6.4")
    project.set_property("flake8_break_build", True)
    project.set_property("flake8_verbose_output", True)
    project.set_property("flake8_include_test_sources", True)
    project.set_property("unittest_inherit_environment", True)
