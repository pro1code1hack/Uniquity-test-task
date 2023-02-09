import csv
from typing import Optional, List, Any

from .models import Book
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid


class CsvFileValidator:
    invalid_uuids = []

    def __init__(self, csv_file: InMemoryUploadedFile):
        """
        Alright, so here we store the csv file in memory and then we can use it to validate the header and other
        essential things.

        We also store the header in a property so that we can use it later on.
        :param csv_file:
        """
        self.csv_file = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
        self.__header = self.header

    @property
    def header(self) -> Optional[list]:
        return self.csv_file.fieldnames

    def validate_header(self) -> None:
        """
        This function validates the header of the csv file.
        :return:
        """
        if self.__header != Book.get_keys():
            raise ValueError('Invalid header')

    def validate_uuid(self) -> list[Any] | bool:
        """
        This function validates the uuid of the csv file.
        :return:
        """
        for row in self.csv_file:
            try:
                uuid.UUID(row['uuid'])
            except ValueError:
                self.invalid_uuids.append(row['uuid'])
        if len(self.invalid_uuids) > 0:
            return self.invalid_uuids
        return True

    def validate_all(self) -> list[Any] | bool:
        """
        This function validates the header and uuid of the csv file.
        :return:
        """
        self.validate_header()
        return self.validate_uuid()

    @classmethod
    def nullify_invalid_uuids(cls):
        """
        This function nullifies the invalid uuids.
        :return:
        """
        cls.invalid_uuids = []
