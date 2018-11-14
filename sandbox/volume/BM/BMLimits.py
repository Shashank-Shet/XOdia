'''
This module is simply to define constants for the working of the BM
The time, resource and buffer limits are below.
'''
TIME_LIMITS = {
    "cpp": 2000,
    "c"  : 2000,
    "py" : 6000,
}

RESOURCE_LIMITS = {
    "cpp": ("--nofile=5", "--nproc=500", "--as=21460"),
    "c"  : ("--nofile=5", "--nproc=500", "--as=21460"),
    "py" : ("--nofile=5", "--nproc=500", "--as=32740")
}

MAX_BUFFER_LENGTH = 100
