import glob
from os.path import basename, dirname, isfile, join

ALL_MODULES = sorted([
    basename(f)[:-3]
    for f in glob.glob(join(dirname(__file__), "*.py"))
    if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
])

__all__ = ALL_MODULES + ["ALL_MODULES"]