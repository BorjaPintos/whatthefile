import unittest

from src.core import Core
from src.domain.loadermodules import LoaderModules
from src.domain.targetfile import TargetFile


class CoreTest(unittest.TestCase):

    def test_run(self):
        """
        modules_path = "./src/modules"
        file = TargetFile("path", b"")
        modules = LoaderModules(modules_path).get_modules()
        """