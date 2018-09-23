from threading import Thread, Event
from collections import deque
from Sandbox import SandboxRequest
request_queue = deque()

class RequestQueue(Thread):
    event_obj = Event()

    def __init__(self):
        Thread.__init__(self)
        self.event_obj.clear()

    def clear_flag(self):
        self.event_obj.clear()

    def set_flag(self):
        self.event_obj.set()

    def run(self):
        while True:
            self.event_obj.wait()
            while len(request_queue):
                req_obj = request_queue.popleft()
                # Sandbox logic
                req_obj.runSandbox(req_obj.stage2_marking)
            self.clear_flag()
            print "Flag cleared"
