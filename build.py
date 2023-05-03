from pybuilder.core import use_plugin, init, Author

use_plugin("filter_resources")

use_plugin("python.core")
use_plugin("python.coverage")
use_plugin("python.unittest")
use_plugin("python.integrationtest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")

name = "budget-guard"
authors = [Author("Mateusz Borsuk", "mtszborsuk212@gmail.com")]
license = "Apache License, Version 2.0"


default_task = ["install_dependencies", "analyze", "publish"]


@init
def initialize(project):
    project.set_property("dir_source_main_python", "src/main/budget_guard")
    project.set_property("dir_source_unittest_python", "src/unit_tests/python")

    project.depends_on_requirements("requirements.txt")
    project.build_depends_on_requirements("requirements-dev.txt")

    project.set_property("coverage_break_build", False)
    project.set_property("flake8_break_build", True)
