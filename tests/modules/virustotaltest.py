import json
import unittest

from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.virustotal.main import Constructor
from src.modules.virustotal import virustotalapiv2 as virustotalapi

params = {"apikey": 'aasdasdasdasdasdasdasdadadadasdadasdasdasdasdasdasdasdasdasdadasdasda'}


class VirusTotalTest(unittest.TestCase):

    def test_without_apikey(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file)
        self.assertEqual(result["error"], "apikey is required")

    def test_with_invalid_apikey(self):
        path = "./tests/examples/collie.jpg"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        result = module.run(target_file, params)
        self.assertEqual(result["error"], "Invalid API KEY")

    def test_virus(self):
        path = "./tests/examples/Ransomware.WannaCry.zip"
        target_file = TargetFile(path)
        module = Constructor()
        self.assertTrue(module.is_valid_for(target_file))
        #I wan't use mocks...
        do_request_backup = virustotalapi._do_request
        get_MD5_backup = virustotalapi.get_MD5_hash

        virustotalapi._do_request = mock_response_virus_total_wannacry
        virustotalapi.get_MD5_hash = mock_hash_wannacry
        result = module.run(target_file, params)
        self.assertEqual(result["positives"], 67)

        #restoring for another tests
        virustotalapi._do_request = do_request_backup
        virustotalapi.get_MD5_hash = get_MD5_backup

    def test_invalid_file(self):
        path = "./tests/examples"
        target_file = TargetPath(path)
        module = Constructor()
        self.assertFalse(module.is_valid_for(target_file))


def mock_hash_wannacry(binary: bytes):
    return "84c82835a5d21bbcf75a61706d8ab549"


