import json
import requests

class ProxyClient:
    def __init__(self, url: str):
        self.url = url

    def send_data(self, data: dict):
        try:
            response = requests.post(self.url, json=data)
            if response.status_code != 200:
                raise Exception("Server returned status code: " + str(response.status_code))
            return response.json()
        except Exception as e:
            print("Error: ", e)

    def add_header(self, name: str, value: str):
        data = {
            "operation": "add_header",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def modify_header(self, name: str, value: str):
        data = {
            "operation": "modify_header",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def add_query_param(self, name: str, value: str):
        data = {
            "operation": "add_query_param",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def modify_query_param(self, name: str, value: str):
        data = {
            "operation": "modify_query_param",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def add_body_param(self, name: str, value: str):
        data = {
            "operation": "add_body_param",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def modify_body_param(self, name: str, value: str):
        data = {
            "operation": "modify_body_param",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def intercept(self, condition: str):
        data = {
            "operation": "intercept",
            "condition": condition
        }
        return self.send_data(data)
    
    def get_history(self):
        data = {
            "operation": "get_history"
        }
        return self.send_data(data)


    def clean(self):
        data = {
            "operation": "clean"
        }
        return self.send_data(data)