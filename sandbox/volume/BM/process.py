'''
This module houses the bot process class and signal handler.
'''

from subprocess import Popen, PIPE, call
from select import poll, POLLIN
import signal
import psutil
from BMLimits import TIME_LIMITS, RESOURCE_LIMITS, MAX_BUFFER_LENGTH
from __init__ import botsdir

def handler(signum, frame):
    '''
    Custom signal handler for SIGALRM
    '''
    raise IOError("Unable to open device")

signal.signal(signal.SIGALRM, handler)

class Process:
    '''
    Adapter class to provide a simple API for bot processes, enabling one line
    initialisation, reading, writing, and polling.
    '''
    def __init__(self, ext, exec_name):
        '''
        Create a Popen process, save its PID and prlimit it based on ext.

        Parameters
        ----------
        ext: str
            Extension of the bot to be run.
        exec_name: str
            Name of the executable which will be run. (player1/player2)
        '''
        # Without stdbuf, reading bot output blocks indefinitely.
        arg_list = ["stdbuf", "-o0", "-e0", "-i0", botsdir + exec_name]
        self.time_limit = TIME_LIMITS[ext]
        self.popen_obj = Popen(arg_list, stdin=PIPE, stdout=PIPE)
        self.set_limits(ext)
        self.poll_obj = poll()
        self.proc_obj = psutil.Process(pid=self.popen_obj.pid)
        self.poll_obj.register(self.popen_obj.stdout.fileno(), POLLIN)

    def set_limits(self, ext):
        '''
        Prlimit encapsulated Popen process using limits provided in file
        BMLimits for bots with extension ext.

        Parameters
        ----------
        ext: str
            Extension of the bot to find limits for.
        '''
        prlimit_args = ["prlimit", "-p", str(self.popen_obj.pid)]
        prlimit_args.extend(RESOURCE_LIMITS[ext])
        call(prlimit_args)

    def suspend(self):
        '''Suspend one bot to dedicate cpu time to the other'''
        self.proc_obj.suspend()

    def resume(self):
        '''Resume current bot'''
        self.proc_obj.resume()

    def kill(self):
        '''
        If process is not dead, kills it.
        '''
        if self.popen_obj.poll() is None:
            self.popen_obj.kill()

    def pass_input(self, ip_string):
        '''
        Version independent method of writing input to the processes's stdin

        Parameters
        ----------
        ip_string: str
            String input to be passed to the bot.
        '''
        ip_string = ip_string.rstrip()
        if not isinstance(ip_string, bytes):
            self.popen_obj.stdin.write(ip_string.encode() + b'\n')
        else:
            self.popen_obj.stdin.write(ip_string + b'\n')
        self.popen_obj.stdin.flush()

    def read_output(self):
        '''
        Read either a line or MAX_BUFFER_LENGTH characters from the processes'
        stdout and returns it. The returned string will have no trailing
        newline. In case of a timout, it returns None.
        '''
        event_list = self.poll_obj.poll(self.time_limit)
        if event_list and event_list[0][1] is POLLIN:
            signal.alarm(1)
            op_string = self.popen_obj.stdout.readline(MAX_BUFFER_LENGTH)
            signal.alarm(0)
            return op_string.rstrip()
        return None

    def is_alive(self):
        '''
        Return True is process is alive, False otherwise.
        '''
        if self.popen_obj.poll() is None:
            return True
        return False
