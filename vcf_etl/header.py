#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import vcfpy
import re
from pathlib import Path

class VariantCaller:
    def __init__(self, string=None, name=None, version=None):
        """
        Class to store the information of the variant caller used to generate a VCF
        :param string: A string with name and version information from a VCF header
        :param name: Name of the variant caller used to generate a VCF file
        :param version: Version of the variant aller used to generate a VCF file
        """
        self._string = None
        self._name = None
        self._version = None

        if string:
            self._string = string
            self._parse_string()

        elif name:
            self._name = name

        elif version:
            self._version = version

    def _parse_string(self):
        """
        Parse the information string of the variant caller used using specific methods
        for each supported variant caller
        """
        if self._string.startswith('freeBayes'):
            self._parse_freebayes_string()

    def _parse_freebayes_string(self):
        """
        Parse the name and version of freebayes from the header line of a VCF file
        """
        variant_caller_re = re.compile("(?P<name>^[\w]+)\s(?P<version>.+$)")
        search_groupdict = variant_caller_re.search(self._string).groupdict()
        self._name = search_groupdict['name']
        self._version = search_groupdict['version']

    def to_dict(self) -> dict:
        """
        Returns a dict with all the properties of the class
        """
        data = {
            'name': self._name,
            'version':self._version,
        }
        return data

    @property
    def name(self) -> str:
        """
        Return the name of a variant caller
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Set the name of a variant caller
        :param value: str
        """
        if type(value) == str:
            self._name = value

    @property
    def version(self) -> str:
        """
        Return the version of a variant caller
        """
        return self._version

    @version.setter
    def version(self, value: str):
        """
        Set the version of a variant caller
        """
        if type(value) == str:
            self._version = value

class Contig:
    def __init__(self, contig_header_line=None):
        """
        Class to store VCF header contig information of the reference genome used to generate a VCF file.
        :param contig_header_line: vcfpy.header.ContigHeaderLine
        """

        self._contig_header_line = None
        self._id = None
        self._length = None
        self._cytobands = None #[TODO] Implement in future iterations

        if contig_header_line:
            self._contig_header_line = contig_header_line
            self._get_id_from_vcfpy_contig_header_line()
            self._get_length_from_vcfpy_contig_header_line()

    def _get_id_from_vcfpy_contig_header_line(self):
        """
        Parses the contig id from a vcfpy.header.ContigHeaderLine
        """
        if type(self._contig_header_line) == vcfpy.header.ContigHeaderLine:
            self._id = self._contig_header_line.mapping['ID']

    def _get_length_from_vcfpy_contig_header_line(self):
        """
        Parses the contig id from a vcfpy.header.ContigHeaderLine
        """
        if type(self._contig_header_line) == vcfpy.header.ContigHeaderLine:
            self._length = int(self._contig_header_line.mapping['length'])

    def to_dict(self) -> dict:
        """
        Returns a dict with all the properties of the class
        """
        data = {
            'id': self._id,
            'length':self._length,
        }
        return data

    @property
    def id(self) -> str:
        """
        Return the contig id
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        Set the contig id
        :param value: str
        """
        if type(value) == str:
            self._id = value

    @property
    def length(self) -> int:
        """
        Return the contig length
        """
        return self._length

    @length.setter
    def length(self, value):
        """
        Set the contig length
        :param value: int
        """
        if type(value) == int:
            self._length = value

