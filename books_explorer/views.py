import uuid

import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from API import APIRequest
from Ubiquity import settings
from .csv_utils import CsvFileValidator
from .forms import CSVUploadForm
from .models import CSVFiles
from .s3_utils import CustomS3


class UploadFileView(LoginRequiredMixin, FormView):
    form_class = CSVUploadForm
    template_name = 'upload_file.html'
    success_url = reverse_lazy('single_file')

    def form_valid(self, form):
        """
        This function is called when the form is valid. It will upload the file to S3 and save the url to the database.
        :param form: CSVUploadForm (UploadFileView.form_class)
        :return: redirect to the single file view in case of success.
        """

        # Validation of the file, imho, very cool implementation
        csv_file: InMemoryUploadedFile = self.request.FILES['csv_file']
        csv_validator = CsvFileValidator(csv_file)
        res = csv_validator.validate_all()
        if res is not True:
            CsvFileValidator.nullify_invalid_uuids()
            return render(self.request, self.template_name, {'form': form, 'errors': res})

        # generate unique id for the file and its name
        file_name_unique_id = uuid.uuid4()
        new_csv_name = '{}.csv'.format(str(file_name_unique_id))

        # upload file to s3 using custom s3 class
        s3 = CustomS3()
        s3.upload_file(str(csv_file), new_csv_name)

        # save file to db, get or create to avoid duplicates as we use uuid
        aws_url = s3.build_url_for_file(new_csv_name)
        CSVFiles.objects.get_or_create(aws_url=aws_url, uuid=file_name_unique_id, author=self.request.user)

        # redirect to single file view and pass the uuid
        APIRequest.make_request(settings.AWS_S3_ENDPOINT_URL, {'uuid': file_name_unique_id})

        return redirect('single_file', file_uuid=file_name_unique_id)

    def form_invalid(self, form):
        # Handling invalid form
        return render(self.request, self.template_name, {'form': form})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_data = []
        all_files_from_db = CSVFiles.objects.filter(author=self.request.user)

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

        context['all_data'] = all_data
        return context


class RenderOneFileView(TemplateView):
    template_name = 'render_one_file.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_uuid = kwargs['file_uuid']
        s3 = CustomS3()
        obj = s3.get_file(str(file_uuid) + '.csv')
        data = pd.read_csv(obj['Body'])
        context['data'] = data
        return context
