import json
import socket

class ProxyClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def __send_data(self, data: str):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.sendall(data)
            s.close()
        except Exception as e:
            print("Error: ", e)

    def add_header(self, name: str, value: str):
        data = {
            "operation": "add_header",
            "name": name,
            "value": value
        }
        json_data = json.dumps(data)
        bytes_data = json_data.encode('utf-8')
        self.__send_data(bytes_data)

    def modify_header(self, name: str, value: str):
        data = {
            "operation": "modify_header",
            "name": name,
            "value": value
        }
        json_data = json.dumps(data)
        bytes_data = json_data.encode('utf-8')
        self.__send_data(bytes_data)

    def add_query_param(self, name: str, value: str):
        data = {
            "operation": "add_query_param",
            "name": name,
            "value": value
        }
        json_data = json.dumps(data)
        bytes_data = json_data.encode('utf-8')
        self.__send_data(bytes_data)

    def modify_query_param(self, name: str, value: str):
        data = {
            "operation": "modify_query_param",
            "name": name,
            "value": value
        }
        json_data = json.dumps(data)
        bytes_data = json_data.encode('utf-8')
        self.__send_data(bytes_data)

    def add_body_param(self, name: str, value: str):
        data = {
            "operation": "add_body_param",
            "name": name,
            "value": value
        }
        json_data = json.dumps(data)
        bytes_data = json_data.encode('utf-8')
        self.__send_data(bytes_data)

    def modify_body_param(self, name: str, value: str):
        data = {
            "operation": "modify_body_param",
            "name": name,
            "value": value
        }
        json_data = json.dumps(data)
        bytes_data = json_data.encode('utf-8')
        self.__send_data(bytes_data)

    def intercept(self, condition: str):
        data = {
            "operation": "intercept",
            "condition": condition
        }
        json_data = json.dumps(data)
        bytes_data = json_data.encode('utf-8')
        self.__send_data(bytes_data)
    
    def clean(self):
        data = {
            "operation": "clean"
        }
        json_data = json.dumps(data)
        bytes_data = json_data.encode('utf-8')
        self.__send_data(bytes_data)