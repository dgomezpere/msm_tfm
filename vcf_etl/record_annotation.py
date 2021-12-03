class RecordAnnotation:
    def __init__(self, data=None):
        """
        Class to store Info varian annotation data from a given record
        :param data: dict
        """
        self._data = None

        if data:
            self._data = data

    def to_dict(self) -> dict:
        """
        Return a dict with all the properties of a record annotation
        """
        return self._data

    @property
    def data(self) -> dict:
        """
        Return annotation data
        """
        return self._data

    @data.setter
    def data(self, value: dict):
        """
        Set annotation data
        """
        if type(value) == dict:
            self._data = value
