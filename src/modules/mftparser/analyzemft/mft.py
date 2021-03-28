#!/usr/bin/env python

# Author: David Kovar [dkovar <at> gmail [dot] com]
# Name: mft.py
#
# Copyright (c) 2010 David Kovar. All rights reserved.
# This software is distributed under the Common Public License 1.0
#
# Date: May 2013
#

import binascii
import json
import ctypes
import struct
from optparse import OptionParser

from src.modules.mftparser.analyzemft import bitparse, mftutils

def parse_record(raw_record, options):
    if len(raw_record) == 0:
        return None
    record = {
        'filename': '',
        'notes': '',
        'ads': 0,
        'datacnt': 0,
    }
    decode_mft_header(record, raw_record)

    # HACK: Apply the NTFS fixup on a 1024 byte record.
    # Note that the fixup is only applied locally to this function.
    if record['seq_number'] == raw_record[510:512] and record['seq_number'] == raw_record[1022:1024]:
        temp_raw_record = raw_record[:510]
        temp_raw_record += (record['seq_attr1'])
        temp_raw_record += raw_record[512:1022]
        temp_raw_record += (record['seq_attr2'])

        raw_record = temp_raw_record

    record_number = record['recordnum']

    if record['magic'] == 0x44414142:
        record['baad'] = True
        return record

    if record['magic'] != 0x454c4946:
        record['corrupt'] = True
        return record

    read_ptr = record['attr_off']

    # How should we preserve the multiple attributes? Do we need to preserve them all?
    while read_ptr < 1024:

        atr_record = decode_atr_header(raw_record[read_ptr:])
        if atr_record['type'] == 0xffffffff:  # End of attributes
            break

        if atr_record['nlen'] > 0:
            record_bytes = raw_record[
                read_ptr + atr_record['name_off']: read_ptr + atr_record['name_off'] + atr_record['nlen'] * 2]
            atr_record['name'] = record_bytes.decode('utf-16')
        else:
            atr_record['name'] = ''

        if atr_record['type'] == 0x10:  # Standard Information
            si_record = decode_si_attribute(raw_record[read_ptr + atr_record['soff']:])
            record['si'] = si_record

        elif atr_record['type'] == 0x20:  # Attribute list
            if atr_record['res'] == 0:
                al_record = decode_attribute_list(raw_record[read_ptr + atr_record['soff']:], record)
                record['al'] = al_record
            else:
                record['al'] = None

        elif atr_record['type'] == 0x30:  # File name
            fn_record = decode_fn_attribute(raw_record[read_ptr + atr_record['soff']:], record)
            record['fn', record['fncnt']] = fn_record
            record['fncnt'] += 1
            if fn_record['crtime'] != 0:
                pass

        elif atr_record['type'] == 0x40:  # Object ID
            object_id_record = decode_object_id(raw_record[read_ptr + atr_record['soff']:])
            record['objid'] = object_id_record

        elif atr_record['type'] == 0x50:  # Security descriptor
            record['sd'] = True

        elif atr_record['type'] == 0x60:  # Volume name
            record['volname'] = True

        elif atr_record['type'] == 0x70:  # Volume information
            volume_info_record = decode_volume_info(raw_record[read_ptr + atr_record['soff']:], options)
            record['volinfo'] = volume_info_record

        elif atr_record['type'] == 0x80:  # Data
            if atr_record['name'] != '':
                record['data_name', record['ads']] = atr_record['name']
                record['ads'] += 1
            if atr_record['res'] == 0:
                data_attribute = decode_data_attribute(raw_record[read_ptr + atr_record['soff']:], atr_record)
            else:
                data_attribute = {
                    'ndataruns': atr_record['ndataruns'],
                    'dataruns': atr_record['dataruns'],
                    'drunerror': atr_record['drunerror'],
                }
            record['data', record['datacnt']] = data_attribute
            record['datacnt'] += 1


        elif atr_record['type'] == 0x90:  # Index root
            record['indexroot'] = True

        elif atr_record['type'] == 0xA0:  # Index allocation
            record['indexallocation'] = True

        elif atr_record['type'] == 0xB0:  # Bitmap
            record['bitmap'] = True

        elif atr_record['type'] == 0xC0:  # Reparse point
            record['reparsepoint'] = True

        elif atr_record['type'] == 0xD0:  # EA Information
            record['eainfo'] = True

        elif atr_record['type'] == 0xE0:  # EA
            record['ea'] = True

        elif atr_record['type'] == 0xF0:  # Property set
            record['propertyset'] = True

        elif atr_record['type'] == 0x100:  # Logged utility stream
            record['loggedutility'] = True

        if atr_record['len'] > 0:
            read_ptr = read_ptr + atr_record['len']
        else:
            break

    #anomaly_detect(record)

    return record

