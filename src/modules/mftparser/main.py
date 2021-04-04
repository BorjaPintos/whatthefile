# -*- coding: utf-8 -*-
from src.domain.targetfile import TargetFile
from src.domain.targetpath import TargetPath
from src.modules.imodule import IModule
from src.modules.mftparser.analyzemft import mftsession, mft
from src.output.outputfactory import OutputFactory
from src.utils import auxiliar
from src.utils.time import Time


class Constructor(IModule):

    def __init__(self):
        super().__init__()
        self._name = "mftparser"
        self._help = """Module to parse $MFT file"""
        self._author = "BorjaPintos"

    def parse_mft(self, path: str):
        session = mftsession.MftSession(path)
        session.open_files()
        session.process_mft_file()
        return session.fullmft

    def is_valid_for(self, target_file: TargetPath):
        if target_file.is_file():
            if "data" in target_file.get_type() and "MFT" in target_file.get_name():
                return True
        return False

    def _pipe_to_another_output(self, events: list):
        if "needs_pipe" in self.get_params() \
                and auxiliar.convert_to_boolean(self.get_params()["needs_pipe"]) \
                and "output" in self.get_params():
            pipe = OutputFactory.get_output_by_dict(self.get_params())
            pipe.dump_list(events)

    def run(self, target_file: TargetFile, result_of_previos_modules: dict) -> dict:
        fullmft = self.parse_mft(target_file.get_path())
        mft_objects = []
        for key, value, in fullmft.items():
            info = self._get_interesing_info(value)
            if info is not None:
                mft_objects.append(info)
        self._pipe_to_another_output(mft_objects)
        return {"mft": mft_objects}

    def _get_interesing_info(self, record):
        mft_object = {}
        if 'baad' in record:
            mft_object["error"] = "BAAD MFT Record"
            return mft_object

        mft_object["filename"] = record['filename']
        mft_object["size"] = record["size"]
        if mft_object["size"] == 0:
            return None
        mft_object["alloc_sizef"] = record["alloc_sizef"]

        if "recordnum" in record:
            mft_object["recordnum"] = record['recordnum']
        if "flags" in record:
            mft_object["active"] = record['flags'] & 0x0001
            mft_object["folder"] = True if int(record['flags']) & 0x0002 else False
            mft_object["file"] = not mft_object["folder"]

        if 'corrupt' in record:
            mft_object["error"] = "Corrupt MFT Record"
            return mft_object


        if "seq" in record:
            mft_object["seq"] = record['seq']


        mft_object["sicrtime"] = None
        mft_object["simtime"] = None
        mft_object["siatime"] = None
        mft_object["sictime"] = None
        mft_object["fncrtime"] = None
        mft_object["fnmtime"] = None
        mft_object["fnatime"] = None
        mft_object["fnctime"] = None

        if 'si' in record:
            mft_object["sicrtime"] = Time.change_output_date_format_from_epoch(record['si']['crtime'])
            mft_object["simtime"] = Time.change_output_date_format_from_epoch(record['si']['mtime'])
            mft_object["siatime"] = Time.change_output_date_format_from_epoch(record['si']['atime'])
            mft_object["sictime"] = Time.change_output_date_format_from_epoch(record['si']['ctime'])
        if record['fncnt'] > 0:
            mft_object["fncrtime"] = Time.change_output_date_format_from_epoch(record['fn', 0]['crtime'])
            mft_object["fnmtime"] = Time.change_output_date_format_from_epoch(record['fn', 0]['mtime'])
            mft_object["fnatime"] = Time.change_output_date_format_from_epoch(record['fn', 0]['atime'])
            mft_object["fnctime"] = Time.change_output_date_format_from_epoch(record['fn', 0]['ctime'])

        if 'objid' in record:
            mft_object["objid"] = record['objid']['objid']
            mft_object["orig_volid"] = record['objid']['orig_volid']
            mft_object["orig_objid"] =record['objid']['orig_objid']
            mft_object["orig_domid"] = record['objid']['orig_domid']


        if 'notes' in record:  # Log of abnormal activity related to this record
            mft_object["notes"] = record['notes']

        mft_object["ads"] = record['ads']

        return mft_object
