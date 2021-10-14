#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import vcfpy
from pathlib import Path
import re
from pprint import pprint


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
        self._INFO = []
        self._calls = []

        if record:
            self._record = record
            self._populate_object()
    # Private methods



    def _populate_object(self):
        """
        """
        self._get_record_id()
        self._get_record_chromosome()
        self._get_record_position()
        self._get_record_start()
        self._get_record_end()
        self._get_record_reference()
        self._get_record_alternative()
        self._get_record_type()
        self._get_record_INFO()
        self._get_record_calls()
#
#     # For each record
    def _get_record_id(self) -> str:
        """
        <PENDING>
        """
        self._id = self._record.CHROM+':'+str(self._record.affected_start)+'-'+str(self._record.affected_end)+'|'+self._record.REF+'|'+self._record.ALT[0].value

    def _get_record_chromosome(self) -> str:
        """
        <PENDING>
        """
        self._chrom = self._record.CHROM

    def _get_record_position(self) -> int:
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

    def _get_record_reference(self) -> str:
        """
        <PENDING>
        """
        self._ref = self._record.REF

    def _get_record_alternative(self) -> str:
        """
        <PENDING>
        """
        self._alt = self._record.ALT[0].value

    def _get_record_type(self) -> str:
        """
        <PENDING>
        """
        self._type = self._record.ALT[0].type


    def _get_record_INFO(self) -> dict:
        """
        <PENDING>
        """
        self._INFO = self._record.INFO

    def _get_record_calls(self) -> list:
        """
        <PENDING>
        """
        self._calls = []

        for call in self._record.calls:
            self._calls.append({
                'sample': call.sample,
                'data': call.data
                })



# #Getters and setters

    @property
    def record(self):
        """
        """
        return self._record

    @record.setter
    def record(self, value):
        """
        """
        if type(value) == vcfpy.record.Record:
            self._record = value

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
    def chromosome(self):
        """
        """
        return self._chrom

    @chromosome.setter
    def chromosome(self, value):
        """
        """
        if type(value) == str:
            self._chrom = value

    @property
    def position(self):
        """
        """
        return self._pos

    @position.setter
    def position(self, value):
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
    def reference(self):
        """
        """
        return self._ref

    @reference.setter
    def reference(self, value):
        """
        """
        if type(value) == str:
            self._ref = value

    @property
    def alternative(self):
        """
        """
        return self._alt

    @alternative.setter
    def alternative(self, value):
        """
        """
        if type(value) == str:
            self._alt = value

    @property
    def var_type(self):
        """
        """
        return self._type

    @var_type.setter
    def var_type(self, value):
        """
        """
        if type(value) == str:
            self._type = value

    @property
    def INFO(self):
        """
        """
        return self._INFO

    @INFO.setter
    def INFO(self, dictionary):
        """
        """
        if type(dictionary) == dict:
            self._INFO = dictionary


    @property
    def var_calls(self):
        """
        """
        return self._calls

    @var_calls.setter
    def var_calls(self, vector):
        """
        """
        if type(vector) == list:
            self._calls = vector



def main():
    vcf_filepath = "/Users/segarmond/Documents/Science/Bioinfo/TFM/old_msm_tfm/msm_tfm-main/test_data/20200908_GISTomics_chr22_variants.decomp.norm.filter.vcf.gz"
    print(vcf_filepath)
    print("Hello Marc")
    reader = vcfpy.Reader.from_path(vcf_filepath)
    vcf_test = []
    for record in reader:
        vcf_test.append(VcfRecord(record))
        break

    print(vcf_test[0].var_calls)


if __name__ == '__main__':
    main()
