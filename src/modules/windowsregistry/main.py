# -*- coding: utf-8 -*-
import traceback

from regipy import RegistryValueNotFoundException, RegistryKeyNotFoundException
from regipy.utils import get_subkey_values_from_list

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
from regipy.registry import RegistryHive

from src.utils.time import Time


class Constructor(IModule):
    PERSISTENCE_ENTRIES_NTUSER = [
        r'\Software\Microsoft\Windows NT\CurrentVersion\Run',
        r'\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\Run',
        r'\Software\Microsoft\Windows NT\CurrentVersion\Terminal Server\Install\Software\Microsoft\Windows\CurrentVersion\RunOnce',
        r'\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run',
        r'\Software\Microsoft\Windows\CurrentVersion\Run',
        r'\Software\Microsoft\Windows\CurrentVersion\RunOnce',
        r'\Software\Microsoft\Windows\CurrentVersion\RunOnceEx',
        r'\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup',
        r'\Software\Microsoft\Windows\CurrentVersion\RunServices',
        r'\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce',
        r'\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run',
        r'\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run',
        r'\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce',
        r'\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx',
        r'\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce\Setup',
        r'\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify',
    ]

    PERSISTENCE_ENTRIES_SOFTWARE = [
        r'\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run',
        r'\Microsoft\Windows\CurrentVersion\Run',
        r'\Microsoft\Windows\CurrentVersion\RunOnce',
        r'\Microsoft\Windows\CurrentVersion\RunOnce\Setup',
        r'\Microsoft\Windows\CurrentVersion\RunOnceEx',
        r'\Wow6432Node\Microsoft\Windows\CurrentVersion\Run',
        r'\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce',
        r'\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce\Setup',
        r'\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx',
        r'\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run',
        r'\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify'
    ]

    def __init__(self):
        super().__init__()
        self._name = "windowsRegistry"
        self._help = """Module to get information about windows registry hives"""
        self._author = "BorjaPintos"

    def is_valid_for(self, target_file: TargetPath):
        if "Windows registry" in target_file.get_type() and \
                target_file.is_file():
            return True
        return False

    def _get_computer_name(self, reg: RegistryHive):
        names = []
        for subkey_path in reg.get_control_sets(r'Control\ComputerName\ComputerName'):
            subkey = reg.get_key(subkey_path)
            try:
                names.append({
                    'name': subkey.get_value('ComputerName'),
                    'timestamp': Time.change_output_date_format_from_epoch(subkey.header.last_modified)
                })
            except RegistryValueNotFoundException as ex:
                continue
        return names

    def _get_last_logon(self, reg: RegistryHive):
        try:
            key = reg.get_key(r'\Microsoft\Windows\CurrentVersion\Authentication\LogonUI')
            return {
                "LastLoggedOnUser": key.get_value("LastLoggedOnUser"),
                "LastLoggedOnSAMUser": key.get_value("LastLoggedOnSAMUser")}
        except:
            pass

    def _get_so_version(self, reg: RegistryHive):

        try:
            subkey = reg.get_key(r'\Microsoft\Windows NT\CurrentVersion')
            return {
                'ProductName': subkey.get_value('ProductName'),
                'ReleaseId': subkey.get_value('ReleaseId')
            }
        except:
            return None

    def _get_persistence(self, reg: RegistryHive, persistence_keys: list):
        all_entries = get_subkey_values_from_list(reg, persistence_keys)
        values_paths = []
        for key_entry, entry_values in all_entries.items():
            for value in entry_values["values"]:
                values_paths.append(value.value)
        return values_paths

    def _get_get_runmru(self, reg: RegistryHive):
        "TODO pendiente de que tenga un ejemplo con datos"
        try:
            subkey = reg.get_key(r'\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU')
            order = subkey.get_value('MRUList')
            list = []
            if order:
                for char in order:
                    try:
                        value = subkey.get_value(char)
                        if value:
                            list.append(value)
                    except:
                        pass
            return list
        except:
            return None

    def _userassist(self, reg: RegistryHive):
        try:
            "TODO pendiente de que tenga un ejemplo con datos"
            subkey = reg.get_key(r'\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist')
            list = []
            for a in subkey.iter_subkeys():
                list.append(a.name)
            return list
        except:
            return None

    def _get_wifis(self, reg: RegistryHive):
        try:
            "ESto solo vale para XP"
            "TODO pendiente de que tenga un ejemplo con datos"
            subkey = reg.get_key(r'\Microsoft\WZCSVC\Parameters\Interfaces')
            list = []
            for a in subkey.iter_subkeys():
                list.append(a.name)
            return list
        except:
            return None

    def _get_usbstorage(self, reg: RegistryHive):
        usbs = []

        try:
            for subkey_path in reg.get_control_sets(r'Enum\USBSTOR'):
                subkey = reg.get_key(subkey_path)
                for usb in subkey.iter_subkeys():
                    usbs.append({
                        'device': usb.name,
                        'timestamp': Time.change_output_date_format_from_epoch(usb.header.last_modified)
                    })
        except:
            return None
        return usbs

    def _get_profilelist(self, reg: RegistryHive):
        profiles = []
        subkey = reg.get_key(r'\Microsoft\Windows NT\CurrentVersion\ProfileList')
        for profile in subkey.iter_subkeys():
            try:
                profiles.append({
                    'Sid': profile.name,
                    'Guid': profile.get_value(r'Guid') if profile.get_value(r'Guid') is not None else "",
                    'ProfileImagePath': profile.get_value(r'ProfileImagePath')
                })
            except RegistryValueNotFoundException as ex:
                continue
        return profiles

    def _get_mounted_devices(self, reg: RegistryHive):
        devices = []
        subkey = reg.get_key(r'\MountedDevices')
        for device in subkey.iter_values():
            devices.append(device.name)
        return devices

    def _get_system_info(self, reg: RegistryHive):
        if reg.hive_type == 'system':
            return {
                "ComputerNames": self._get_computer_name(reg),
                "USBSTOR": self._get_usbstorage(reg),
                "MountedDevices": self._get_mounted_devices(reg)
            }

    def _get_sofware_info(self, reg: RegistryHive):
        if reg.hive_type == 'software':
            return {
                "LogonUI": self._get_last_logon(reg),
                "SOCurrentVersion": self._get_so_version(reg),
                "persistence": self._get_persistence(reg, Constructor.PERSISTENCE_ENTRIES_SOFTWARE),
                "profileList" : self._get_profilelist(reg),
                "xp_wifis": self._get_wifis(reg)
            }

    def _get_ntuser_info(self, reg: RegistryHive):
        if reg.hive_type == 'ntuser':
            return {
                "persistence": self._get_persistence(reg, Constructor.PERSISTENCE_ENTRIES_NTUSER),
                "runMRU": self._get_get_runmru(reg),
                "userAssist": self._userassist(reg)
            }

    def _get_users(self, reg: RegistryHive):
        key = reg.get_key(r'\SAM\Domains\Account\Users\Names')
        users = []
        for user in key.iter_subkeys():
            users.append(user.name)
        return users

    def _get_sam_info(self, reg: RegistryHive):
        if reg.hive_type == 'sam':
            return {
                "users": self._get_users(reg)
            }

    def _extract_data(self, path: str):
        reg = RegistryHive(path)
        return self._clean_nones({
            "SYSTEM": self._get_system_info(reg),
            "SOFTWARE": self._get_sofware_info(reg),
            "NTUSER": self._get_ntuser_info(reg),
            "SAM": self._get_sam_info(reg)
        })

    def _clean_nones(self, dictionary: dict):
        keys = list(dictionary.keys())
        for key in keys:
            if dictionary[key] is None:
                del dictionary[key]
            elif isinstance(dictionary[key], dict):
                self._clean_nones(dictionary[key])
        return dictionary

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        return self._extract_data(target_file.get_path())