# MD5|name|inode|mode_as_string|UID|GID|size|atime|mtime|ctime|crtime
def mft_to_json(record):
    json_object = {}
    
    if record.has_key('si'):
        #print "Make Me JSON %s, %s, %s , %s, %s"  % (str(record['recordnum']), str(record['filename']), str(record['magic']), str(record['size']), record['si']['mtime'].dtstr)
        json_object['filename'] = str(record['filename'])
        json_object['recordnumber'] = str(record['recordnum'])
        json_object['recordtype'] = str(record['recordtype'])
    else:
        #print str(record['recordnum'])  + str(record['filename'])
        json_object['filename'] = "nFn"
        json_object['recordnumber'] = str(record['recordnum'])        
        
    return json_object

def add_note(record, s):
    if record['notes'] == '':
        record['notes'] = "%s" % s
    else:
        record['notes'] = "%s | %s |" % (record['notes'], s)


def decode_mft_header(record, raw_record):
    record['magic'] = struct.unpack("<I", raw_record[:4])[0]
    record['upd_off'] = struct.unpack("<H", raw_record[4:6])[0]
    record['upd_cnt'] = struct.unpack("<H", raw_record[6:8])[0]
    record['lsn'] = struct.unpack("<d", raw_record[8:16])[0]
    record['seq'] = struct.unpack("<H", raw_record[16:18])[0]
    record['link'] = struct.unpack("<H", raw_record[18:20])[0]
    record['attr_off'] = struct.unpack("<H", raw_record[20:22])[0]
    record['flags'] = struct.unpack("<H", raw_record[22:24])[0]
    record['size'] = struct.unpack("<I", raw_record[24:28])[0]
    record['alloc_sizef'] = struct.unpack("<I", raw_record[28:32])[0]
    record['base_ref'] = struct.unpack("<Lxx", raw_record[32:38])[0]
    record['base_seq'] = struct.unpack("<H", raw_record[38:40])[0]
    record['next_attrid'] = struct.unpack("<H", raw_record[40:42])[0]
    record['f1'] = raw_record[42:44]  # Padding
    record['recordnum'] = struct.unpack("<I", raw_record[44:48])[0]  # Number of this MFT Record
    record['seq_number'] = raw_record[48:50]  # Sequence number
    # Sequence attributes location are hardcoded since the record size is hardcoded too.
    # The following two lines are subject to NTFS versions. See:
    # https://github.com/libyal/libfsntfs/blob/master/documentation/New%20Technologies%20File%20System%20(NTFS).asciidoc#mft-entry-header
    if record['upd_off'] == 42:
        record['seq_attr1'] = raw_record[44:46]  # Sequence attribute for sector 1
        record['seq_attr2'] = raw_record[46:58]  # Sequence attribute for sector 2
    else:
        record['seq_attr1'] = raw_record[50:52]  # Sequence attribute for sector 1
        record['seq_attr2'] = raw_record[52:54]  # Sequence attribute for sector 2
    record['fncnt'] = 0  # Counter for number of FN attributes
    record['datacnt'] = 0  # Counter for number of $DATA attributes


def decode_mft_magic(record):
    if record['magic'] == 0x454c4946:
        return "Good"
    elif record['magic'] == 0x44414142:
        return 'Bad'
    elif record['magic'] == 0x00000000:
        return 'Zero'
    else:
        return 'Unknown'


# decodeMFTisactive and decodeMFTrecordtype both look at the flags field in the MFT header.
# The first bit indicates if the record is active or inactive. The second bit indicates if it
# is a file or a folder.
#
# I had this coded incorrectly initially. Spencer Lynch identified and fixed the code. Many thanks!

def decode_mft_isactive(record):
    if record['flags'] & 0x0001:
        return 'Active'
    else:
        return 'Inactive'


def decode_mft_recordtype(record):
    if int(record['flags']) & 0x0002:
        tmp_buffer = 'Folder'
    else:
        tmp_buffer = 'File'
    if int(record['flags']) & 0x0004:
        tmp_buffer = "%s %s" % (tmp_buffer, '+ Unknown1')
    if int(record['flags']) & 0x0008:
        tmp_buffer = "%s %s" % (tmp_buffer, '+ Unknown2')

    return tmp_buffer


