from subprocess import Popen, PIPE, call
from select import poll, POLLIN
from BMLimits import time_limits, resource_limits, MAX_BUFFER_LENGTH
import signal

def handler(signum, frame):
    raise IOError("Unable to open device")

signal.signal(signal.SIGALRM, handler)

class Process:
    
    def __init__(self, ext, exec_name):
        arg_list = [ "stdbuf", "-o0", "-e0", "-i0", "../bots/" + exec_name ]
        self.time_limit = time_limits[ext]
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

    def passInput(self, ip):
        if not isinstance(ip, bytes):
            self.popen_obj.stdin.write(ip.encode()+'\n')
        else:
            self.popen_obj.stdin.write(ip + '\n')
        self.popen_obj.stdin.flush()

    def readOutput(self):
        event_list = self.poll_obj.poll(self.time_limit)
        if event_list and event_list[0][1] is POLLIN:
            alarm(1)
            op = self.popen_obj.stdout.readline(MAX_BUFFER_LENGTH)
            alarm(0)
            return op.rstrip('\n')
        return None

    def isAlive(self):
        if self.popen_obj.poll() is None:
            return True
        return False
