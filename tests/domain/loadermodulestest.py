import unittest
from src.domain.loadermodules import LoaderModules

MODULES_PATH = "./src/modules"
NUM_MODULES = 11


class LoaderModulesTest(unittest.TestCase):

    def test_load_modules(self):
        modules = LoaderModules(MODULES_PATH).get_modules()
        self.assertEqual(len(modules), NUM_MODULES)
