import os
cases = ["test_scirpt.py", "test.py", "server.py", "first_script.py"]
os.system("ps -x > processes.txt")
with open('processes.txt', 'r') as fd:
    for line in fd.readlines():
        if any(c in line.lower() for c in cases):
            pid = line[:5]
            os.system("kill {}".format(pid))
            print(pid, "deleted")


