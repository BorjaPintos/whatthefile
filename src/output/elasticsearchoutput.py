# -*- coding: utf-8 -*-
import ssl
from src.output.ioutput import IOutput
from elasticsearch import Elasticsearch
from ssl import create_default_context

from src.utils import auxiliar


class ElasticsearchOutput(IOutput):

    def __init__(self, params: dict = None):
        self._elasticsearch_config = params
        self._connection = self._connect()
        self._index = self._elasticsearch_config["index"]

    def _connect(self):
        host = self._elasticsearch_config["host"]
        port = self._elasticsearch_config["port"]
        scheme = self._elasticsearch_config["scheme"]
        context = None
        try:
            path_to_cafile_pem = self._elasticsearch_config["ssl_certificate_path"]
            context = create_default_context(cafile=path_to_cafile_pem)
            context.check_hostname = auxiliar.convert_to_boolean(self._elasticsearch_config["check_hostname"])
            context.verify_mode = ssl.CERT_REQUIRED if auxiliar.convert_to_boolean(self._elasticsearch_config["verify_certs"]) else ssl.CERT_NONE
            if context.verify_mode is ssl.CERT_NONE:
                import urllib3
                urllib3.disable_warnings()

        except KeyError:
            pass
        http_auth = None
        try:
            user = self._elasticsearch_config["user"]
            password = self._elasticsearch_config["password"]
            http_auth = (user, password)
        except KeyError:
            pass
        connection = Elasticsearch([host], scheme=scheme, port=port,
                                   ssl_context=context, http_auth=http_auth)
        return connection

    def __del__(self):
        if self._connection:
            self._connection.close()

    def dump_object(self, element: dict):
        self._connection.index(index=self._index, body=element)

    def dump_list(self, elements: list):
        body = []
        n_batch_elements = 0
        max = 500
        for entry in elements:
            body.append({'index': {}})
            body.append(entry)
            n_batch_elements = n_batch_elements+1
            if n_batch_elements == max:
                self._connection.bulk(index=self._index, body=body)
                n_batch_elements = 0
                body.clear()

        #elementos que quedaron fuera del ultimo batch
        if len(body) > 0:
            self._connection.bulk(index=self._index, body=body)
