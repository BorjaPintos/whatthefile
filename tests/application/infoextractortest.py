# -*- coding: utf-8 -*-
import unittest
from src.domain.targetfile import TargetFile
from src.application.infoextractor.infoextactor import Infoextractor
from src.utils import auxiliar


class InfoExtractorTest(unittest.TestCase):

    def test_info(self):
        path = "./tests/examples/importantinfo.txt"
        target_file = TargetFile(path)
        infoextractor = Infoextractor()
        result = infoextractor.run({
            "strings": {"elements": auxiliar.get_str_utf_8_from_bytes(target_file.get_binary())}
        })
        self.assertEqual(result["emails"], ['cosa@cosa.com', 'cosita2@cosita.com', 'cosita3@pron.com'])
        self.assertEqual(result["IBANs"],
                         ['ES12 3456 7890 1234 5678 9012', 'ES1234567890123456789012', 'ES12-3456-7890-1234-5678-9011'])
        self.assertEqual(result["URLs"], ['http://google.es', 'http://facebook.com', 'ftp://localhost:2222',
                                          'mysql://host:puerto/database', 'http://iamgenmolona.com'])
        self.assertEqual(result["Bitcoin"], ['3KVkBhzGfAH4s4tGZA9yfbUJwhcwHBkdKC'])

    def test_extract_info_from_other_modules(self):
        infoextractor = Infoextractor()
        result = infoextractor.run(self.get_info_modules_prev_dummy())
        self.assertEqual(result["emails"],
                         ['cosa@cosa.com', 'cosita2@cosita.com', 'cosita3@pron.com', 'nope@nope.nope',
                          "thresh@thresh.com", "blur@blur.com"])
        self.assertEqual(result["IBANs"],
                         ['ES12 3456 7890 1234 5678 9012', 'ES1234567890123456789012', 'ES12-3456-7890-1234-5678-9011'])
        self.assertEqual(result["URLs"], ['http://google.es', 'http://facebook.com', 'ftp://localhost:2222',
                                          'mysql://host:puerto/database', 'http://iamgenmolona.com',
                                          'http://metadata1.com', 'http://metadata2.com', 'https://qrbceader1.es',
                                          'https://qrbceader2.es'])
        self.assertEqual(result["Bitcoin"], ['3KVkBhzGfAH4s4tGZA9yfbUJwhcwHBkdKC'])

    def test_with_not_info(self):
        infoextractor = Infoextractor()
        result = infoextractor.run({})
        self.assertTrue("emails" not in result)
        self.assertTrue("URLs" not in result)
        self.assertTrue("IBANs" not in result)

    def get_info_modules_prev_dummy(self):
        return {
            'certificatereader': {'serial_number': 12029605598864358562, 'version': 'v1', 'extensions': [],
                                  'nor_valid_after': '2031-02-11T19:42:51.000000',
                                  'nor_valid_before': '2021-02-13T19:42:51.000000',
                                  'issuer': '1.2.840.113549.1.9.1=nope@nope.nope,CN=whatthefile,OU=Research,O=Research,L=Santiago de Compostela,ST=Galicia,C=es',
                                  'subject': '1.2.840.113549.1.9.1=nope@nope.nope,CN=whatthefile,OU=Research,O=Research,L=Santiago de Compostela,ST=Galicia,C=es',
                                  'signature': 'a7f28469861a7a5766b0077fb4b1beca7633ba184e8b0c3935d3b1e159726762a402cf7eb951b5c1f3cc3559c44b4b1d94c4e7e3558529704d489c59d616bdfd11ffa2f6020cc7a962ceecffeba655bd41f49b5fd143b779e852b9e0a43a560f110a8dc409837167fa280b21b44edbd45e33817e6e05fb0f80b8cbd9fd5af471f41fd87bc80cb53b758f68013d3da82e1f6191692eddca0103891b913edd51d04aa829548983bba34017ab89f42ea309b9d58ea55f66daeb3235a3c4e65f2772d0be9f99c67a922f873b47a19b94d5dc533c97a2dde6f85709f671281ee1704edaabe46796a27327005238bb80c8e31376b0e21abb03d2e26a82111cd27da8e7',
                                  'signature_algorithm_hash': 'sha256',
                                  'signature_algorithm': 'sha256WithRSAEncryption', 'key_size': 2048,
                                  'public_key': {'e': 65537,
                                                 'n': 21621845509361630704557909745540130871407083178392027067149576490740301148934618495535398207258204596620675833354082578418969237227574573536517651489634029285360838618951419768905963936742333242067417423464777710351303288971733299632061433493125444484913348558983485750876736782109553861563430635889761277570080535032326835588048941841795159967612943121061698215956105849962108961414840465679905513511510275849474146643222503106301741271915135133866013510181273311105468480372471584859280885706212003465298681184752936938522129435046380155890389233470723624597215164102251588653194915264021776537504043553480686212069},
                                  'start_module': '2021-02-19T15:57:26.002509',
                                  'end_module': '2021-02-19T15:57:26.061908',
                                  'total_module_duration': 0.05939888954162598},
            "qrbcreader": {"0": "https://qrbceader1.es",
                           "1": "https://qrbceader2.es",
                           "2": "3KVkBhzGfAH4s4tGZA9yfbUJwhcwHBkdKC",
                           "3": "3AG4AbABvAGEAZABBAG4AZABJAG4AcwB",
                           "4": "La 2 es una btc real, la 3 es un fake"},
            "tikaparser": {"content": """Esto es un fichero con un email cosa@cosa.com
                                        cosita2@cosita.com y cosita3@pron.com

                                        también podemos encontrar uls como http://google.es http://facebook.com
                                        incluso ftp://localhost:2222
                                        mysql://host:puerto/database y este es un ejemplo de un servicio de mysql

                                        <src="http://iamgenmolona.com">"""},
            "strings": {
                "elements": """números de cuenta: ES12 3456 7890 1234 5678 9012 este es uno 
                    Este otro ES1234567890123456789012 
                    y aquí intento engañar con este verdadero 
                    ES12-3456-7890-1234-5678-9011 y este falso ES12-3456-7890-1234-5678-901""",
                "n_elements": 1,
                ">=": 6
            },
            "metadata": {"key": ["url1", "url2"], "values": ["http://metadata1.com", "http://metadata2.com"],
                         "key_values": ["url1:http://metadata1.com", "url3:http://metadata3.com"]},
            "ocrtesseract": {"Thresh": "thresh@thresh.com",
                             "Blur": "blur@blur.com"}
        }
