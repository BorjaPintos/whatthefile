# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.browserhistory.main import Constructor
from src.output.listoutput import ListOutput
from src.output.outputfactory import OutputFactory


class BrowserHistoryTest(unittest.TestCase):

    def test_chrome_history_v1(self):
        path = "./tests/examples/browsers/chrome/History"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue(result["browser"], "chrome")
        self.assertEqual(len(result["downloads"]), 2)
        self.assertEqual(result["downloads"][0]["type"], "Download")
        self.assertTrue(result["downloads"][0]["browser"], "chrome")
        self.assertEqual(len(result["visites"]), 69)
        self.assertEqual(result["visites"][0]["type"], "Visit")
        self.assertTrue(result["visites"][0]["browser"], "chrome")
        self.assertEqual(len(result["searchs"]), 3)
        self.assertEqual(result["searchs"][0]["type"], "Search")
        self.assertTrue(result["searchs"][0]["browser"], "chrome")

    def test_chrome_history_v1_with_second_output(self):
        path = "./tests/examples/browsers/chrome/History"
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params({"needs_pipe": True, "output": "list"})
        my_lyst_output = ListOutput()
        backup_function = OutputFactory._get_list_output
        OutputFactory._get_list_output = lambda params: my_lyst_output
        result = module.run(target_file, {})
        OutputFactory._get_list_output = backup_function
        self.assertTrue(result["browser"], "chrome")
        self.assertTrue(result["n_downloads"] != 0)
        self.assertTrue(result["n_visites"] != 0)
        self.assertTrue(result["n_searchs"] != 0)
        self.assertTrue(len(my_lyst_output.get_list()),
                        result["n_downloads"] + result["n_visites"] + result["n_searchs"])

    def test_chrome_history_v2(self):
        path = "./tests/examples/browsers/chrome/History-59.0.3071.86"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue(result["browser"], "chrome")
        self.assertEqual(len(result["downloads"]), 1)
        self.assertEqual(result["downloads"][0]["type"], "Download")
        self.assertEqual(len(result["visites"]), 1)
        self.assertEqual(len(result["searchs"]), 0)

    def test_safari_history_v1(self):
        path = "./tests/examples/browsers/safari/History.db"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue(result["browser"], "safari")
        self.assertEqual(len(result["downloads"]), 0)
        self.assertEqual(len(result["visites"]), 25)
        self.assertEqual(result["visites"][0]["type"], "Visit")
        self.assertEqual(len(result["searchs"]), 0)

    def test_firefox_history_v1(self):
        path = "./tests/examples/browsers/firefox/places.sqlite"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue(result["browser"], "firefox")
        self.assertEqual(len(result["downloads"]), 0)
        self.assertEqual(len(result["visites"]), 1)
        self.assertEqual(result["visites"][0]["type"], "Visit")
        self.assertEqual(len(result["searchs"]), 0)

    def test_firefox_history_v2(self):
        path = "./tests/examples/browsers/firefox/places_new.sqlite"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue(result["browser"], "firefox")
        self.assertEqual(len(result["downloads"]), 1)
        self.assertEqual(result["downloads"][0]["type"], "Download")
        self.assertEqual(len(result["visites"]), 34)
        self.assertEqual(result["visites"][0]["type"], "Visit")
        self.assertEqual(len(result["searchs"]), 0)


    def test_edge_history(self):
        path = "./tests/examples/browsers/edge/History"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        print(result)
        self.assertTrue(result["browser"], "edge")
        self.assertEqual(len(result["downloads"]), 2)
        self.assertEqual(result["downloads"][0]["type"], "Download")
        self.assertEqual(len(result["visites"]), 20)
        self.assertEqual(result["visites"][0]["type"], "Visit")
        self.assertEqual(len(result["searchs"]), 2)
        self.assertEqual(result["searchs"][0]["type"], "Search")

    def test_edge_history_with_second_output(self):
        path = "./tests/examples/browsers/edge/History"
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params({"needs_pipe": True, "output": "list"})
        my_lyst_output = ListOutput()
        backup_function = OutputFactory._get_list_output
        OutputFactory._get_list_output = lambda params: my_lyst_output
        result = module.run(target_file, {})
        OutputFactory._get_list_output = backup_function
        self.assertTrue(result["browser"], "edge")
        self.assertTrue(result["n_downloads"] == 2)
        self.assertTrue(result["n_visites"] == 20)
        self.assertTrue(result["n_searchs"] == 2)
        self.assertTrue(len(my_lyst_output.get_list()),
                        result["n_downloads"] + result["n_visites"] + result["n_searchs"])

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
