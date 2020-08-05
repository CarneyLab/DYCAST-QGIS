from os import path

class LoadCasesParameters:
    def __init__(self, srid_of_cases, file_path: str):
        self.srid_of_cases = srid_of_cases
        self.file_path = file_path

    @property
    def srid_of_cases(self):
        return self._srid_of_cases

    @srid_of_cases.setter
    def srid_of_cases(self, value):
        if not value: raise ValueError("SRID of Cases cannot be empty")
        self._srid_of_cases = value

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        if not value: raise ValueError("Select an input file from your devise")
        if not path.exists(value): raise ValueError("File '{file_path}' does not exist".format(file_path=value))
        self._file_path = value
