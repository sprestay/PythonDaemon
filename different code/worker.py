from daemon import Daemon
import time, sys
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from queue import Queue

class Program(Daemon):
    q = Queue()
    daemon = ('localhost', 6000)

    def add_new_task(self, task):
        self.q.put(task)
    
    def begin_work(self):
        task = self.q.get()
        print("STARTING ", task)


    def run(self):
        with Listener(self.daemon) as listener:
            response = None
            while not response:
                request = None
                while not request:
                    with listener.accept() as conn:
                        request = conn.recv()
                        self.add_new_task(request)


if __name__ == "__main__":
    daemon = Program('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
