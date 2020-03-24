import os
from os import path
from setuptools import find_packages
from importlib import import_module
import itertools
import unittest
import pillow_affine


class Tester(unittest.TestCase):
    def test_import(self):
        pkg_name = "pillow_affine"
        here = path.abspath(path.dirname(__file__))
        pkg_root = path.join(here, "..", pkg_name)

        packages = find_packages(pkg_root)

        modules = []
        for package in packages:
            files = os.listdir(path.join(pkg_root, package.replace(".", os.sep)))
            for file in files:
                name, ext = path.splitext(file)
                if ext == ".py" and name != "__init__":
                    modules.append(f"{package}.{name}")

        for module in itertools.chain(packages, modules):
            import_module(f"{pkg_name}.{module}")

    def test_about(self):
        for attr in (
            "name",
            "description",
            "version",
            "url",
            "license",
            "author",
            "author_email",
        ):
            self.assertIsInstance(getattr(pillow_affine, f"__{attr}__"), str)
