#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import vcfpy
from pathlib import Path
import re
from pprint import pprint

class VariantCaller:
    def __init__(self, string=None):
        """
        Class to store VariantCaller attributes from a given string
        :param str
        """
        self._string = None
        self._mapping = {}
        self._name = None
        self._version = None

        if string:
            self._string = string
            self._parse_string()

    def _parse_string(self):
        """
        Runs _parse_freebayes_string() if a given string begins with 'freeBayes'
        :param str
        """
        if self._string.startswith('freeBayes'):
            self._parse_freebayes_string()

    def _parse_freebayes_string(self):
        """
        Parses the name and version of a VariantCaller
        :param str
        """
        variant_caller_re = re.compile("(?P<name>^[\w]+)\s(?P<version>.+$)")
        self._mapping = variant_caller_re.search(self._string).groupdict()
        self._name = self._mapping['name']
        self._version = self._mapping['version']

    @property
    def mapping(self):
        """
        Returns string with a variant caller name and _version
        :return: str "(?P<name>^[\w]+)\s(?P<version>.+$)"
        """
        return self._mapping

    @mapping.setter
    def mapping(self, value):
        """
        Sets an string with the name and version of the variantcaller
        :param value: str
        """
        if type(value) == dict:
            if 'name' in value.keys() and 'version' in value.keys():
                if type(value['name']) == str and type(value['version']) == str:
                    self._mapping = value
                    self._name = value['name']
                    self._version = value['version']

    @property
    def name(self):
        """
        Returns string with a variantcaller name
        :return: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set an string with the name of the variantcaller
        :param value: str
        """
        if type(value) == str:
            self._name = value

    @property
    def version(self):
        """
        Return a string with the variantcaller version
        :return: str
        """
        return self._version

    @version.setter
    def version(self, value):
        """
        Sets an string with the version of the variantcaller
        :param value: str
        """
        if type(value) == str:
            self._version = value

class Contig:
    def __init__(self, contig_header_line=None):
        """
        Class to store metadata information from the contig field of the header of a VCF formatted file.
        :param contig_header_line: vcfpy.header.ContigHeaderLine
        """

        self._contig_header_line = None
        self._mapping = None
        self._id = None
        self._length = None
        self._cytobands = None #[TODO] Implement in future iterations

        if contig_header_line:
            self._contig_header_line = contig_header_line
            self._get_mapping_from_contig_header_line()
            self._id = self._mapping['id']
            self._length = self._mapping['length']

    def _get_mapping_from_contig_header_line(self):
        """
        Parses the id and length attributes of contig field from a VCF file
        :param contig_header_line: vcfpy.header.ContigHeaderLine
        """
        if type(self._contig_header_line) == vcfpy.header.ContigHeaderLine:
            self._mapping = {
                'id': self._contig_header_line.mapping['ID'],
                'length': self._contig_header_line.mapping['length'],
            }

    @property
    def mapping(self):
        """
        Returns a Dict object with contigs' id and length.
        :return: Dict with the following format:
            {
                'id': str,
                'length': int,
            }
        """
        return self._mapping

    @mapping.setter
    def mapping(self, value):
        """
        Sets a Dict object with key value id and length for the contig field.
        :param value: Dict with the following format:
            {
                'id': str,
                'length': int,
            }
        """
        if type(value) == dict:
            if 'id' in value.keys() and 'length' in value.keys():
                if type(value['id']) == str and type(value['length']) == int:
                    self._mapping = value
                    self._id = value['id']
                    self._length = value['length']

    @property
    def id(self):
        """
        Return a string with the id value of contigs field
        :return: str
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        Sets an string with id value for the contig field
        :param value: str
        """
        if type(value) == str:
            self._id = value

    @property
    def length(self):
        """
        Return a integer with the _length of the contig field
        :return: int
        """
        return self._length

    @length.setter
    def length(self, value):
        """
        Sets an integer with the length of the contig field
        :param value: str
        """
        if type(value) == int:
            self._length = value

