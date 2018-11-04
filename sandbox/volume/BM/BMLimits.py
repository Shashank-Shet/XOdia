time_limits = {
    "cpp": 2000,
    "c"  : 2000,
    "py" : 6000,
}

resource_limits = {
    "cpp": ("--nofile=5", "--nproc=500", "--as=21460"),
    "c"  : ("--nofile=5", "--nproc=500", "--as=21460"),
    "py" : ("--nofile=5", "--nproc=500", "--as=32740")
}

