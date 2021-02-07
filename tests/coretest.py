import os
import unittest
from src.core import Core
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.outputfactory import OutputFactory


class CoreTest(unittest.TestCase):

    def test_run_strings(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list",
                                         "extracted_output_path": "./tests/examples/safe_directory"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": False},
                         "module.hashes": {"active": False,'hashes_to_calculate' : "MD5,SHA1,SHA256"},
                         "module.imagerecognitiontensorflow": {"active": False},
                         "module.metadata": {"active": False}, "module.ocrtesseract": {"active": False},
                         "module.qrbcreader": {"active": False}, "module.strings": {"active": True, "char_min": 10},
                         "module.virustotal": {"active": False}, "module.zipextractor": {"active": False}})
        path = "./tests/examples/collie.jpg.zip"
        output = OutputFactory.get_output(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertEqual(len(output.get_list()[0]["strings"][">=10"]), 3)
        self.assertEqual(output.get_list()[0]["strings"]["n_elements"], 3)

    def test_run_zipextractor(self):
        conf = WhatTheFileConfiguration()
        conf.parse_string("""
        [whatthefile]
        modules_package = src.modules
        extracted_output_path = ./tests/examples/safe_directory
        output = list
        [module.zipextractor]
        active = true
        extracted_output_path = ${whatthefile:extracted_output_path}/zipextractor
        """)

        final_file = "./tests/examples/safe_directory/zipextractor/collie.jpg"
        dir_file = os.path.dirname(final_file)
        if os.path.exists(final_file):
            os.remove(final_file)
        if os.path.exists(dir_file):
            os.rmdir(dir_file)
        self.assertFalse(os.path.exists(final_file))

        path = "./tests/examples/collie.jpg.zip"
        output = OutputFactory.get_output(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertTrue(os.path.exists(final_file))
        self.assertEqual(output.get_list()[-1]["path"], final_file)

        os.remove(final_file)
        os.rmdir(dir_file)

    def test_run_hashes(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list",
                                         "extracted_output_path": "./tests/examples/safe_directory"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": False},
                         "module.hashes": {"active": True,'hashes_to_calculate' : "MD5,SHA1,SHA256"},
                         "module.imagerecognitiontensorflow": {"active": False},
                         "module.metadata": {"active": False}, "module.ocrtesseract": {"active": False},
                         "module.qrbcreader": {"active": False}, "module.strings": {"active": False, "char_min": 10},
                         "module.virustotal": {"active": False}, "module.zipextractor": {"active": False}})
        path = "./tests/examples/collie.jpg.zip"
        output = OutputFactory.get_output(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertTrue("SHA256" in output.get_list()[0]["hashes"])
        self.assertTrue("start_module" in output.get_list()[0]["hashes"])
        self.assertTrue("end_module" in output.get_list()[0]["hashes"])
        self.assertTrue("begin_analysis" in output.get_list()[0])
        self.assertTrue("end_analysis" in output.get_list()[0])

    def a_test_run_directory(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list",
                                         "extracted_output_path": "./tests/examples/safe_directory"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": True},
                         "module.hashes": {"active": True, 'hashes_to_calculate' : "MD5,SHA1,SHA256"},
                         "module.imagerecognitiontensorflow": {"active": True},
                         "module.metadata": {"active": True}, "module.ocrtesseract": {"active": True},
                         "module.qrbcreader": {"active": True}, "module.strings": {"active": True, "char_min": 4},
                         "module.virustotal": {"active": False}, "module.zipextractor": {"active": True}})

        path = "./tests/examples/testdirectorydonotinsertmoreitems"
        output = OutputFactory.get_output(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertEqual(len(output.get_list()), 3)
        self.assertEqual(output.get_list()[0]["st_size"], 128)

    def a_test_run_all(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list",
                                         "extracted_output_path": "./tests/examples/safe_directory"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": True},
                         "module.hashes": {"active": True, 'hashes_to_calculate': "MD5,SHA1,SHA256"},
                         "module.imagerecognitiontensorflow": {"active": True},
                         "module.metadata": {"active": True}, "module.ocrtesseract": {"active": True},
                         "module.qrbcreader": {"active": True}, "module.strings": {"active": True, "char_min": 4},
                         "module.virustotal": {"active": True}, "module.zipextractor": {"active": True}})
        path = "./tests/examples/collie.jpg"
        output = OutputFactory.get_output(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertEqual("collie" in output.get_list()[0]["imagerecognitiontensorflow"])