class RecordField:
    def __init__(self, record_field_line=None):
        """
        Class to store the VCF header information of VCF INFO and FORMAT fields from vcfpy.header.InfoHeaderLine
        and vcfpy.header.FormatHeaderLine
        :param record_field_line: vcfpy.header.InfoHeaderLine or vcfpy.header.FormatHeaderLine
        """
        self._record_field_line = None
        self._field_type = None
        self._id = None
        self._number = None
        self._type = None
        self._description = None

        if record_field_line:
            self._record_field_line = record_field_line
            self._get_field_type_from_vcfpy_record_field_line()
            self._get_id_from_vcfpy_record_field_line()
            self._get_number_from_vcfpy_record_field_line()
            self._get_type_from_vcfpy_record_field_line()
            self._get_description_from_vcfpy_record_field_line()

    def _get_field_type_from_vcfpy_record_field_line(self):
        """
        Get record field type from vcfpy.header.InfoHeaderLine or vcfpy.header.FormatHeaderLine
        """
        if type(self._record_field_line) == vcfpy.header.InfoHeaderLine:
            self._field_type = 'INFO'

        elif type(self._record_field_line) == vcfpy.header.FormatHeaderLine:
            self._field_type = 'FORMAT'

        else:
            msg = "RecordField of type '{}', not supported".format(self._record_field_line)
            raise TypeError(msg)

    def _get_id_from_vcfpy_record_field_line(self):
        """
        Get record field id from vcfpy.header.InfoHeaderLine or vcfpy.header.FormatHeaderLine
        """
        self._id = self._record_field_line.mapping['ID']

    def _get_number_from_vcfpy_record_field_line(self):
        """
        Get record field number of values from vcfpy.header.InfoHeaderLine or vcfpy.header.FormatHeaderLine
        """
        self._number = str(self._record_field_line.mapping['Number'])

    def _get_type_from_vcfpy_record_field_line(self):
        """
        Get record field type (data type) from vcfpy.header.InfoHeaderLine or vcfpy.header.FormatHeaderLine
        """
        self._type = self._record_field_line.mapping['Type']

    def _get_description_from_vcfpy_record_field_line(self):
        """
        Get record field description from vcfpy.header.InfoHeaderLine or vcfpy.header.FormatHeaderLine
        """
        self._description = self._record_field_line.mapping['Description']

    def to_dict(self) -> dict:
        """
        Returns a dict with all the properties of the class
        """
        data = {
            'field_type': self._field_type,
            'id': self._id,
            'number': self._number,
            'type': self._type,
            'description': self._description,
        }
        return data

    @property
    def field_type(self) -> str:
        """
        Get field type of the record field: [None, 'INFO', 'FORMAT']
        """
        return self._field_type

    @field_type.setter
    def field_type(self, value):
        """
        Set field type of the record field [None, 'INFO', 'FORMAT']
        :param value: any of the following items: [None, 'INFO', 'FORMAT']
        """
        if value in [None, 'INFO', 'FORMAT']:
            self._field_type = value
        else:
            msg = "Value '{}' is not supported. Available values: [None, 'INFO', 'FORMAT']".format(value)
            raise ValueError(msg)

    @property
    def id(self) -> str:
        """
        Get the id of the record field
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        Set the id of the record field
        :param value: str
        """
        if type(value) == str: #[TODO] Raise error if condition not fulfilled
            self._id = value

    @property
    def number(self) -> str:
        """
        Get the number of values per record in the record field
        """
        return self._number

    @number.setter
    def number(self, value):
        """
        Set the number of values per record in the record field
        """
        if type(value) == str: #[TODO] Declare specific and constrained values. Raise error if condition not fulfilled
            self._number = value

    @property
    def type(self) -> str:
        """
        Get the data type of the record field
        """
        return self._type

    @type.setter
    def type(self, value):
        """
        Set the data type of the record field
        :param value: str
        """
        if type(value) == str: #[TODO] Declare specific and constrained values. Raise error if condition not fulfilled
            self._type = value

    @property
    def description(self) -> str:
        """
        Get the description of a record field
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        Set the description of a record field
        :param value: str
        """
        if type(value) == str:
            self._description = value

class Sample:
    def __init__(self, id=None):
        """
        Class to store sample data from a VCF
        :param id: str
        """

        self._id = None

        if id:
            if type(id) == str:
                self._id = id
            else:
                raise TypeError("Param 'id' must be 'str'")

    def to_dict(self) -> dict:
        """
        Returns a dict with all the properties of the class
        """
        data = {
            'id': self._id,
        }
        return data

    @property
    def id(self) -> str:
        """
        Get the id of a sample
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        Set the id of a sample
        :param value: str
        """
        if type(value) == str:
            self._id = value
        else:
            raise TypeError("Attribute 'id' only supports 'str' type values")

