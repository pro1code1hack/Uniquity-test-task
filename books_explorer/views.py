import uuid

import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CSVUploadForm
from .csv_utils import CsvFileValidator
from .models import CSVFiles
from API import APIRequest
from .s3_utils import CustomS3


@login_required
def upload_file(request):
    # First of all check if user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.method == 'POST':
        # Here we set up the form
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Validation of the file, imho, very cool implementation
            csv_file: InMemoryUploadedFile = request.FILES['csv_file']
            csv_validator = CsvFileValidator(csv_file)
            res = csv_validator.validate_all()
            if res is not True:
                CsvFileValidator.nullify_invalid_uuids()
                return render(request, 'upload_file.html', {'form': form, 'errors': res})

            # generate unique id for the file and its name
            file_name_unique_id = uuid.uuid4()
            new_csv_name = '{}.csv'.format(str(file_name_unique_id))

            # upload file to s3 using custom s3 class
            s3 = CustomS3()
            s3.upload_file(str(csv_file), new_csv_name)

            # save file to db, get or create to avoid duplicates as we use uuid
            aws_url = s3.build_url_for_file(new_csv_name)
            CSVFiles.objects.get_or_create(aws_url=aws_url, uuid=file_name_unique_id, author=request.user)

            # send request to aws lambda (kinda) --> like a cron job :)
            APIRequest.make_request(settings.AWS_S3_ENDPOINT_URL, {'uuid': file_name_unique_id})

            # redirect to single file view and pass the uuid
            return HttpResponseRedirect('/{}'.format(file_name_unique_id))
    else:
        form = CSVUploadForm()
    return render(request, 'upload_file.html', context={'form': form})


def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    all_data = []
    all_files_from_db = CSVFiles.objects.filter(author=request.user)

    s3 = CustomS3()
    for file in all_files_from_db:
        obj = s3.get_file(str(file.uuid) + '.csv')
        data = pd.read_csv(obj['Body'])
        all_data.append({
            'uuid': file.uuid,
            'author': file.author,
            'aws_url': file.aws_url,
            'data': data,
        })

    return render(request, 'home.html', {'all_data': all_data})


def render_one_file(request, file_uuid: str):
    s3 = CustomS3()
    obj = s3.get_file(str(file_uuid) + '.csv')
    data = pd.read_csv(obj['Body'])
    return render(request, 'render_one_file.html', {'data': data})
