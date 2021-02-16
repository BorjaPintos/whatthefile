"""Created on 12-09-2019."""
import os
import uuid

from flask import send_file, request, redirect, abort, Response
import json

from application.web.settings import Config
from src.core import Core
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration
from src.output.listoutput import ListOutput


def importRoutes(rootpath, app, config_object: Config):
    """Add user routes to app."""

    conf = WhatTheFileConfiguration()
    conf.parse_file(config_object.WHATTHEFILECONFIGFILE)
    output = ListOutput()
    core = Core(conf, output)

    @app.route(rootpath, methods=['GET', 'POST'])
    def index_or_upload_file():
        if request.method == 'GET':
            return send_file("pages/index.html", mimetype='text/html')
        else:
            if 'fileToUpload' not in request.files:
                abort(404)
            else:
                file = request.files['fileToUpload']
                binary = file.read()
                if len(binary) != 0:
                    path = _write_file(config_object, binary, os.path.basename(file.filename))
                    output.get_list().clear()
                    core.run(path)
                    _remove_file(path)
                    core.clean_safe_output_path()
                    result = output.get_list()
                    remove_internal_info(result)
                    return Response(json.dumps(result, default=str), 200, mimetype='application/json')
                else:
                    return Response(json.dumps({"error": "invalid file"}, default=str), 400,  mimetype='application/json')
                    
    @app.route(rootpath + "favicon.ico", methods=['GET'])
    def get_favicon():
        return send_file("images/favicon.png", mimetype='image/png')


def remove_internal_info(list_elements: list):
    remove_entries = ["directory", "path", "st_blksize", "st_blksize", "st_blocks", "st_flags", "st_birthtime",
                       "st_atime", "st_ctime", "st_mtime", "st_device", "st_gid","st_uid","st_mode","st_device"]

    for element in list_elements:
        for entry in remove_entries:
            try:
                del element[entry]
            except KeyError:
                pass


def _write_file(conf: Config, binary: bytes, name: str) -> str:
    path_to_save = os.path.join(conf.TEMPORAL_DIRECTORY, name)
    with open(path_to_save, "wb+") as file:
        file.write(binary)
    return path_to_save


def _remove_file(file_to_remove: str):
    os.remove(file_to_remove)