def decode_atr_header(s):
    d = {'type': struct.unpack("<L", s[:4])[0]}
    if d['type'] == 0xffffffff:
        return d

    d['len'] = struct.unpack("<L", s[4:8])[0]
    d['res'] = struct.unpack("B", bytes([s[8]]))[0]
    d['nlen'] = struct.unpack("B", bytes([s[9]]))[0]
    d['name_off'] = struct.unpack("<H", s[10:12])[0]
    d['flags'] = struct.unpack("<H", s[12:14])[0]
    d['id'] = struct.unpack("<H", s[14:16])[0]
    if d['res'] == 0:
        d['ssize'] = struct.unpack("<L", s[16:20])[0]  # dwLength
        d['soff'] = struct.unpack("<H", s[20:22])[0]  # wAttrOffset
        d['idxflag'] = struct.unpack("B", bytes([s[22]]))[0]  # uchIndexedTag
        _ = struct.unpack("B", bytes([s[23]]))[0]  # Padding
    else:
        # d['start_vcn'] = struct.unpack("<Lxxxx",s[16:24])[0]    # n64StartVCN
        # d['last_vcn'] = struct.unpack("<Lxxxx",s[24:32])[0]     # n64EndVCN
        d['start_vcn'] = struct.unpack("<Q", s[16:24])[0]  # n64StartVCN
        d['last_vcn'] = struct.unpack("<Q", s[24:32])[0]  # n64EndVCN
        d['run_off'] = struct.unpack("<H", s[32:34])[0]  # wDataRunOffset (in clusters, from start of partition?)
        d['compsize'] = struct.unpack("<H", s[34:36])[0]  # wCompressionSize
        _ = struct.unpack("<I", s[36:40])[0]  # Padding
        d['allocsize'] = struct.unpack("<Lxxxx", s[40:48])[0]  # n64AllocSize
        d['realsize'] = struct.unpack("<Lxxxx", s[48:56])[0]  # n64RealSize
        d['streamsize'] = struct.unpack("<Lxxxx", s[56:64])[0]  # n64StreamSize
        (d['ndataruns'], d['dataruns'], d['drunerror']) = unpack_dataruns(s[64:])

    return d


# Dataruns - http://inform.pucp.edu.pe/~inf232/Ntfs/ntfs_doc_v0.5/concepts/data_runs.html
def unpack_dataruns(datarun_str):
    dataruns = []
    numruns = 0
    pos = 0
    prevoffset = 0
    error = ''

    c_uint8 = ctypes.c_uint8

    class LengthBits(ctypes.LittleEndianStructure):
        _fields_ = [
            ("lenlen", c_uint8, 4),
            ("offlen", c_uint8, 4),
        ]

    class Lengths(ctypes.Union):
        _fields_ = [("b", LengthBits),
                    ("asbyte", c_uint8)]

    lengths = Lengths()

    # mftutils.hexdump(str,':',16)

    while True:
        lengths.asbyte = struct.unpack("B", bytes([datarun_str[pos]]))[0]
        pos += 1
        if lengths.asbyte == 0x00:
            break

        if lengths.b.lenlen > 6 or lengths.b.lenlen == 0:
            error = "Datarun oddity."
            break

        bit_len = bitparse.parse_little_endian_signed(datarun_str[pos:pos + lengths.b.lenlen])

        # print lengths.b.lenlen, lengths.b.offlen, bit_len
        pos += lengths.b.lenlen

        if lengths.b.offlen > 0:
            offset = bitparse.parse_little_endian_signed(datarun_str[pos:pos + lengths.b.offlen])
            offset = offset + prevoffset
            prevoffset = offset
            pos += lengths.b.offlen
        else:  # Sparse
            offset = 0
            pos += 1

        dataruns.append([bit_len, offset])
        numruns += 1

        # print "Lenlen: %d Offlen: %d Len: %d Offset: %d" % (lengths.b.lenlen, lengths.b.offlen, bit_len, offset)

    return numruns, dataruns, error


def decode_si_attribute(s):
    d = {
        'crtime': mftutils.WindowsTime(struct.unpack("<L", s[:4])[0], struct.unpack("<L", s[4:8])[0]).get_unix_time(),
        'mtime': mftutils.WindowsTime(struct.unpack("<L", s[8:12])[0], struct.unpack("<L", s[12:16])[0]).get_unix_time(),
        'ctime': mftutils.WindowsTime(struct.unpack("<L", s[16:20])[0], struct.unpack("<L", s[20:24])[0]).get_unix_time(),
        'atime': mftutils.WindowsTime(struct.unpack("<L", s[24:28])[0], struct.unpack("<L", s[28:32])[0]).get_unix_time(),
        'dos': struct.unpack("<I", s[32:36])[0], 'maxver': struct.unpack("<I", s[36:40])[0],
        'ver': struct.unpack("<I", s[40:44])[0], 'class_id': struct.unpack("<I", s[44:48])[0],
        'own_id': struct.unpack("<I", s[48:52])[0], 'sec_id': struct.unpack("<I", s[52:56])[0],
        'quota': struct.unpack("<d", s[56:64])[0], 'usn': struct.unpack("<d", s[64:72])[0],
    }

    return d


