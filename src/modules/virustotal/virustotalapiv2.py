# -*- coding: utf-8 -*-
import json
import hashlib
import urllib.parse
import urllib.request
import time
from urllib.error import HTTPError

vt_file_report_url = "https://www.virustotal.com/vtapi/v2/file/report"
vt_url_report_url = "https://www.virustotal.com/vtapi/v2/url/report"
vt_ip_report_url = "https://www.virustotal.com/vtapi/v2/ip-address/report"
vt_domain_report_url = "https://www.virustotal.com/vtapi/v2/domain/report"


def check_hash(apikey: str, hash: str):
    params = {'apikey': apikey, 'resource': hash}
    encoded_parameters = urllib.parse.urlencode(params).encode("utf-8")
    response_code = -2
    while response_code == -2:
        json_response = _do_request(encoded_parameters)
        if "error" in json_response:
          return json_response
        response_code = json_response['response_code']
        if (response_code == -2):
            time.sleep(1)
    return json_response


def _do_request(encoded_parameters: str):
    try:
        request = urllib.request.Request(vt_file_report_url, encoded_parameters)
        response = urllib.request.urlopen(request)
    except HTTPError as e:
        if e.code == 403:
            return {"error": "Invalid API KEY"}
    return json.loads(response.read())


def get_MD5_hash(binary: bytes):
    hasher = hashlib.md5()
    hasher.update(binary)
    md5 = hasher.hexdigest()
    return md5