class RecordField:
    def __init__(self, record_field_line=None):
        """
        Class to storedata  parsed from VCF file INFO and FORMAT fields
        :param value: dispatcher[field_type]['field_info_parser'](key=id)
        """
        self._record_field_line = None
        self._mapping = {}
        self._field_type = None
        self._id = None
        self._number = None
        self._type = None
        self._description = None

        if record_field_line:
            self._record_field_line = record_field_line
            self._get_mapping_from_record_field_line()
            self._field_type = self._mapping['field_type']
            self._id = self._mapping['id']
            self._number = self._mapping['number']
            self._type = self._mapping['type']
            self._description = self._mapping['description']


    def _get_mapping_from_record_field_line(self):
        """
        Parses the attributes for INFO and FORMAT fields
        :return: Dict with field attributes
        """
        if type(self._record_field_line) == vcfpy.header.InfoHeaderLine:
            self._mapping['field_type'] = 'INFO'

        elif type(self._record_field_line) == vcfpy.header.FormatHeaderLine:
            self._mapping['field_type'] = 'FORMAT'

        self._mapping['id'] = self._record_field_line.mapping['ID']
        self._mapping['number'] = str(self._record_field_line.mapping['Number'])
        self._mapping['type'] = self._record_field_line.mapping['Type']
        self._mapping['description'] = self._record_field_line.mapping['Description']

    @property
    def mapping(self):
        """
        Returns a Dict with attributes for INFO and FORMAT fields
        :return: Dict with field attributes
        """
        return self._mapping

    @mapping.setter
    def mapping(self, value):
        """
        Sets attributes for INFO and FORMAT fields
        :param value: Dict with the following format:
            {
                'field_type': str,
                'id': str,
                'number': int,
                'type': str,
                'description': str,
            }
        """
        wanted_keys = ['field_type','id','number','type','description']
        if type(value) == dict:
            if len(set(value.keys()) - set(wanted_keys)) == 0:
                dtypes = [type(x) for x in value.values()]
                if len(set(dtypes)) == 0 and str in dtypes:
                    self._mapping = value
                    self._field_type = value['field_type']
                    self._id = value['id']
                    self._number = value['number']
                    self._type = value['type']
                    self._description = value['description']

class Sample:
    def __init__(self, id):
        """
        Class to store identification value for each sample of a VCF file
        :param id: self._header.samples.names
        """

        self._id = None

        if type(id) == str:
            self._id = id
        else:
            raise TypeError("Attribute 'id' must be 'str'")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if type(value) == str:
            self._id = value
        else:
            raise TypeError("Attribute 'id' must be 'str'")

