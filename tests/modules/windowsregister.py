# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.modules.windowsregistry.main import Constructor


class WindowsRegisterTest(unittest.TestCase):

    def test_SYSTEM(self):
        path = "./tests/examples/winregistry/SYSTEM"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual(result["SYSTEM"]["ComputerNames"][0]["name"], "WKS-WIN732BITA")
        self.assertEqual(result["SYSTEM"]["ComputerNames"][1]["name"], "WIN-V5T3CSP8U4H")
        self.assertEqual(len(result["SYSTEM"]["USBSTOR"]), 2)
        self.assertEqual(len(result["SYSTEM"]["MountedDevices"]), 11)

    def test_SOFTWARE(self):
        path = "./tests/examples/winregistry/SOFTWARE"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual(result["SOFTWARE"]["LogonUI"]["LastLoggedOnUser"], "SHIELDBASE\\rsydow")
        self.assertEqual(result["SOFTWARE"]["LogonUI"]["LastLoggedOnSAMUser"], "SHIELDBASE\\rsydow")
        self.assertEqual(result["SOFTWARE"]["SOCurrentVersion"]["ProductName"], "Windows 7 Ultimate")
        self.assertEqual(len(result["SOFTWARE"]["persistence"]), 7)
        self.assertEqual(len(result["SOFTWARE"]["profileList"]), 11)



    def test_SAM(self):
        path = "./tests/examples/winregistry/SAM"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual(len(result["SAM"]["users"]), 3)
        self.assertEqual(result["SAM"]["users"][0], "Administrator")

    def test_NTUSER(self):
        path = "./tests/examples/winregistry/NTUSER.dat"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, {})
        self.assertEqual(result["NTUSER"]["persistence"][0], "C:\\WINDOWS\\system32\\ctfmon.exe")


    def test_invalid_file(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))
