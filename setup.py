"""Python setup.py for budgetguard package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("budgetguard", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="budgetguard",
    version=read("budgetguard", "VERSION"),
    description="Awesome budgetguard created by M-Borsuk",
    url="https://github.com/M-Borsuk/BudgetGuard/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="M-Borsuk",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["budgetguard = budgetguard.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
