import os
from src.domain.whatthefileconfiguration import WhatTheFileConfiguration


class Safe:
    safe_output_path = None
    i = 0

    @staticmethod
    def next_rotation():
        Safe.i = Safe.i + 1
        Safe.safe_output_path = os.path.join(os.path.dirname(Safe.safe_output_path), "./" + str(Safe.i)) \
            .replace("/./", "/").replace("/../", "/")
        if not os.path.exists(Safe.safe_output_path):
            os.mkdir(Safe.safe_output_path)

    @staticmethod
    def configure(conf: WhatTheFileConfiguration):
        try:
            Safe.i = 0
            Safe.safe_output_path = os.path.abspath(os.path.join(conf.get_property("whatthefile", "safe_output_path"),
                                                                 "./" + str(Safe.i)).replace("/./", "/").replace("/../",
                                                                                                                 "/"))
            Safe.next_rotation()
        except:
            raise BaseException("safe_output_path is required")

    @staticmethod
    def create_file(path: str, binary: bytes) -> str:
        subpath = path.replace("/./", "/").replace("/../", "/")
        path_to_save = os.path.join(Safe.safe_output_path, subpath).replace("/./", "/").replace("/../", "/")
        Safe._create_folders(os.path.dirname(subpath))
        with open(path_to_save, "wb+") as file:
            file.write(binary)
        return path_to_save

    @staticmethod
    def _create_folders(sub_path: str):
        folders = []
        folder = sub_path
        while folder not in ["", "/"]:
            if folder != ".":
                folders.append(folder)
            folder = os.path.dirname(folder)
        folders.reverse()
        for path in folders:
            path_to_create = os.path.join(Safe.safe_output_path, "./" + path).replace("/./", "/").replace("/../", "/")
            if not os.path.exists(path_to_create):
                os.mkdir(path_to_create)

    @staticmethod
    def reset(conf: WhatTheFileConfiguration):
        safe_output_path = conf.get_property("whatthefile", "safe_output_path")
        for element in os.listdir(safe_output_path):
            Safe._delete(os.path.join(safe_output_path, "./" + str(element)))
        Safe.configure(conf)

    @staticmethod
    def _delete(path: str):
        if os.path.isdir(path):
            for element in os.listdir(path):
                Safe._delete(os.path.join(path, "./" + str(element)).replace("/./", "/").replace("/../", "/"))
            os.rmdir(path)
        else:
            os.remove(path)