def decode_fn_attribute(s, _):
    # File name attributes can have null dates.

    d = {
        'par_ref': struct.unpack("<Lxx", s[:6])[0], 'par_seq': struct.unpack("<H", s[6:8])[0],
        'crtime': mftutils.WindowsTime(struct.unpack("<L", s[8:12])[0], struct.unpack("<L", s[12:16])[0]).get_unix_time(),
        'mtime': mftutils.WindowsTime(struct.unpack("<L", s[16:20])[0], struct.unpack("<L", s[20:24])[0]).get_unix_time(),
        'ctime': mftutils.WindowsTime(struct.unpack("<L", s[24:28])[0], struct.unpack("<L", s[28:32])[0]).get_unix_time(),
        'atime': mftutils.WindowsTime(struct.unpack("<L", s[32:36])[0], struct.unpack("<L", s[36:40])[0]).get_unix_time(),
        'alloc_fsize': struct.unpack("<q", s[40:48])[0], 'real_fsize': struct.unpack("<q", s[48:56])[0],
        'flags': struct.unpack("<d", s[56:64])[0], 'nlen': struct.unpack("B", bytes([s[64]]))[0],
        'nspace': struct.unpack("B", bytes([s[65]]))[0],
    }

    attr_bytes = s[66:66 + d['nlen'] * 2]
    try:
        d['name'] = attr_bytes.decode('utf-16')
    except:
        d['name'] = 'UnableToDecodeFilename'

    return d


def decode_attribute_list(s, _):
    d = {
        'type': struct.unpack("<I", s[:4])[0], 'len': struct.unpack("<H", s[4:6])[0],
        'nlen': struct.unpack("B", bytes([s[6]]))[0], 'f1': struct.unpack("B", bytes([s[7]]))[0],
        'start_vcn': struct.unpack("<d", s[8:16])[0], 'file_ref': struct.unpack("<Lxx", s[16:22])[0],
        'seq': struct.unpack("<H", s[22:24])[0], 'id': struct.unpack("<H", s[24:26])[0],
    }

    attr_bytes = s[26:26 + d['nlen'] * 2]
    d['name'] = attr_bytes.decode('utf-16').encode('utf-8')

    return d


def decode_volume_info(s, options):
    d = {
        'f1': struct.unpack("<d", s[:8])[0], 'maj_ver': struct.unpack("B", bytes([s[8]]))[0],
        'min_ver': struct.unpack("B", bytes([s[9]]))[0], 'flags': struct.unpack("<H", s[10:12])[0],
        'f2': struct.unpack("<I", s[12:16])[0],
    }

    return d


# Decode a Resident Data Attribute
def decode_data_attribute(s, at_rrecord):
    d = {'data': s[:at_rrecord['ssize']]}

    #        print 'Data: ', d['data']
    return d


def decode_object_id(s):
    d = {
        'objid': object_id(s[0:16]),
        'orig_volid': object_id(s[16:32]),
        'orig_objid': object_id(s[32:48]),
        'orig_domid': object_id(s[48:64]),
    }

    return d


def object_id(s):
    if s == 0:
        objstr = 'Undefined'
    else:
        objstr = '-'.join(map(bytes.decode, map(binascii.hexlify, (s[0:4][::-1], s[4:6][::-1], \
                                                                   s[6:8][::-1], s[8:10], s[10:]))))

    return objstr


def anomaly_detect(record):
    if record['fncnt'] > 0:
        #          print record['si']['crtime'].dt, record['fn', 0]['crtime'].dt

        # Check for STD create times that are before the FN create times
        try:
            if record['si']['crtime'].dt < record['fn', 0]['crtime'].dt:
                record['stf-fn-shift'] = True
        except:
            pass

        # Check for STD create times with a nanosecond value of '0'     
        try:
            if record['si']['crtime'].dt != 0:
                if record['si']['crtime'].dt.microsecond == 0:
                    record['usec-zero'] = True
        except:
            pass

        # Check for STD create times that are after the STD modify times.  This is often the result of a file copy.
        try:
            if record['si']['crtime'].dt > record['si']['mtime'].dt:
                record['possible-copy'] = True
        except:
            pass

        # Check for STD access times that are after the STD modify and STD create times.  For systems with last access 
        # timestamp disabled (Windows Vista+), this is an indication of a file moved from one volume to another.
        try:
            if record['si']['atime'].dt > record['si']['mtime'].dt and record['si']['atime'].dt > record['si']['crtime'].dt:
                record['possible-volmove'] = True
        except:
            pass
