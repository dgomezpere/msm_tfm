from collections import OrderedDict

class RecordCall:
    def __init__(self, call=None):
        """
        Class to store sample and call data of a VCF record call
        :param value: vcfpy.record.Call
        """
        # Initialize all properties to None
        self._call = None
        self._sample = None
        self._data = OrderedDict()

        if call:
            self._call = call
            self._get_vcfpy_call_sample()
            self._get_vcfpy_call_data()

    def _get_vcfpy_call_sample(self):
        """
        Get the sample ID of a VCF record call
        :param value: vcfpy.record.Call
        """
        self._sample = self._call.sample

    def _get_vcfpy_call_data(self):
        """
        Get the call data of a VCF record call
        :param value: vcfpy.record.Call
        """
        self._data = OrderedDict(self._call.data)

    def to_dict(self):
        """
        Return a dict with the properties of a record call
        """
        data = {
            'sample':self._sample,
            **self._data
        }
        return data

    @property
    def sample(self) -> str:
        """
        Return the sample ID
        """
        return self._sample

    @sample.setter
    def sample(self, value: str):
        """
        Set the sample ID
        """
        if type(value) == str:
            self._sample = value

    @property
    def data(self) -> OrderedDict:
        """
        Return call data in an OrderedDict
        :return: OrderedDict
        """
        return self._data

    @data.setter
    def data(self, value: OrderedDict):
        """
        Set call data from an OrderedDict
        """
        if type(value) == OrderedDict:
            self._data = value