def mock_response_virus_total_wannacry(encoded_params: str):
    return {'scans': {
        'Bkav': {'detected': True, 'version': '1.3.0.9899', 'result': 'W32.Common.B4665B53', 'update': '20210204'},
        'Elastic': {'detected': True, 'version': '4.0.16', 'result': 'malicious (high confidence)',
                    'update': '20210121'},
        'DrWeb': {'detected': True, 'version': '7.0.49.9080', 'result': 'Trojan.Encoder.11432', 'update': '20210204'},
        'MicroWorld-eScan': {'detected': True, 'version': '14.0.409.0', 'result': 'Trojan.Ransom.WannaCryptor.A',
                             'update': '20210204'},
        'FireEye': {'detected': True, 'version': '32.44.1.0', 'result': 'Generic.mg.84c82835a5d21bbc',
                    'update': '20210204'},
        'CAT-QuickHeal': {'detected': True, 'version': '14.00', 'result': 'Ransom.WannaCrypt.A4', 'update': '20210204'},
        'ALYac': {'detected': True, 'version': '1.1.3.1', 'result': 'Trojan.Ransom.WannaCryptor', 'update': '20210204'},
        'Cylance': {'detected': True, 'version': '2.3.1.101', 'result': 'Unsafe', 'update': '20210204'},
        'Zillya': {'detected': True, 'version': '2.0.0.4286', 'result': 'Trojan.WannaCry.Win32.2',
                   'update': '20210204'},
        'SUPERAntiSpyware': {'detected': False, 'version': '5.6.0.1032', 'result': None, 'update': '20210129'},
        'Sangfor': {'detected': True, 'version': '1.0', 'result': 'Malware', 'update': '20210204'},
        'CrowdStrike': {'detected': True, 'version': '1.0', 'result': 'win/malicious_confidence_100% (W)',
                        'update': '20190702'},
        'Alibaba': {'detected': True, 'version': '0.3.0.5', 'result': 'Ransom:Win32/Wanna.b934b1f9',
                    'update': '20190527'},
        'K7GW': {'detected': True, 'version': '11.164.36358', 'result': 'Trojan ( 0050d7171 )', 'update': '20210204'},
        'K7AntiVirus': {'detected': True, 'version': '11.164.36362', 'result': 'Trojan ( 0050d7171 )',
                        'update': '20210204'},
        'BitDefenderTheta': {'detected': True, 'version': '7.2.37796.0', 'result': 'Gen:NN.ZexaF.34804.wt0@aGEmS3di',
                             'update': '20210201'},
        'Cyren': {'detected': True, 'version': '6.3.0.2', 'result': 'W32/Trojan.ZTSA-8671', 'update': '20210204'},
        'Symantec': {'detected': True, 'version': '1.13.0.0', 'result': 'Ransom.Wannacry', 'update': '20210204'},
        'ESET-NOD32': {'detected': True, 'version': '22758', 'result': 'Win32/Filecoder.WannaCryptor.D',
                       'update': '20210204'},
        'APEX': {'detected': True, 'version': '6.128', 'result': 'Malicious', 'update': '20210204'},
        'TotalDefense': {'detected': False, 'version': '37.1.62.1', 'result': None, 'update': '20210204'},
        'Avast': {'detected': True, 'version': '21.1.5827.0', 'result': 'Win32:WanaCry-A [Trj]', 'update': '20210204'},
        'ClamAV': {'detected': True, 'version': '0.103.1.0', 'result': 'Win.Ransomware.WannaCry-6313787-0',
                   'update': '20210204'},
        'Kaspersky': {'detected': True, 'version': '15.0.1.13', 'result': 'Trojan-Ransom.Win32.Wanna.zbu',
                      'update': '20210204'},
        'BitDefender': {'detected': True, 'version': '7.2', 'result': 'Trojan.Ransom.WannaCryptor.A',
                        'update': '20210204'},
        'NANO-Antivirus': {'detected': True, 'version': '1.0.146.25261', 'result': 'Trojan.Win32.Ransom.eoptnj',
                           'update': '20210204'},
        'Paloalto': {'detected': True, 'version': '1.0', 'result': 'generic.ml', 'update': '20210204'},
        'AegisLab': {'detected': True, 'version': '4.2', 'result': 'Trojan.Win32.Wanna.toNn', 'update': '20210204'},
        'Tencent': {'detected': True, 'version': '1.0.0.1', 'result': 'Trojan-Ransom.Win32.Wcry.a',
                    'update': '20210204'},
        'Ad-Aware': {'detected': True, 'version': '3.0.16.117', 'result': 'Trojan.Ransom.WannaCryptor.A',
                     'update': '20210204'},
        'Sophos': {'detected': True, 'version': '1.0.2.0', 'result': 'Mal/Generic-S + Troj/Ransom-EMG',
                   'update': '20210204'},
        'Comodo': {'detected': True, 'version': '33234', 'result': 'TrojWare.Win32.Ransom.WannaCrypt.B@719b9h',
                   'update': '20210204'},
        'F-Secure': {'detected': True, 'version': '12.0.86.52', 'result': 'Trojan.TR/Ransom.JB', 'update': '20210204'},
        'Baidu': {'detected': True, 'version': '1.0.0.2', 'result': 'Win32.Trojan.WannaCry.c', 'update': '20190318'},
        'VIPRE': {'detected': True, 'version': '90174', 'result': 'Trojan.Win32.Generic!BT', 'update': '20210204'},
        'TrendMicro': {'detected': True, 'version': '11.0.0.1006', 'result': 'Ransom_WANA.A', 'update': '20210204'},
        'McAfee-GW-Edition': {'detected': True, 'version': 'v2019.1.2+3728',
                              'result': 'BehavesLike.Win32.RansomWannaCry.wc', 'update': '20210204'},
        'CMC': {'detected': False, 'version': '2.10.2019.1', 'result': None, 'update': '20210130'},
        'Emsisoft': {'detected': True, 'version': '2018.12.0.1641', 'result': 'Trojan.Ransom.WannaCryptor.A (B)',
                     'update': '20210204'},
        'SentinelOne': {'detected': True, 'version': '5.0.0.9', 'result': 'Static AI - Malicious PE - Ransomware',
                        'update': '20210131'},
        'GData': {'detected': True, 'version': 'A:25.28537B:27.21842', 'result': 'Win32.Trojan-Ransom.WannaCry.A',
                  'update': '20210204'},
        'Jiangmin': {'detected': True, 'version': '16.0.100', 'result': 'Trojan.Wanna.eo', 'update': '20210204'},
        'eGambit': {'detected': True, 'version': None, 'result': 'Trojan.Generic', 'update': '20210204'},
        'Avira': {'detected': True, 'version': '8.3.3.10', 'result': 'TR/Ransom.JB', 'update': '20210204'},
        'MAX': {'detected': True, 'version': '2019.9.16.1', 'result': 'malware (ai score=100)', 'update': '20210204'},
        'Antiy-AVL': {'detected': True, 'version': '3.0.0.1', 'result': 'Trojan[Ransom]/Win32.Scatter',
                      'update': '20210204'},
        'Kingsoft': {'detected': True, 'version': '2017.9.26.565', 'result': 'Win32.Troj.Wannacry.cg.(kcloud)',
                     'update': '20210204'},
        'Gridinsoft': {'detected': True, 'version': '1.0.28.119', 'result': 'Ransom.Win32.Filecoder.dd',
                       'update': '20210204'},
        'Arcabit': {'detected': True, 'version': '1.0.0.881', 'result': 'Trojan.Ransom.WannaCryptor.A',
                    'update': '20210204'},
        'ViRobot': {'detected': True, 'version': '2014.3.20.0', 'result': 'Trojan.Win32.S.WannaCry.3514368.N',
                    'update': '20210204'},
        'ZoneAlarm': {'detected': True, 'version': '1.0', 'result': 'Trojan-Ransom.Win32.Wanna.zbu',
                      'update': '20210204'},
        'Microsoft': {'detected': True, 'version': '1.1.17800.5', 'result': 'Ransom:Win32/WannaCrypt',
                      'update': '20210204'},
        'Cynet': {'detected': True, 'version': '4.0.0.25', 'result': 'Malicious (score: 100)', 'update': '20210204'},
        'AhnLab-V3': {'detected': True, 'version': '3.19.4.10106', 'result': 'Trojan/Win32.WannaCryptor.R200571',
                      'update': '20210204'},
        'Acronis': {'detected': True, 'version': '1.1.1.80', 'result': 'suspicious', 'update': '20201023'},
        'McAfee': {'detected': True, 'version': '6.0.6.653', 'result': 'Ransom-O.g', 'update': '20210204'},
        'TACHYON': {'detected': True, 'version': '2021-02-04.05', 'result': 'Ransom/W32.WannaCry.Zen',
                    'update': '20210204'},
        'VBA32': {'detected': True, 'version': '4.4.1', 'result': 'TrojanRansom.WannaCrypt', 'update': '20210204'},
        'Malwarebytes': {'detected': True, 'version': '4.2.1.18', 'result': 'WannaCry.Ransom.Encrypt.DDS',
                         'update': '20210203'},
        'Zoner': {'detected': True, 'version': '0.0.0.0', 'result': 'Trojan.Win32.55605', 'update': '20210203'},
        'TrendMicro-HouseCall': {'detected': True, 'version': '10.0.0.1040', 'result': 'Ransom_WANA.A',
                                 'update': '20210204'},
        'Rising': {'detected': True, 'version': '25.0.0.26', 'result': 'Trojan.Win32.Rasftuby.a (CLASSIC)',
                   'update': '20210204'},
        'Yandex': {'detected': True, 'version': '5.5.2.24', 'result': 'Trojan.Igent.bUj9pX.12', 'update': '20210204'},
        'Ikarus': {'detected': True, 'version': '0.1.5.2', 'result': 'Trojan-Ransom.WannaCry', 'update': '20210204'},
        'MaxSecure': {'detected': True, 'version': '1.0.0.1', 'result': 'Trojan.Ransom.Wanna.d', 'update': '20201212'},
        'Fortinet': {'detected': True, 'version': '6.2.142.0', 'result': 'Malicious_Behavior.SB', 'update': '20210204'},
        'Webroot': {'detected': True, 'version': '1.0.0.403', 'result': 'W32.Ransomware.Wcry', 'update': '20210204'},
        'AVG': {'detected': True, 'version': '21.1.5827.0', 'result': 'Win32:WanaCry-A [Trj]', 'update': '20210204'},
        'Panda': {'detected': True, 'version': '4.6.4.2', 'result': 'Trj/RansomCrypt.K', 'update': '20210204'},
        'Qihoo-360': {'detected': True, 'version': '1.0.0.1120', 'result': 'Win32/Trojan.Multi.daf',
                      'update': '20210204'}},
        'scan_id': 'ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa-1612465505',
        'sha1': '5ff465afaabcbf0150d1a3ab2c2e74f3a4426467',
        'resource': 'ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa', 'response_code': 1,
        'scan_date': '2021-02-04 19:05:05',
        'permalink': 'https://www.virustotal.com/gui/file/ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa/detection/f-ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa-1612465505',
        'verbose_msg': 'Scan finished, information embedded', 'total': 70, 'positives': 67,
        'sha256': 'ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa',
        'md5': '84c82835a5d21bbcf75a61706d8ab549'}
