import vcfpy
from record_info import RecordInfo
from record_call import RecordCall
from record_annotation import RecordAnnotation

class VcfRecord:
    def __init__(self, record=None, record_fields=None, annotation_field=None, annotation_keys=None, annotation_sep=None):
        """
        Class to store data of a VCF record
        :param record: vcfpy.Record object
        :param annotation_field: Record annotation INFO field ID (i.e. 'CSQ')
        :param annotation_keys: A list of annotation field IDs
        :param annotation_list_sep: Character used to separate different record annotations (i.e. ',')
        :param annotation_sep: Character used to separate annotation value fields of a record annotation (i.e. '|')
        """
        # Initialize all properties to None
        self._record = None
        self._record_fields = None
        self._id = None
        self._chrom = None
        self._pos = None
        self._start = None
        self._end = None
        self._ref = None
        self._alt = None
        self._type = None
        self._qual = None
        self._info = []
        self._calls = []
        self._annotation_field = None
        self._annotation_keys = None
        self._annotation_sep = None
        self._annotations = []

        # Populate object with a vcfpy.Record
        if record and type(record) == vcfpy.Record:
            self._record = record
            self._record_fields = record_fields
            self._get_vcfpy_record_id()
            self._get_vcfpy_record_chrom()
            self._get_vcfpy_record_pos()
            self._get_vcfpy_record_start()
            self._get_vcfpy_record_end()
            self._get_vcfpy_record_ref()
            self._get_vcfpy_record_alt()
            self._get_vcfpy_record_type()
            self._get_vcfpy_record_qual()
            self._get_vcfpy_record_info()
            self._get_vcfpy_record_calls()

        if annotation_field and annotation_keys and annotation_sep:
            self._annotation_field = annotation_field
            self._annotation_keys = annotation_keys
            self._annotation_sep = annotation_sep
            self._get_vcfpy_record_annotations()
            self._get_vcfpy_record_info()

    def _get_vcfpy_record_id(self) -> str:
        """
        Get the id of a vcfpy.Record
        """
        self._id = "{chrom}:{pos}|{ref}|{alt}".format(
            chrom = self._record.CHROM,
            pos = self._record.POS,
            ref = self._record.REF,
            alt = self._record.ALT[0].value
        )

    def _get_vcfpy_record_chrom(self) -> str:
        """
        Get the chromosome of a vcfpy.Record
        """
        self._chrom = self._record.CHROM

    def _get_vcfpy_record_pos(self) -> int:
        """
        Get the 1-based begin position of a vcfpy.Record
        """
        self._pos = self._record.POS

    def _get_vcfpy_record_start(self) -> int:
        """
        Get the 0-based affected start position of a vcfpy.Record
        """
        self._start = self._record.affected_start

    def _get_vcfpy_record_end(self) -> int:
        """
        Get the 0-based affected end position of a vcfpy.Record
        """
        self._end = self._record.affected_end

    def _get_vcfpy_record_ref(self) -> str:
        """
        Get the REF (reference) allele of a vcfpy.Record
        :return: str
        """
        self._ref = self._record.REF

    def _get_vcfpy_record_alt(self) -> str:
        """
        Get the ALT (alternate) allele of a biallelic vcfpy.Record
        """
        self._alt = self._record.ALT[0].value

    def _get_vcfpy_record_type(self) -> str:
        """
        Get the ALT (alternate) allele type of a biallelic vcfpy.Record
        """
        self._type = self._record.ALT[0].type

    def _get_vcfpy_record_qual(self) -> float:
        """
        Get the QUAL of a vcf.Record
        """
        self._qual = self._record.QUAL

    def _get_vcfpy_record_info(self) -> RecordInfo:
        """
        Get the RecordInfo object from a vcfpy.Record
        """
        data = self._record.INFO
        # Remove annotation field from info data
        if self._annotation_field:
            data.pop(self._annotation_field, None)

        # Extract per alternate allele values from lists because variant records from input VCF file are decomposed
        for record_field in self._record_fields:
            if record_field.field_type == 'INFO' and record_field.number == 'A' and type(data[record_field.id]) == list and len(data[record_field.id]) == 1:
                data[record_field.id] = data[record_field.id][0]
        self._info = RecordInfo(data=data)

    def _get_vcfpy_record_calls(self) -> [RecordCall]:
        """
        Get a list of RecordCall objects from a vcfpy.Record
        """
        self._calls = []
        for call in self._record.calls:
            data = call.data
            for record_field in self._record_fields:
                if record_field.field_type == 'FORMAT' and record_field.number == 'A' and type(data[record_field.id]) == list and len(data[record_field.id]) == 1:
                    data[record_field.id] = data[record_field.id][0]
            call.data = data
            self._calls.append(RecordCall(call=call))

    def _get_vcfpy_record_annotations(self) -> [RecordAnnotation]:
        """
        Get a list of RecordAnnotation obejcts from a vcfpy.Record
        """

        # Get annotation field content from vcfpy.Record.INFO
        annotations = self._record.INFO[self._annotation_field]
        # Split mutiple annotations for a record by a separator
        for annotation_str in annotations:
            # Split annotation values by a separator
            annotation_values = annotation_str.split(self._annotation_sep)
            # Create a dictionary of annotations
            annotation_data = dict(zip(self._annotation_keys, annotation_values))
            # Append RecordAnnotation objects
            self._annotations.append(RecordAnnotation(data=annotation_data))

    def to_dict(self):
        """
        Returns a dict with all the properties of the class
        """
        data = {
            'id': self._id,
            'chrom': self._chrom,
            'pos': self._pos,
            'start': self._start,
            'end': self._end,
            'ref': self._ref,
            'alt': self._alt,
            'type': self._type,
            'qual': self._qual,
            'info': {'id': self._id, **self._info.to_dict()},
            'calls': [{'id': self._id, **call.to_dict()} for call in self._calls],
            'annotations': [{'id': self._id, **annotation.to_dict()} for annotation in self._annotations],
        }
        return data

    @property
    def id(self) -> str:
        """
        Return record id
        """
        return self._id

    @id.setter
    def id(self, value: str):
        """
        Set record id
        """
        if type(value) == str:
            self._id = value

    @property
    def chrom(self) -> str:
        """
        Return record chromosome
        """
        return self._chrom

    @chrom.setter
    def chrom(self, value: str):
        """
        Set record chromosome
        """
        if type(value) == str:
            self._chrom = value

    @property
    def pos(self) -> int:
        """
        Return 1-based record position
        """
        return self._pos

    @pos.setter
    def pos(self, value: int):
        """
        Set 1-based record position
        """
        if type(value) == int:
            self._pos = value

    @property
    def start(self) -> int:
        """
        Return record 0-based affected start position
        """
        return self._start

    @start.setter
    def start(self, value: int):
        """
        Set record 0-based affected start position
        """
        if type(value) == int:
            self._start = value

    @property
    def end(self) -> int:
        """
        Return record 0-based affected end position
        """
        return self._end

    @end.setter
    def end(self, value: int):
        """
        Set record 0-based affected end position
        """
        if type(value) == int:
            self._end = value

    @property
    def ref(self) -> str:
        """
        Return record REF (reference) allele
        """
        return self._ref

    @ref.setter
    def ref(self, value: str):
        """
        Set record REF (reference) allele
        """
        if type(value) == str:
            self._ref = value

    @property
    def alt(self) -> str:
        """
        Return record ALT (alternate) allele
        """
        return self._alt

    @alt.setter
    def alt(self, value: str):
        """
        Set record ALT (alternate) allele
        """
        if type(value) == str:
            self._alt = value

    @property
    def type(self) -> str:
        """
        Return record ALT (alternate) allele type
        """
        return self._type

    @type.setter
    def type(self, value: str):
        """
        Set record ALT (alternate) allele type
        """
        if type(value) == str:
            self._type = value

    @property
    def qual(self) -> float:
        """
        Return record QUAL
        """
        return self._qual

    @qual.setter
    def qual(self, value: float):
        """
        Set record QUAL
        """
        if type(value) == float:
            self._qual = value

    @property
    def info(self) -> RecordInfo:
        """
        Return record INFO data as a RecordInfo
        """
        return self._info

    @info.setter
    def info(self, value: RecordInfo):
        """
        Set record INFO data as a RecordInfo object
        """
        if type(value) == RecordInfo:
            self._info = value

    @property
    def calls(self) -> [RecordCall]:
        """
        Return a list of record calls data as a list of RecordCall objects
        """
        return self._calls

    @calls.setter
    def calls(self, value: [RecordCall]):
        """
        Set a list of record calls data as a list of RecordCall objects
        """
        if type(value) == list:
            test_calls = []
            for item in value:
                test_calls.append(type(item)==RecordCall)
            if all(test_calls):
                self._calls = value

    @property
    def annotations(self) -> [RecordAnnotation]:
        """
        Return a list or record annotations data as a list of RecordAnnotation objects
        """
        return self._annotations

    @annotations.setter
    def annotations(self, value: [RecordAnnotation]):
        """
        Set a list of record annotations data as a list of RecordAnnotation objects
        """
        if type(value) == list:
            test_annotations = []
            for item in value:
                test_annotations.append(type(item)==RecordAnnotation)
            if all(test_annotation):
                self._annotations = value
