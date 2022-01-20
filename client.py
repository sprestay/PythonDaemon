from multiprocessing.connection import Listener
from multiprocessing.connection import Client
import json, socket

daemon = ('localhost', 6666)

def send(request):
    sock = socket.socket()
    sock.connect(daemon)
    sock.send(request)
    data = sock.recv(3333)
    print(data.decode("utf-8"))
    sock.close()


    
send(str.encode(json.dumps({"service_name": "hello_service", "content": {"input_params": {"name": "Ivan"}, "output_params": {"res": "S"}}, "method": "ADD", "type": "sync"})))
send(str.encode(json.dumps({"service_name": "hello_service", "content": {"input_params": {"name": "Olya"}, "output_params": {"res": "S"}}, "method": "ADD", "type": "async"})))
send(str.encode(json.dumps({"service_name": "hello_service", "content": {"input_params": {"name": "Katya"}, "output_params": {"res": "S"}}, "method": "ADD", "type": "async"})))
send(str.encode(json.dumps({"service_name": "hello_service", "content": {"input_params": {"name": "Kolya"}, "output_params": {"res": "S"}}, "method": "ADD", "type": "sync"})))
send(str.encode(json.dumps({"service_name": "hello_service", "content": {"input_params": {"name": "Eva"}, "output_params": {"res": "S"}}, "method": "ADD", "type": "async"})))