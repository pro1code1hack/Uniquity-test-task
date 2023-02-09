from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
import uuid
import pandas as pd
from django.contrib.auth.models import User

# Create your models here.

"""
The CSV file will contain the following columns:
■ Book title
■ Book author
■ Date published
■ Unique identifier for the book (which one is not important)
■ Publisher name
"""


class CSVFiles(models.Model):
    uuid = models.UUIDField(unique=True, editable=False)
    aws_url = models.URLField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.aws_url

    @property
    def file_name(self) -> str:
        return self.aws_url.split('/')[-1]


class Book(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date_published = models.DateField(auto_now=True)
    publisher = models.CharField(max_length=255)

    def __str__(self):
        return str(self.uuid)

    def convert_to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(self)

    @classmethod
    def to_dict(cls) -> dict:
        """
        This function returns a dictionary of the class attributes.
        """
        return {
            'uuid': cls.uuid,
            'title': cls.title,
            'author': cls.author,
            'date_published': cls.date_published,
            'publisher': cls.publisher,
        }

    @classmethod
    def get_keys(cls) -> list:
        """
        This function returns a list of the class attributes.
        It will be used to validate the header of the csv file.
        """
        return list(cls.to_dict().keys())
