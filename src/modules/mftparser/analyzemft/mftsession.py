#!/usr/bin/env python

# Author: David Kovar [dkovar <at> gmail [dot] com]
# Name: mftsession.py
#
# Copyright (c) 2010 David Kovar. All rights reserved.
# This software is distributed under the Common Public License 1.0
#
# Date: May 2013
#


VERSION = "v3.BorjaPintos"
import sys
from src.modules.mftparser.analyzemft import mft


SIAttributeSizeXP = 72
SIAttributeSizeNT = 48

class MftSession:
    """Class to describe an entire MFT processing session"""

    @staticmethod
    def fmt_excel(date_str):
        return '="{}"'.format(date_str)

    @staticmethod
    def fmt_norm(date_str):
        return date_str


    def __init__(self, filepath : str):
        self.mft = {}
        self.fullmft = {}
        self.folders = {}
        self.debug = False
        self.mftsize = 0
        self.path_sep = "/"
        self.options = {}
        self.filename = filepath

    def open_files(self):

        try:
            self.file_mft = open(self.filename, 'rb')
        except:
            print ("Unable to open file: %s" % self.filename)
            sys.exit()

    def process_mft_file(self):

        self.build_filepaths()

        # reset the file reading
        self.num_records = 0
        self.file_mft.seek(0)
        raw_record = self.file_mft.read(1024)

        while raw_record != b"":
            record = mft.parse_record(raw_record, self.options)

            record['filename'] = self.mft[self.num_records]['filename']

            self.fullmft[self.num_records] = record

            self.num_records += 1

            if record['ads'] > 0:
                for i in range(0, record['ads']):
                    #                         print "ADS: %s" % (record['data_name', i])
                    record_ads = record.copy()

                    record_ads['filename'] = record['filename'] + ':' + record['data_name', i]
                    self.fullmft[self.num_records] = record_ads

            raw_record = self.file_mft.read(1024)

    def build_filepaths(self):
        # reset the file reading
        self.file_mft.seek(0)

        self.num_records = 0

        # 1024 is valid for current version of Windows but should really get this value from somewhere
        raw_record = self.file_mft.read(1024)
        while raw_record != b"":
            minirec = {}
            record = mft.parse_record(raw_record, self.options)
            minirec['filename'] = record['filename']
            minirec['fncnt'] = record['fncnt']
            if record['fncnt'] == 1:
                minirec['par_ref'] = record['fn', 0]['par_ref']
                minirec['name'] = record['fn', 0]['name']
            if record['fncnt'] > 1:
                minirec['par_ref'] = record['fn', 0]['par_ref']
                for i in (0, record['fncnt'] - 1):
                    # print record['fn',i]
                    if record['fn', i]['nspace'] == 0x1 or record['fn', i]['nspace'] == 0x3:
                        minirec['name'] = record['fn', i]['name']
                if minirec.get('name') is None:
                    minirec['name'] = record['fn', record['fncnt'] - 1]['name']

            self.mft[self.num_records] = minirec
            self.num_records += 1

            raw_record = self.file_mft.read(1024)

        self.gen_filepaths()

    def get_folder_path(self, seqnum):

        if seqnum not in self.mft:
            return 'Orphan'

        # If we've already figured out the path name, just return it
        if (self.mft[seqnum]['filename']) != '':
            return self.mft[seqnum]['filename']

        try:
            # if (self.mft[seqnum]['fn',0]['par_ref'] == 0) or
            # (self.mft[seqnum]['fn',0]['par_ref'] == 5):  # There should be no seq
            # number 0, not sure why I had that check in place.
            if self.mft[seqnum]['par_ref'] == 5:  # Seq number 5 is "/", root of the directory
                self.mft[seqnum]['filename'] = self.path_sep + self.mft[seqnum]['name']
                return self.mft[seqnum]['filename']
        except:  # If there was an error getting the parent's sequence number, then there is no FN record
            self.mft[seqnum]['filename'] = 'NoFNRecord'
            return self.mft[seqnum]['filename']

        # Self referential parent sequence number. The filename becomes a NoFNRecord note
        if (self.mft[seqnum]['par_ref']) == seqnum:
            self.mft[seqnum]['filename'] = 'ORPHAN' + self.path_sep + self.mft[seqnum]['name']
            return self.mft[seqnum]['filename']

        # We're not at the top of the tree and we've not hit an error
        parentpath = self.get_folder_path((self.mft[seqnum]['par_ref']))
        self.mft[seqnum]['filename'] = parentpath + self.path_sep + self.mft[seqnum]['name']

        return self.mft[seqnum]['filename']

    def gen_filepaths(self):

        for i in self.mft:
            if (self.mft[i]['filename']) == '':
                if self.mft[i]['fncnt'] > 0:
                    self.get_folder_path(i)
                else:
                    self.mft[i]['filename'] = 'NoFNRecord'
