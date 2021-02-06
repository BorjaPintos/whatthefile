import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.hashes.main import Constructor


class HashesTest(unittest.TestCase):

    def test_run(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result["MD5"], "9e30d001ac1e7e2a7c959be45e8e5bda")
        self.assertEqual(result["SHA1"], "85fbeea5f3ed2709867eefb9ab68859416c0bdf9")
        self.assertEqual(result["SHA224"], "e7d8b57c8ea1e23bc435b4613f3ad2ac3d536519367ee88f3dd30736")
        self.assertEqual(result["SHA256"], "d9c854cd27a99288f92d4c8fa3a7ac5de737d77a5f6325bc91b45b4125fb7d96")
        self.assertEqual(result["SHA384"], "0dd94583aae098eb5abc82d98f2db48b2ae0a711d00e660b189894192f8f83bc947020b61390c523650e44a8cafa2ee0")
        self.assertEqual(result["SHA512"], "8b779c6a71c998fa5edd82707887e632adf3e1b2d2dea4e4d3484d734b8ea8704d640145b7e23c49b749599a56d8dd1b9f86e436a9c71787a28ab1a8f8534fe1")
        self.assertEqual(result["SHA3_224"], "1434ef4be662dbc8fa461ca7ef6416527383ebf3fbe2eba83c2a9923")
        self.assertEqual(result["SHA3_256"], "24bb53e4769a6752948d5cee30b6d9cb551326e5b3082e1eb91e3c15aa1e0632")
        self.assertEqual(result["SHA3_384"], "05aed7ab3971fcd9327777f873b3ff39eb5f5b538e77518d8f8f2e270ca2892e20f2c7432996481a515cd67ce14060ce")
        self.assertEqual(result["SHA3_512"], "27cd8006cbabaab515180a1103e03742dfcfbd684b7e9c858f80774098f4029c3130cf8de8b0e188fea4ae849b9c67e531c1981b8dc8008a1fea0dc6346cf804")

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))