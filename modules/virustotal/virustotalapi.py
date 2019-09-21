# -*- coding: utf-8 -*-
import sys
import urllib
import json

apikey = 'd788bd14c1d47be3b1067b01eff561407bc0c63507c26d4566b1e60c83388b09'
vt_file_report_url = "https://www.virustotal.com/vtapi/v2/file/report"
vt_url_report_url = "https://www.virustotal.com/vtapi/v2/url/report"
vt_ip_report_url = "https://www.virustotal.com/vtapi/v2/ip-address/report"
vt_domain_report_url = "https://www.virustotal.com/vtapi/v2/domain/report"

def checkHash(hash):
  params = {'apikey': apikey, 'resource': hash}
  encoded_parameters = urllib.parse.urlencode(params).encode("utf-8")

  response_code = -1
  while response_code != 1 and response_code !=0:
    request = urllib.request.Request(vt_file_report_url, encoded_parameters)
    with urllib.request.urlopen(request) as response:
        json_response = json.loads(response.read())
    response_code = json_response['response_code']

  return json_response