class VcfHeader:
    def __init__(self, filepath=None):
        """
        Class to store metadata information from the header of a VCF formatted file
        :param filepath: path/to/file.vcf(.gz)
        """
        # Initialize all properties to None
        self._vcf_filepath = None
        self._header = None
        self._file_format = None
        self._file_date = None
        self._variant_caller = None
        self._command_line = None #[TODO] Implement in future iterations
        self._reference = None
        self._contigs = []
        self._record_fields = []
        self._samples = []

        # Populate VcfHeader object from VCF filepath
        if filepath:
            self._vcf_filepath = filepath
            self._load_header_from_vcf_filepath(self._vcf_filepath)
            self._populate_object()

    # Private methods
    def _load_header_from_vcf_filepath(self, filepath: str) -> vcfpy.header.Header:
        """
        Loads the header content from a VCF filepath in a vcfpy.header.Header class
        :param filepath: path/to/file.vcf
        """
        self._header = vcfpy.Reader.from_path(filepath).header

    def _populate_object(self):
        """
        Parses the metadata from a VCF file and populates VcfHeader object
        :return: self._file_format = str
                 self._file_date = str
                 self._variant_caller = VaraiantCaller
                 self._command_line = [TODO]
                 self._reference = str
                 self._contigs = list
                 self._record_fields = list
                 self._samples = list
        """
        self._get_file_format_from_header()
        self._get_file_date_from_header()
        self._get_variant_caller_from_header()
        self._get_reference_from_header()
        self._get_contigs_from_header()
        self._get_record_fields_from_header()
        self._get_samples_from_header()

    def _get_header_line_value_from_key(self, header_line_type: type, line_key: str):
        """
        Checks the header_line_type
        :param value: type
        :param value: str
        """
        for line in self._header.lines:
            if type(line) == header_line_type and line.key == line_key:
                return line.value

    def _get_file_format_from_header(self) -> str:
        """
        Loads the file format value from the Header of a VCF file
        :return: str
        """
        self._file_format = self._get_header_line_value_from_key(
            header_line_type = vcfpy.header.HeaderLine,
            line_key='fileformat',
        )

    def _get_file_date_from_header(self) -> str:
        """
        Loads the file date value from the Header of a VCF file
        :return: str
        """
        self._file_date = self._get_header_line_value_from_key(
            header_line_type = vcfpy.header.HeaderLine,
            line_key='fileDate',
        )

    def _get_variant_caller_from_header(self) -> VariantCaller:
        """
        Loads the variantcaller data from the Header of a VCF file
        :return: VariantCaller
        """
        variant_caller_string = self._get_header_line_value_from_key(
            header_line_type = vcfpy.header.HeaderLine,
            line_key='source',
        )

        self._variant_caller = VariantCaller(string=variant_caller_string)

    def _get_reference_from_header(self) -> str:
        """
        Loads the reference genome value from the Header of a VCF file
        :return: str
        """
        self._reference = self._get_header_line_value_from_key(
            header_line_type = vcfpy.header.HeaderLine,
            line_key='reference',
        )

    def _get_contigs_from_header(self) -> list:
        """
        Loads the contig field values from the Header of a VCF file
        :return: list of Contig objects
        """
        self._contigs = []
        for line in self._header.lines:
            if type(line) == vcfpy.header.ContigHeaderLine:
                self._contigs.append(Contig(contig_header_line=line))

    def _get_record_fields_from_header(self) -> list:
        """
        Loads the INFO and FORMAT field values from the Header of a VCF file
        :return: list of RecordField objects
        """
        self._record_fields = []

        dispatcher = {
            'INFO':{
                'id_parser': self._header.info_ids,
                'field_info_parser': self._header.get_info_field_info
            },
            'FORMAT':{
                'id_parser': self._header.format_ids,
                'field_info_parser': self._header.get_format_field_info
            }
        }

        for field_type in dispatcher.keys():
            ids = dispatcher[field_type]['id_parser']()
            for id in ids:
                record_field_line = dispatcher[field_type]['field_info_parser'](key=id)
                self._record_fields.append(RecordField(record_field_line=record_field_line))

    def _get_samples_from_header(self):
        """
        Loads samples id from the Header of a VCF file
        :return: list
        """

        self._samples = [Sample(id=id) for id in self._header.samples.names]

    @property
    def file_format(self):
        """
        Returns a string with VCF file format
        :return: str
        """
        return self._file_format

    @file_format.setter
    def file_format(self, value):
        """
        Sets file format attribute for VCFHeader objects
        :param value: str
        """
        if type(value) == str:
            self._file_format = value

    @property
    def file_date(self):
        """
        Returns a string with VCF file date
        :return: str
        """
        return self._file_date

    @file_date.setter
    def file_date(self, value):
        """
        Sets file date attribute for VCFHeader objects
        :param value: str
        """
        if type(value) == str:
            self._file_date = value

    @property
    def variant_caller(self):
        """
        Returns a VarianCaller object (see VariantCaller class)
        :return: VariantCaller
        """
        return self._variant_caller

    @variant_caller.setter
    def variant_caller(self, value):
        """
        Sets a VariantCaller object from a dict with required keys and values.
        :param value: Dict with the following format:
            {
                "name": str,
                "version": str,
            }
        """
        if type(value) == dict:
            self._variant_caller = VariantCaller()
            self._variant_caller.mapping = value

    @property
    def reference(self):
        """
        Returns a string with the reference genome value from a VCF file
        :return: str
        """
        return self._reference

    @reference.setter
    def reference(self, value):
        """
        Sets reference genome value
        :param value: str
        """
        if type(value) == str:
            self._reference = value

    @property
    def contigs(self):
        """
        Returns a list of Contig objects (see Contig class)
        :return: list
        """
        return self._contigs

    @contigs.setter
    def contigs(self, value):
        """
        Sets a lists of Contig objects
        :param value: list
        """
        if type(value) == list and len(value) != 0:
            self._contigs = []
            for item in value:
                if type(item) == Contig:
                    self._contigs.append(item)
                else:
                    pass #[TODO] raise error in future

        if type(value) == list and len(value) == 0:
            self._contigs = []

        else:
            pass #[TODO] raise error in future

    @property
    def record_fields(self):
        """
        Returns a list of RecordField objects (see RecordField class)
        :return: list
        """
        return self._record_fields

    @record_fields.setter
    def record_fields(self, value):
        """
        Sets a lists of Recordfield objects
        :param value: list
        """
        if type(value) == list and len(value) != 0:
            self._record_fields = []
            for item in value:
                if type(item) == RecordField:
                    self._record_fields.append(item)
                else:
                    pass #[TODO] raise error in future

        if type(value) == list and len(value) == 0:
            self._record_fields = []

        else:
            pass #[TODO] raise error in future

    @property
    def samples(self):
        """
        Returns a list of Sample objects with sample names
        :return: list
        """
        return self._samples

    @samples.setter
    def samples(self, value):
        """
        Sets a list of Sampple objects with sample names
        :param value: list
        """
        if type(value) == list and len(value) != 0:
            self._samples = []
            for item in value:
                if type(item) == Sample:
                    self._samples.append(item)
                else:
                    pass #[TODO] raise error in future

        if type(value) == list and len(value) == 0:
            self._samples = []

        else:
            pass #[TODO] raise error in future


def main():
    vcf_filepath = "/home/dgp/Documents/MGvizPro_projects/msm_tfm/test_data/20200908_GISTomics_chr22_variants.decomp.norm.filter.vcf.gz"
    vcf_header = VcfHeader(filepath=vcf_filepath)
    # print(vcf_header.file_format)
    # print(vcf_header.file_date)
    # print(vcf_header.variant_caller)
    # print(vcf_header.variant_caller.mapping)
    # print(vcf_header.variant_caller.name)
    # print(vcf_header.variant_caller.version)
    # vcf_header.variant_caller = {'name':'pepito', 'version':'foo'}
    # print(vcf_header.variant_caller.mapping)
    # print(vcf_header.reference)
    # print(len(vcf_header.contigs))
    # print(vcf_header.contigs[:10])
    # print([x.mapping for x in vcf_header.contigs[:10]])
    # print([x.id for x in vcf_header.contigs[:10]])
    # print([x.length for x in vcf_header.contigs[:10]])
    # print(vcf_header.record_fields[:10])
    # print([x.mapping for x in vcf_header.record_fields[:10]])
    print([x.id for x in vcf_header.samples])

if __name__ == '__main__':
    main()
