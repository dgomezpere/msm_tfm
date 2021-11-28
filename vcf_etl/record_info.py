class RecordInfo:
    def __init__(self, data=None):
        """
        Class to store the INFO data from a VCF record
        :param data: dict
        """
        self._data = None

        if data:
            self._data = data

    def to_dict(self) -> dict:
        """
        Return a dict with all the properties of record INFO data
        """
        return self._data

    @property
    def data(self) -> dict:
        """
        Return INFO data of a VCF record
        """
        return self._data

    @data.setter
    def data(self, value: dict):
        """
        Set INFO data of a VCF record
        """
        if type(value) == dict:
            self._data = value
