import time, sys, os, json, uuid, subprocess, socket, threading
from queue import Queue


class Program():
    q = Queue()
    daemon = ('localhost', 6666)
    cli = ('localhost', 9999)
    max_tasks = 3
    max_connections = 100
    current_processes = []

    def add_task(self, service, content):
        task_id = str(uuid.uuid1())
        self.q.put({
            "task_id": task_id,
            "service_name": service,
            "input_params": content['input_params'],
            "output_params": content['output_params']
        })
        return task_id

    def start_processing_task(self):
        while len(self.current_processes) < self.max_tasks and self.q.qsize() > 0:
            task = self.q.get()
            with open(os.path.join("scripts", "input", "{}.json".format(task['task_id'])), 'w+') as fd:
                fd.write(json.dumps(task['input_params']))
            p = subprocess.Popen(["python3", os.path.join("scripts", "{}.py".format(task['service_name'])), task['task_id']], shell=False)
            self.current_processes.append(task['task_id'])

    def clear_current_processes(self):
        folder = os.path.join("scripts", "output")
        files = os.listdir(folder)
        for f in files:
            task_id = f.split(".")[0]
            if task_id in self.current_processes:
                self.current_processes.remove(task_id)
        

    def client_msg(self, conn, task_id, _type):
        if not task_id:
            response = "wrong request"
        elif _type == 'async':
            response = "Task %s added" % task_id
        elif _type == 'sync':
            folder = os.path.join("scripts", "output")
            while True:
                fs = [x.split(".")[0] for x in os.listdir(folder)]
                if task_id in fs:
                    break
            response = "%s task done" % task_id
        conn.send(str.encode(response))
        conn.close()

    def run(self):
        sock = socket.socket()
        sock.bind(self.daemon)
        sock.listen(self.max_connections)
        sock.setblocking(0)
        while True:
            self.clear_current_processes()
            self.start_processing_task()
            try:
                conn, addr = sock.accept()
                data = conn.recv(9000)
                request = json.loads(data.decode("utf-8"))
                if 'service_name' in request and 'content' in request and request['method'] == "ADD":
                    task_id = self.add_task(request['service_name'], request['content'])
                else:
                    task_id = None

                threading.Thread(target=self.client_msg, args=(conn,task_id, request['type']), daemon=True).start() 
            except Exception as e:
                if (str(e.args[0]) != "35"):
                    print(e)
                pass



if __name__ == "__main__":
    print("DAEMON PID: ", os.getpid())
    daemon = Program()
    daemon.run()