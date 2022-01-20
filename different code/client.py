from multiprocessing.connection import Client
from multiprocessing.connection import Listener
import os

# адрес сервера (процесса в руте) для исходящих
# запросов
daemon = ('localhost', 6000)

def send(request: dict) -> bool or dict:
    """
    Принимает словарь аргументов удалённого метода.
    Отправляет запрос, после чего открывет сокет
    и ждет на нем ответ от сервера.
    """
    with Client(daemon) as conn:
        conn.send(request)

def hello(name: str) -> send:
    """
    Формирует уникальный запрос и вызывает функцию
    send для его отправки.
    """
    return send({
        "method": "hello",
        "name": name
    })

response = hello("Привет")