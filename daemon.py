import subprocess, os, sys


class Daemon():
    path = "my_process.pid"
    
    def __init__(self):
        if sys.platform in ("linux", "linux2", "darwin"):
            self.kill_command = "kill {}"
        else: # случай с windows
            self.kill_command = "taskkill /F /PID {}" 

    def start(self):
        if (os.path.exists(self.path)):
            old_pid = open(self.path, "r").read()
            if len(old_pid):
                print("Process already running {}".format(old_pid))
                exit(0)

        fd = open("stdout.txt","a+")
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(fd.fileno(), sys.stdout.fileno())
        os.dup2(fd.fileno(), sys.stderr.fileno())
        process = subprocess.Popen(["python3", "server.py"], shell=False, stdout=fd.fileno())

        pidfile = open(self.path, 'a')
        pidfile.write(str(process.pid) + "\n" + str(os.getpid()) + "\n")
        pidfile.close()

        print("Process is running! - ", process.pid)
    
    def stop(self):
        with open(self.path, "r") as fd:
            for l in fd.readlines():
                os.system(self.kill_command.format(l))
                print(l, "killed")
                
        with open(self.path, "w") as fd:
            fd.write("")
        

if __name__ == "__main__":
    daemon = Daemon()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        else:
            print ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)