# Module to handle file storage creation on upload and file upload
#from django import HttpResponse
from .__init__ import path
import os

file_directory_path = path + "files/"

allowed_file_ext = [      # Allowed uploadable file types
    "c",
    "cpp",
    "py"
    ]

max_size = 1000000                              # Max file size: 1MB


def file_storage_handle(file_object):
    file_name = file_object.name
    if not validate_extensions(file_name):
        return 1
    if not validate_size(file_object):
        return 2
    else:
        return 0


def validate_extensions(name):
    extension = name.split('.')[-1]        # split the name by '.' symbol and take last token
    if extension not in allowed_file_ext:
        return False
    else:
        return True


def validate_size(file_object):
    if file_object.size > max_size:
        return False
    else:
        return True
