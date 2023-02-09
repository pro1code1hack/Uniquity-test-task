from django.forms import forms
from django.core.validators import FileExtensionValidator
from django.core.validators import FileExtensionValidator


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])

