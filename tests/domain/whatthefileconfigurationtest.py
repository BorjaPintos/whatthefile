import unittest

from src.domain.whatthefileconfiguration import WhatTheFileConfiguration


class WhatTheFileConfigurationTest(unittest.TestCase):

    def test_load_conf_dict(self):
        conf = WhatTheFileConfiguration()
        conf.parse_dict(self.get_conf_dict())
        self.assertEqual(len(conf.get_modules_names()), 10)
        self.assertTrue(conf.get_property_boolean("module.hashes", "active"))
        self.assertTrue("active" in conf.get_section("module.hashes"))

    def test_load_conf_string(self):
        conf = WhatTheFileConfiguration()
        conf.parse_string(self.get_conf_string())
        self.assertEqual(len(conf.get_modules_names()), 10)
        self.assertTrue(conf.get_property_boolean("module.hashes", "active"))
        self.assertTrue("active" in conf.get_section("module.hashes"))

    def test_load_conf_file(self):
        conf = WhatTheFileConfiguration()
        conf.parse_file('./tests/examples/whatthefile.ini')
        self.assertEqual(len(conf.get_modules_names()), 10)
        self.assertTrue(conf.get_property_boolean("module.hashes", "active"))
        self.assertTrue("active" in conf.get_section("module.hashes"))

    def get_conf_dict(self):
        return {"whatthefile": {"modules_package": "src.modules"},
                         "module.commentextractor": {"active": True}, "module.entropy": {"active": True},
                         "module.hashes": {"active": True}, "module.imagerecognitiontensorflow": {"active": True},
                         "module.metadata": {"active": True}, "module.ocrtesseract": {"active": True},
                         "module.qrbcreader": {"active": True}, "module.strings": {"active": True},
                         "module.virustotal": {"active": True}, "module.zipextractor": {"active": True}}


    def get_conf_string(self):
        return """
        [whatthefile]
        modules_package = "src.modules"
        [module.commentextractor]
        active = true
        [module.entropy]
        active = true
        [module.hashes]
        active = true
        [module.imagerecognitiontensorflow]
        active = true
        [module.metadata]
        active = true
        [module.ocrtesseract]
        active = true
        [module.qrbcreader]
        active = true
        [module.strings]
        active = true
        [module.virustotal]
        active = true
        [module.zipextractor]
        active = true
        """
