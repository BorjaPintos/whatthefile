# -*- coding: utf-8 -*-
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.ioutput import IOutput
from elasticsearch import Elasticsearch
from ssl import create_default_context


class ElasticsearchOutput(IOutput):

    def __init__(self, conf: WhatTheFileConfiguration = None):

        self._elasticsearch_config = conf.get_section("output.elasticsearch")
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

    def dump(self, element: dict):
        self._connection.index(index=self._index, body=element)
