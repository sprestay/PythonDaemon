import multiprocessing
import socket
import os
import time
import ex1


class Listener(multiprocessing.Process):
    def __init__(self, _ttl):
        super(Listener, self).__init__()
        self.ttl = _ttl
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 0))

    def get_pid(self):
        return self.pid

    def get_name(self):
        return self.socket.getsockname()

    def run(self):
        self.socket.listen(1)
        time.sleep(self.ttl)

    def listen(self):
        self.start()

