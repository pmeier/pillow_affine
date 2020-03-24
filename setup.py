from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

about = {}
with open(path.join(here, "pillow_affine", "__about__.py"), "r") as fh:
    exec(fh.read(), about)

with open(path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()

install_requires = ("pillow",)

type_check_requires = (
    "mypy",
    # FIXME: change this before release, since this does not work
    "numpy-stubs@https://github.com/numpy/numpy-stubs/archive/master.zip",
)

test_requires = (
    "pytest",
    "pyimagetest",
    "numpy",
)

doc_requires = (
    "sphinx",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
)

dev_requires = (*type_check_requires, *test_requires, *doc_requires)

extras_require = {
    "type_check": type_check_requires,
    "test": test_requires,
    "doc": doc_requires,
    "dev": dev_requires,
}

classifiers = (
    "Development Status :: 3 - Beta",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
)

setup(
    name=about["__name__"],
    description=about["__description__"],
    version=about["__version__"],
    url=about["__url__"],
    license=about["__license__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("test",)),
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=">=3.6",
    classifiers=classifiers,
)
