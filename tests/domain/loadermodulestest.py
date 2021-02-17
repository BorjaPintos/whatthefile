import unittest
from src.domain.loadermodules import LoaderModules
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration

class LoaderModulesTest(unittest.TestCase):

    def test_load_modules(self):
        config = WhatTheFileConfiguration()
        config.parse_dict(self.get_config_dict())
        modules = LoaderModules(config).get_modules()
        self.assertEqual(len(modules), len(config.get_modules_names()))

    def test_load_simple_modules(self):
        config = WhatTheFileConfiguration()
        config.parse_dict(self.get_simple_config_dict())
        modules = LoaderModules(config).get_modules()
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0].get_name(), "entropy")

    def get_config_dict(self):
        return {"whatthefile": {"modules_package": "src.modules"},
                "module.certificatereader": {"active": True},
                "module.commentextractor": {"active": True},
                "module.entropy": {"active": True},
                "module.hashes": {"active": True},
                "module.imagerecognitiontensorflow": {"active": True},
                "module.infoextractor": {"active": True},
                "module.metadata": {"active": True},
                "module.ocrtesseract": {"active": True},
                "module.qrbcreader": {"active": True},
                "module.strings": {"active": True},
                "module.tikaparser": {"active": True},
                "module.virustotal": {"active": True},
                "module.zipextractor": {"active": True}}

    def get_simple_config_dict(self):
        return {"whatthefile": {"modules_package": "src.modules"},
                "module.commentextractor": {"active": False}, "module.entropy": {"active": True},
                "module.hashes": {"active": False}, "module.imagerecognitiontensorflow": {"active": False},
                "module.metadata": {"active": False}, "module.ocrtesseract": {"active": False},
                "module.qrbcreader": {"active": False}, "module.strings": {"active": False},
                "module.virustotal": {"active": False}, "module.zipextractor": {"active": False}}
