from subprocess import Popen, PIPE, call
from select import poll, POLLIN
from BMLimits import time_limits, resource_limits

class Process:
    
    def __init__(self, ext, exec_path):
        arg_list = [ "stdbuf", "-o0", "-e0", "-i0", exec_path ]
        self.popen_obj = Popen(arg_list, stdin=PIPE, stdout=PIPE)
        self.setLimits(ext)
        self.poll_obj = poll()
        self.poll_obj.register(self.popen_obj.stdout.fileno(), POLLIN)

    def setLimits(self, ext):
        prlimit_args = [ "prlimit", "-p", str(self.popen_obj.pid) ]
        prlimit_args.extend(resource_limits[ext])
        call(prlimit_args)

    def kill(self):
        if self.popen_obj.poll() is None:
            self.popen_obj.kill()

    def passInput(self):
        pass
    
    def waitForInput(self):
        pass

    def isAlive(self):
        if self.popen_obj.poll() is None:
            return True
        return False

    
