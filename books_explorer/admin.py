from django.contrib import admin
from .models import CSVFiles


@admin.register(CSVFiles)
class CSVFilesAdmin(admin.ModelAdmin):
    list_display = ('author', 'uuid', 'aws_url')
    list_filter = ('author', 'uuid', 'aws_url')
    search_fields = ('author', 'uuid', 'aws_url')
    ordering = ('author', 'uuid', 'aws_url')