class VcfHeader:
    def __init__(self, filepath=None):
        """
        Stores the metadata from a VCF header. Can be initialized with a VCF filepath.
        :param filepath: path/to/file.vcf(.gz)
        """
        # Initialize an empty class with all the properties as private
        self._vcf_filepath = None # str
        self._vcfpy_header = None # vcfpy.header.Header
        self._file_format = None # str
        self._file_date = None # str
        self._variant_caller = None # VariantCaller
        self._command_line = None #[TODO] Implement in future iterations
        self._reference = None # str
        self._contigs = [] # [Contig,...]
        self._record_fields = [] # [RecordField,...]
        self._samples = [] # [Sample,...]

        # Populate properties from a VCF filepath
        if filepath:
            self._vcf_filepath = filepath
            self._load_header_from_vcf_filepath()
            self._populate_from_vcfpy_header()

    def _load_header_from_vcf_filepath(self):
        """
        Loads the VCF header as a vcfpy.header.Header object from a VCF filepath
        """
        self._vcfpy_header = vcfpy.Reader.from_path(self._vcf_filepath).header

    def _populate_from_vcfpy_header(self):
        """
        Populates the class properties from a vcfpy.header.Header object
        """
        # VCF file format: self._file_format (str)
        self._get_file_format_from_vcfpy_header()
        # VCF file date: self._file_date (str)
        self._get_file_date_from_vcfpy_header()
        # Variant caller to generate the VCF: self._variant_caller (VariantCaller)
        self._get_variant_caller_from_vcfpy_header()
        # Reference genome to generate the VCF: self._reference (str)
        self._get_reference_from_vcfpy_header()
        # Contigs used to generate the VCF from the reference genome: self._contigs ([Contig,...])
        self._get_contigs_from_vcfpy_header()
        # Record fields in VCF INFO and FORMAT: self._record_fields ([RecordField,...])
        self._get_record_fields_from_vcfpy_header()
        # Data from samples included in the VCF: self._samples ([Sample,...])
        self._get_samples_from_vcfpy_header()

    def _get_vcfpy_header_line_value_from_key(self, header_line_type: type, line_key: str):
        """
        Checks if a vcfpy.header.HeaderLine from vcfpy.header.Header has the wanted line key
        (line_key) and returns the value of the vcfpy.header.HeaderLine
        :param header_line_type: Type of vcfpy header line
        :param line_key: Key of vcfpy header line
        :return: The value of the vcfpy header line
        """
        for line in self._vcfpy_header.lines:
            if type(line) == header_line_type and line.key == line_key:
                return line.value

    def _get_file_format_from_vcfpy_header(self) -> str:
        """
        Get the file format value from vcfpy.header.Header
        """
        value = self._get_vcfpy_header_line_value_from_key(
            header_line_type = vcfpy.header.HeaderLine,
            line_key='fileformat',
        )
        self._file_format = str(value)

    def _get_file_date_from_vcfpy_header(self) -> str:
        """
        Get the file date value from vcfpy.header.Header
        """
        value = self._get_vcfpy_header_line_value_from_key(
            header_line_type = vcfpy.header.HeaderLine,
            line_key='fileDate',
        )
        self._file_date = str(value)

    def _get_variant_caller_from_vcfpy_header(self) -> VariantCaller:
        """
        Get the variant caller data from vcfpy.header.Header
        """
        value = self._get_vcfpy_header_line_value_from_key(
            header_line_type = vcfpy.header.HeaderLine,
            line_key='source',
        )
        self._variant_caller = VariantCaller(string=str(value))

    def _get_reference_from_vcfpy_header(self) -> str: #[TODO] Check if type == Path is neccessary
        """
        Get the reference genome filepath from vcfpy.header.Header
        """
        value = self._get_vcfpy_header_line_value_from_key(
            header_line_type = vcfpy.header.HeaderLine,
            line_key='reference',
        )
        self._reference = str(value)

    def _get_contigs_from_vcfpy_header(self) -> [Contig]:
        """
        Get the contig field values from vcfpy.header.Header
        """
        self._contigs = []
        for line in self._vcfpy_header.lines:
            if type(line) == vcfpy.header.ContigHeaderLine:
                contig = Contig(contig_header_line=line)
                self._contigs.append(contig)

    def _get_record_fields_from_vcfpy_header(self) -> [RecordField]:
        """
        Get the INFO and FORMAT field info from vcfpy.header.Header
        """
        self._record_fields = []

        # Dispatcher to get INFO and FORMAT record field ids and information
        dispatcher = {
            'INFO':{
                'ids': self._vcfpy_header.info_ids,
                'field_info_parser': self._vcfpy_header.get_info_field_info
            },
            'FORMAT':{
                'ids': self._vcfpy_header.format_ids,
                'field_info_parser': self._vcfpy_header.get_format_field_info
            }
        }

        for record_field_type in dispatcher.keys():
            record_field_ids = dispatcher[record_field_type]['ids']()
            for record_field_id in record_field_ids:
                record_field_line = dispatcher[record_field_type]['field_info_parser'](key=record_field_id)
                record_field = RecordField(record_field_line=record_field_line)
                self._record_fields.append(record_field)

    def _get_samples_from_vcfpy_header(self) -> [Sample]:
        """
        Get samples from vcfpy.header.Header
        """
        self._samples = []
        for sample_id in self._vcfpy_header.samples.names:
            sample = Sample(id=sample_id)
            self._samples.append(sample)

    def get_annotation_keys(self, annotation_field: str) -> list:
        """
        Get the annotation keys from the header annotations record field
        """
        annotation_keys = None
        annotation_keys_string_re = re.compile("(?P<annotation_keys_string>[\w\|]+)$")
        for record_field in self._record_fields:
            if record_field.id == annotation_field:
                annotation_keys = annotation_keys_string_re.search(record_field.description).groupdict()['annotation_keys_string'].split('|')
        return annotation_keys

    def to_dict(self) -> dict:
        """
        Returns a dict with all the properties of the class
        """
        data = {
            'file_format': self._file_format,
            'file_date': self._file_date,
            'variant_caller': self._variant_caller.to_dict(),
            'reference': self._reference,
            'contigs': [contig.to_dict() for contig in self._contigs],
            'record_fields': [record_field.to_dict() for record_field in self._record_fields],
            'samples': [sample.to_dict() for sample in self._samples],
        }
        return data

    @property
    def file_format(self) -> str:
        """
        Return the VCF file format
        """
        return self._file_format

    @file_format.setter
    def file_format(self, value: str):
        """
        Set VCF file format
        :param value: str
        """
        if type(value) == str:
            self._file_format = value

    @property
    def file_date(self) -> str:
        """
        Return the VCF generation file date
        """
        return self._file_date

    @file_date.setter
    def file_date(self, value: str):
        """
        Set the VCF generation file date
        :param value: str
        """
        if type(value) == str:
            self._file_date = value

    @property
    def variant_caller(self) -> VariantCaller:
        """
        Return a VarianCaller object
        """
        return self._variant_caller

    @variant_caller.setter
    def variant_caller(self, value: VariantCaller):
        """
        Set the variant caller used to generate the VCF
        :param value: VariantCaller
        """
        if type(value) == VariantCaller:
            self._variant_caller = value

    @property
    def reference(self) -> str:
        """
        Return the string path to the reference genome used to generate the VCF file
        """
        return self._reference

    @reference.setter
    def reference(self, value: str):
        """
        Set the string path to the reference genome used to generate the VCF file
        :param value: str
        """
        if type(value) == str:
            self._reference = value

    @property
    def contigs(self) -> [Contig]:
        """
        Returs a list of Contig objects
        """
        return self._contigs

    @contigs.setter
    def contigs(self, value: [Contig]):
        """
        Set a lists of Contig objects
        :param value: [Contig,...]
        """
        self._contigs = []

        if type(value) == list and len(value) != 0:
            for item in value:
                if type(item) == Contig:
                    self._contigs.append(item)
                else:
                    msg = "Only 'Contig' items are supported. '{}' item has been detected.".format(type(item))
                    raise TypeError(msg)

        elif type(value) == list and len(value) == 0:
            pass

        else:
            msg = "Only an empty list or 'Contig' object list is supported."
            raise TypeError(msg)

    @property
    def record_fields(self) -> [RecordField]:
        """
        Return a list of RecordField objects
        """
        return self._record_fields

    @record_fields.setter
    def record_fields(self, value: [RecordField]):
        """
        Set a list of Recordfield objects
        :param value: [RecordField,...]
        """
        self._record_fields = []

        if type(value) == list and len(value) != 0:
            for item in value:
                if type(item) == RecordField:
                    self._record_fields.append(item)
                else:
                    msg = "Only 'RecordField' items are supported. '{}' item has been detected.".format(type(item))
                    raise TypeError(msg)

        if type(value) == list and len(value) == 0:
            pass

        else:
            msg = "Only an empty list or 'RecordField' object list is supported."
            raise TypeError(msg)

    @property
    def samples(self) -> [Sample]:
        """
        Return a list of Sample objects
        """
        return self._samples

    @samples.setter
    def samples(self, value: [Sample]):
        """
        Set a list of Sampple objects
        :param value: [Sample,...]
        """
        self._samples = []

        if type(value) == list and len(value) != 0:
            for item in value:
                if type(item) == Sample:
                    self._samples.append(item)
                else:
                    msg = "Only 'Sample' items are supported. '{}' item has been detected.".format(type(item))
                    raise TypeError(msg)

        if type(value) == list and len(value) == 0:
            pass

        else:
            msg = "Only an empty list or 'Sample' object list is supported."
            raise TypeError(msg)
