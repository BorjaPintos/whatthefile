# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.evtxreader.main import Constructor
from src.output.listoutput import ListOutput
from src.output.outputfactory import OutputFactory


class EvtxReaderTest(unittest.TestCase):

    def test_read_evtx(self):
        path = "./tests/examples/evtx/security.evtx"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue(len(result["events"]) != 0)

    def test_read_evtx2(self):
        path = "./tests/examples/evtx/System.evtx"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertTrue(len(result["events"]) != 0)

    def test_read_evtx_with_second_output(self):
        path = "./tests/examples/evtx/System2.evtx"
        target_file = TargetFile(path)
        module = Constructor()
        module.set_params({"needs_pipe": True, "output": "list"})
        my_lyst_output = ListOutput()
        backup_function = OutputFactory._get_list_output
        OutputFactory._get_list_output = lambda params : my_lyst_output
        result = module.run(target_file, {})
        OutputFactory._get_list_output = backup_function
        self.assertTrue(result["n_events"] != 0)
        self.assertTrue(len(my_lyst_output.get_list()), result["n_events"])

    def test_invalid_file(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))

