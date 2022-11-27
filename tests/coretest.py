import os
import unittest
from queue import Queue

from src.core import Core
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.outputfactory import OutputFactory


class CoreTest(unittest.TestCase):

    def test_ignore(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list", "log_output": "stdout",
                                         "safe_output_path": "./tests/examples/safe_directory"},
                         "module.hashes": {"active": True, 'hashes_to_calculate': "MD5,SHA1,SHA256"},
                         "module.ignore": {"active": True,
                                           'file_hashes_md5_to_ignore': './tests/examples/ignoredhashesmd5.txt'},
                         "module.imagerecognitiontensorflow": {"active": False},
                         "module.metadata": {"active": False}, "module.ocrtesseract": {"active": False},
                         "module.qrbcreader": {"active": False}, "module.strings": {"active": True, "char_min": 10},
                         "module.virustotal": {"active": False}, "module.zipextractor": {"active": False}})
        path = "./tests/examples/collie.jpg"
        output = OutputFactory.get_output_by_conf(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertEqual(len(output.get_list()), 0)

    def test_run_strings(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list", "log_output": "stdout",
                                         "safe_output_path": "./tests/examples/safe_directory"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": False},
                         "module.hashes": {"active": False, 'hashes_to_calculate': "MD5,SHA1,SHA256"},
                         "module.imagerecognitiontensorflow": {"active": False},
                         "module.metadata": {"active": False}, "module.ocrtesseract": {"active": False},
                         "module.qrbcreader": {"active": False}, "module.strings": {"active": True, "char_min": 10},
                         "module.virustotal": {"active": False}, "module.zipextractor": {"active": False}})
        path = "./tests/examples/collie.jpg.zip"
        output = OutputFactory.get_output_by_conf(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertEqual(output.get_list()[0]["strings"]["elements"][0], "collie.jpg")

    def test_run_zipextractor(self):
        conf = WhatTheFileConfiguration()
        output_safe_directory = "./tests/examples/safe_directory"
        conf.parse_string("""
        [whatthefile]
        modules_package = src.modules
        safe_output_path = """ + output_safe_directory + """
        output = list
        log_output = stdout
        [module.zipextractor]
        active = true
        """)

        final_file = os.path.abspath(output_safe_directory) + \
                     "/1/zipextractor/" + \
                     os.path.abspath("./tests/examples/collie.jpg.zip/collie.jpg").replace(":", "")
        final_file = os.path.abspath(final_file)
        if os.path.exists(final_file):
            os.remove(final_file)
        self._remove_test_folders(output_safe_directory)

        self.assertFalse(os.path.exists(final_file))
        path = "./tests/examples/collie.jpg.zip"
        output = OutputFactory.get_output_by_conf(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertTrue(os.path.exists(final_file))

        paths = []
        for element in output.get_list():
            paths.append(element["path"])
        self.assertTrue(os.path.abspath(final_file) in paths)

        os.remove(final_file)
        self._remove_test_folders(output_safe_directory)

    def test_zipextractor_unzip_with_zip_inside(self):

        output_safe_directory = "./tests/examples/safe_directory"
        final_file = os.path.abspath(output_safe_directory) + \
                     "/2/zipextractor/" + \
                     os.path.abspath(output_safe_directory).replace(":", "") + \
                     "/1/zipextractor/" + \
                     os.path.abspath("./tests/examples/folderzip.zip/folderzip/Surprisezip.txt.zip/Surprisezip.txt").replace(":", "")
        final_file = os.path.abspath(final_file)
        temporal_zip = os.path.abspath(output_safe_directory) + \
                       "/1/zipextractor/" + \
                       os.path.abspath("./tests/examples/folderzip.zip/folderzip/Surprisezip.txt.zip").replace(":", "")
        temporal_zip = os.path.abspath(temporal_zip)
        conf = WhatTheFileConfiguration()
        conf.parse_string("""
                [whatthefile]
                modules_package = src.modules
                safe_output_path = """ + output_safe_directory + """
                output = list
                log_output = stdout
                [module.zipextractor]
                active = true
                """)

        if os.path.exists(final_file):
            os.remove(final_file)
        self._remove_test_folders(output_safe_directory)

        self.assertFalse(os.path.exists(final_file))
        path = "./tests/examples/folderzip.zip"
        output = OutputFactory.get_output_by_conf(conf)
        core = Core(conf, output)
        core.run(path)

        paths = []
        for element in output.get_list():
            paths.append(os.path.abspath(element["path"]))

        self.assertTrue(temporal_zip in paths)
        self._remove_test_folders(output_safe_directory)

    def test_run_hashes(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list", "log_output": "stdout",
                                         "safe_output_path": "./tests/examples/safe_directory"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": False},
                         "module.hashes": {"active": True, 'hashes_to_calculate': "MD5,SHA1,SHA256"},
                         "module.imagerecognitiontensorflow": {"active": False},
                         "module.metadata": {"active": False}, "module.ocrtesseract": {"active": False},
                         "module.qrbcreader": {"active": False}, "module.strings": {"active": False, "char_min": 10},
                         "module.virustotal": {"active": False}, "module.zipextractor": {"active": False}})
        path = "./tests/examples/collie.jpg.zip"
        output = OutputFactory.get_output_by_conf(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertTrue("SHA256" in output.get_list()[0]["hashes"])
        self.assertTrue("start_module" in output.get_list()[0]["hashes"])
        self.assertTrue("end_module" in output.get_list()[0]["hashes"])
        self.assertTrue("begin_analysis" in output.get_list()[0])
        self.assertTrue("end_analysis" in output.get_list()[0])

    def test_run_directory(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list", "log_output": "stdout",
                                         "safe_output_path": "./tests/examples/safe_directory"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": True},
                         "module.hashes": {"active": True, 'hashes_to_calculate': "MD5,SHA1,SHA256"},
                         "module.imagerecognitiontensorflow": {"active": True},
                         "module.metadata": {"active": True}, "module.ocrtesseract": {"active": True},
                         "module.qrbcreader": {"active": True}, "module.strings": {"active": True, "char_min": 4},
                         "module.virustotal": {"active": False}, "module.zipextractor": {"active": True}})

        path = "./tests/examples/testdirectorydonotinsertmoreitems"
        output = OutputFactory.get_output_by_conf(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertEqual(len(output.get_list()), 3)

    def a_test_run_all(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict({"whatthefile": {"modules_package": "src.modules", "output": "list", "log_output": "stdout",
                                         "safe_output_path": "./tests/examples/safe_directory"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": True},
                         "module.hashes": {"active": True, 'hashes_to_calculate': "MD5,SHA1,SHA256"},
                         "module.imagerecognitiontensorflow": {"active": True},
                         "module.metadata": {"active": True}, "module.ocrtesseract": {"active": True},
                         "module.qrbcreader": {"active": True}, "module.strings": {"active": True, "char_min": 4},
                         "module.virustotal": {"active": True}, "module.zipextractor": {"active": True},
                         "module.tikaparser": {"active": True},  "module.whisper": {"active": True}, "module.certificatereader": {"active": True},
                         "module.browserhisstory": {"active": True}})
        path = "./tests/examples/collie.jpg"
        output = OutputFactory.get_output_by_conf(conf)
        core = Core(conf, output)
        core.run(path)
        self.assertEqual("collie" in output.get_list()[0]["imagerecognitiontensorflow"])

    @staticmethod
    def _remove_test_folders(output_safe_path):
        for root, dirs, files in os.walk(output_safe_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
