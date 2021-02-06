import unittest
from src.core import Core
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.outputfactory import OutputFactory


class CoreTest(unittest.TestCase):

    def test_run_strings(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list"},
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
        self.assertEqual(len(output.get_list()[0]["strings"]), 3)

    def test_run_hashes(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list"},
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
        self.assertEqual(len(output.get_list()[0]["hashes"]), 3)

    def a_test_run_directory(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list"},
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
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list"},
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
