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
        Class to store sample and data attributes from a given call
        :param value: vcfpy.record.Call
        """
        # Initialize all properties to None
        self._call = None
        self._sample = None
        self._data = OrderedDict()

        if call:
            self._call = call
            self._get_call_sample()
            self._get_call_data()

    def _get_call_sample(self):
        """
        Loads the sample atribute from vcfpy.Call objects
        :param value: vcfpy.record.Call
        """
        self._sample = self._call.sample

    def _get_call_data(self):
        """
        Loads as OrderedDict the data atribute from vcfpy.Call objects
        :param value: vcfpy.record.Call
        """
        self._data = OrderedDict(self._call.data)

    #Getters and setters
    @property
    def sample(self):
        """
        Returns a string with sample atribute for vcfpy.record.Call
        :return: str
        """
        return self._sample

    @sample.setter
    def sample(self, value):
        """
        Sets sample atribute for RecordCall object
        :param value: str
        """
        if type(value) == str:
            self._sample = value

    @property
    def data(self):
        """
        Returns an OrderedDict with data attribute from vcf.Call
        :return: OrderedDict
        """
        return self._data

    @data.setter
    def data(self, value):
        """
        Sets data attribute from OrderedDict for RecordCall object
        :param value: OrderedDict
        """
        if type(value) == OrderedDict:
            self._data = value

class RecordInfo:
    def __init__(self, data=None):
        """
        Class to store Info field data from a given record
        :param data: dict
        """
        self._data = data

    # Getters and setters
    @property
    def data(self):
        """
        Returns a RecordInfo object from a given vcfpy.record
        :return: dict
        """
        return self._data

    @data.setter
    def data(self, value):
        """
        Sets data attribute from OrderedDict for RecordCall object
        :param value: dict
        """
        if type(value) == dict:
            self._data = value

class RecordAnnotation:
    def __init__(self, data=None):
        """
        Class to store Info varian annotation data from a given record
        :param data: dict
        """
        self._data = data

    # Getters and setters
    @property
    def data(self):
        """
        Returns a dict with RecordAnnotation data
        :return: dict
        """
        return self._data

    @data.setter
    def data(self, value):
        """
        Sets data attribute from a dict
        :param value: dict
        """
        if type(value) == dict:
            self._data = value

class VcfRecord:
    def __init__(self, record=None, annotation_field=None, annotation_keys=None, annotation_list_sep=None, annotation_sep=None):
        """
        Class to store data from a given record of a VCF formatted file
        :param filepath: vcfpy.record
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
        self._annotation_field = None
        self._annotation_keys = None
        self._annotation_list_sep = None
        self._annotation_sep = None
        self._annotations = []


        if record:
            self._record = record
            self._populate_record()

        if annotation_field and annotation_keys and annotation_list_sep and annotation_sep:
            self._populate_annotations()

    # Private methods
    def _populate_record(self):
        """
        Parses the data from a given record of a VCF formatted file (wihtout including variant annotation)
        :return:self._get_record_id = str
                self._get_record_chrom = str
                self._get_record_pos = int
                self._get_record_start = int
                self._get_record_end = int
                self._get_record_ref = str
                self._get_record_alt = str
                self._get_record_type = str
                self._get_record_info = RecordInfo
                self._get_record_calls = list
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

    def _get_record_id(self) -> str:
        """
        Generates and loads the id value for a given record of a VCF file
        :return: str
        """
        self._id = self._record.CHROM+':'+str(self._record.affected_start)+'-'+str(self._record.affected_end)+'|'+self._record.REF+'|'+self._record.ALT[0].value

    def _get_record_chrom(self) -> str:
        """
        Loads the chromosome field from a given record of a VCF file
        :return: str
        """
        self._chrom = self._record.CHROM

    def _get_record_pos(self) -> int:
        """
        Loads the position field from a given record of a VCF file
        :return: int
        """
        self._pos = self._record.POS

    def _get_record_start(self) -> int:
        """
        Loads the start position field from a given record of a VCF file
        :return: int
        """
        self._start = self._record.affected_start

    def _get_record_end(self) -> int:
        """
        Loads the end position field from a given record of a VCF file
        :return: int
        """
        self._end = self._record.affected_end

    def _get_record_ref(self) -> str:
        """
        Loads the reference value field from a given record of a VCF file
        :return: str
        """
        self._ref = self._record.REF

    def _get_record_alt(self) -> str:
        """
        Loads the alternative value field from a given record of a VCF file
        :return: str
        """
        self._alt = self._record.ALT[0].value

    def _get_record_type(self) -> str:
        """
        Loads the variance type field from a given record of a VCF file
        :return: str
        """
        self._type = self._record.ALT[0].type

    def _get_record_info(self) -> dict:
        """
        Loads the info field from a given record of a VCF file
        :return: RecordInfo
        """
        data = self._record.INFO
        # Remove annotation field from info data
        if self._annotation_field:
            data.pop(self._annotation_field, None)
        self._info = RecordInfo(data=data)

    def _get_record_calls(self) -> list:
        """
        Loads the calls from a given record of a VCF file
        :return: list of RecordCall objects
        """
        self._calls = []

        for call in self._record.calls:
            self._calls.append(RecordCall(call=call))

    def _populate_record_annotations(self):
        """
        Parses the variant annotation data from the INFO field of a record from a VCF file
        """

        # Get annotation field content from vcfpy.Record.INFO
        annotations_str = self._record.INFO[self._annotation_field]
        # Split mutiple annotations for a record by a separator
        for annotation_str in annotations_str.split(self._annotation_list_sep):
            # Split annotation values by a separator
            annotation_values = annotation_str.split(self._annotation_sep)
            # Create a dictionary of annotations
            annotation_data = dict(zip(self._annotation_keys, annotation_values))
            # Append RecordAnnotation objects
            self._annotations.append(RecordAnnotation(annotation=annotation_data))

    #Getters and setters
    @property
    def id(self):
        """
        Returns a string with a record id
        :return: str
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        Sets record id value of a given record
        :param value: str
        """
        if type(value) == str:
            self._id = value

    @property
    def chrom(self):
        """
        Returns a string with a record chromosome value
        :return: str
        """
        return self._chrom

    @chrom.setter
    def chrom(self, value):
        """
        Sets record chromosome value of a given record
        :param value: str
        """
        if type(value) == str:
            self._chrom = value

    @property
    def pos(self):
        """
        Returns a integer with a record position
        :return: int
        """
        return self._pos

    @pos.setter
    def pos(self, value):
        """
        Sets record position value of a given record
        :param value: int
        """
        if type(value) == int:
            self._pos = value

    @property
    def start(self):
        """
        Returns a integer with a record starting position
        :return: int
        """
        return self._start

    @start.setter
    def start(self, value):
        """
        Sets record starting position value of a given record
        :param value: int
        """
        if type(value) == int:
            self._start = value

    @property
    def end(self):
        """
        Returns a integer with a record ending position
        :return: int
        """
        return self._end

    @end.setter
    def end(self, value):
        """
        Sets record ending position value of a given record
        :param value: int
        """
        if type(value) == int:
            self._end = value

    @property
    def ref(self):
        """
        Returns a string with a record reference value
        :return: str
        """
        return self._ref

    @ref.setter
    def ref(self, value):
        """
        Sets record reference value of a given record
        :param value: str
        """
        if type(value) == str:
            self._ref = value

    @property
    def alt(self):
        """
        Returns a string with a record alternative value
        :return: str
        """
        return self._alt

    @alt.setter
    def alt(self, value):
        """
        Sets record alternative value of a given record
        :param value: str
        """
        if type(value) == str:
            self._alt = value

    @property
    def type(self):
        """
        Returns a string with a record variance type
        :return: str
        """
        return self._type

    @type.setter
    def type(self, value):
        """
        Sets record variance type of a given record
        :param value: str
        """
        if type(value) == str:
            self._type = value

    @property
    def info(self):
        """
        Returns a dictionary with a record info field
        :return: RecordInfo
        """
        return self._info

    @info.setter
    def info(self, value):
        """
        Sets record info field of a given record
        :param value: RecordInfo
        """
        if type(value) == RecordInfo:
            self._info = value

    @property
    def calls(self):
        """
        Returns a list of RecordCall objects with call info from a record
        :return: list
        """
        return self._calls

    @calls.setter
    def calls(self, value):
        """
        Sets a list of RecordCall objects of a given record
        :param value: list
        """
        if type(value) == list:
            test_calls = []
            for item in value:
                test_calls.append(type(item)==RecordCall)
            if all(test_calls):
                self._calls = value

    @property
    def annotations(self):
        """
        Returns a list of RecordAnnotation objects with vcfpy.Record.INFO annotation field from a record
        :return: list
        """
        return self._annotations

    @annotations.setter
    def annotations(self):
        """
        Sets a list of RecordAnnotation objects of a given record
        :param value: list
        """
        if type(value) == list:
            test_annotations = []
            for item in value:
                test_annotations.append(type(item)==RecordAnnotation)
            if all(test_annotation):
                self._annotations = value

def main():
    vcf_filepath = "/Users/segarmond/Documents/Science/Bioinfo/TFM/old_msm_tfm/msm_tfm-main/test_data/20200908_GISTomics_chr22_variants.decomp.norm.filter.vcf.gz"
    print(vcf_filepath)
    reader = vcfpy.Reader.from_path(vcf_filepath)
    vcf_test = []
    for record in reader:
        vcf_test.append(VcfRecord(record))
        break
    pprint(type(vcf_test[0].calls[0]))

if __name__ == '__main__':
    main()
