from multiprocessing.connection import Listener
from multiprocessing.connection import Client
import os

# адрес сервера (этого процесса) для входящих запросов
pid = os.fork()
print("PID", pid)
daemon = ('localhost', 63757)
# адрес клиента для исходящих ответов

with Listener(daemon) as listener:
    print("GOT A MESSAGE")
    response = None
    while not response:
        request = None
        while not request:
            with listener.accept() as conn:
                print("HERE")
                request = conn.recv()
        if request["method"] == "connect":
            response = api.connect(request)
        elif request["method"] == "disconnect":
            response = api.disconnect(request)
        else:
            response = None
        if response:
          try:
            with Client(cli) as conn:
                conn.send(response)
          except ConnectionRefusedError as e:
              logger.warning(e)
          else:
            response = None