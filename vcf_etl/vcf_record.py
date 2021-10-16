#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import vcfpy
from pathlib import Path
import re
from pprint import pprint
from collections import OrderedDict

class RecordCall:
    def __init__(self, call=None):
        """
        """
        # Initialize all properties to None
        self._call = None
        self._sample = None
        self._data = OrderedDict()

        if call:
            self._call = call
            self._get_call_sample()
            self._get_call_data()

    #For each call
    def _get_call_sample(self):
        """
        """
        self._sample = self._call.sample

    def _get_call_data(self):
        """
        """
        self._data = OrderedDict(self._call.data)

    #Getters and setters
    @property
    def sample(self):
        """
        """
        return self._sample

    @sample.setter
    def sample(self, value):
        """
        """
        if type(value) == str:
            self._sample = value

    @property
    def data(self):
        """
        """
        return self._data

    @data.setter
    def data(self, dictionary):
        """
        Enhance
        """
        if type(dictionary) == OrderedDict:
            self._data = dictionary

class RecordInfo:
    def __init__(self, record=None):
        """
        """
        # Initialize all properties to None
        self._record = None
        self._data = OrderedDict()
        if record:
            self._record = record
            self._get_record_info_data()

    #Private methods
    def _get_record_info_data(self):
        self._data = OrderedDict(self._record.INFO)

    #Getters and setters
    @property
    def data(self):
        """
        """
        return self._data

    @data.setter
    def data(self, dictionary):
        """
        Enhance
        """
        if type(dictionary) == OrderedDict:
            self._data = dictionary

class VcfRecord:
    def __init__(self, record=None):
        """
        """
        # Initialize all properties to None
        self._record = None
        self._id = None
        self._chrom = None
        self._pos = None
        self._start = None
        self._end = None
        self._ref = None
        self._alt = None
        self._type = None
        self._info = []
        self._calls = []

        if record:
            self._record = record
            self._populate_object()

    # Private methods
    def _populate_object(self):
        """
        """
        self._get_record_id()
        self._get_record_chrom()
        self._get_record_pos()
        self._get_record_start()
        self._get_record_end()
        self._get_record_ref()
        self._get_record_alt()
        self._get_record_type()
        self._get_record_info()
        self._get_record_calls()

    # For each record
    def _get_record_id(self) -> str:
        """
        <PENDING>
        """
        self._id = self._record.CHROM+':'+str(self._record.affected_start)+'-'+str(self._record.affected_end)+'|'+self._record.REF+'|'+self._record.ALT[0].value

    def _get_record_chrom(self) -> str:
        """
        <PENDING>
        """
        self._chrom = self._record.CHROM

    def _get_record_pos(self) -> int:
        """
        <PENDING>
        """
        self._pos = self._record.POS

    def _get_record_start(self) -> int:
        """
        <PENDING>
        """
        self._start = self._record.affected_start

    def _get_record_end(self) -> int:
        """
        <PENDING>
        """
        self._end = self._record.affected_end

    def _get_record_ref(self) -> str:
        """
        <PENDING>
        """
        self._ref = self._record.REF

    def _get_record_alt(self) -> str:
        """
        <PENDING>
        """
        self._alt = self._record.ALT[0].value

    def _get_record_type(self) -> str:
        """
        <PENDING>
        """
        self._type = self._record.ALT[0].type


    def _get_record_info(self) -> dict:
        """
        <PENDING>
        """
        self._info = RecordInfo(self._record)

    def _get_record_calls(self) -> list:
        """
        <PENDING>
        """
        self._calls = []

        for call in self._record.calls:
            self._calls.append(RecordCall(call))

    #Getters and setters
    @property
    def id(self):
        """
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        """
        if type(value) == str:
            self._id = value

    @property
    def chrom(self):
        """
        """
        return self._chrom

    @chrom.setter
    def chrom(self, value):
        """
        """
        if type(value) == str:
            self._chrom = value

    @property
    def pos(self):
        """
        """
        return self._pos

    @pos.setter
    def pos(self, value):
        """
        """
        if type(value) == int:
            self._pos = value

    @property
    def start(self):
        """
        """
        return self._start

    @start.setter
    def start(self, value):
        """
        """
        if type(value) == int:
            self._start = value

    @property
    def end(self):
        """
        """
        return self._end

    @end.setter
    def end(self, value):
        """
        """
        if type(value) == int:
            self._end = value

    @property
    def ref(self):
        """
        """
        return self._ref

    @ref.setter
    def ref(self, value):
        """
        """
        if type(value) == str:
            self._ref = value

    @property
    def alt(self):
        """
        """
        return self._alt

    @alt.setter
    def alt(self, value):
        """
        """
        if type(value) == str:
            self._alt = value

    @property
    def type(self):
        """
        """
        return self._type

    @type.setter
    def type(self, value):
        """
        """
        if type(value) == str:
            self._type = value

    @property
    def info(self):
        """
        """
        return self._info

    @info.setter
    def info(self, dictionary):
        """
        """
        if type(dictionary) == OrderedDict:
            self._info = dictionary

    @property
    def calls(self):
        """
        """
        return self._calls

    @calls.setter
    def calls(self, vector):
        """
        """
        if type(vector) == list:
            self._calls = vector

def main():
    vcf_filepath = "/Users/segarmond/Documents/Science/Bioinfo/TFM/old_msm_tfm/msm_tfm-main/test_data/20200908_GISTomics_chr22_variants.decomp.norm.filter.vcf.gz"
    print(vcf_filepath)
    reader = vcfpy.Reader.from_path(vcf_filepath)
    vcf_test = []
    for record in reader:
        vcf_test.append(VcfRecord(record))
        break
    pprint(vcf_test[0].info.data)

if __name__ == '__main__':
    main()
