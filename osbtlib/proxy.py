import json
import requests
from .exceptions import SendDataError

class ProxyClient:
    def __init__(self, url: str):
        self.url = url

    def send_data(self, data: dict) -> dict:
        try:
            response = requests.post(self.url, json=data)
            if response.status_code != 200:
                raise Exception("Server returned status code: " + str(response.status_code))
            return response.json()
        except Exception as e:
            raise SendDataError(f"Send Data Error: {str(e)}")

    def add_header(self, name: str, value: str) -> dict:
        data = {
            "operation": "add_header",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def modify_header(self, name: str, value: str) -> dict:
        data = {
            "operation": "modify_header",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def add_query_param(self, name: str, value: str) -> dict:
        data = {
            "operation": "add_query_param",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def modify_query_param(self, name: str, value: str) -> dict:
        data = {
            "operation": "modify_query_param",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def add_body_param(self, name: str, value: str) -> dict:
        data = {
            "operation": "add_body_param",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def modify_body_param(self, name: str, value: str) -> dict:
        data = {
            "operation": "modify_body_param",
            "name": name,
            "value": value
        }
        return self.send_data(data)

    def intercept_request(self, condition: str) -> dict:
        data = {
            "operation": "intercept_request",
            "condition": condition
        }
        return self.send_data(data)
    
    def intercept_response(self, condition: str) -> dict:
        data = {
            "operation": "intercept_response",
            "condition": condition
        }
        return self.send_data(data)
    
    def get_history(self) -> dict:
        data = {
            "operation": "get_history"
        }
        return self.send_data(data)

    def clean(self) -> dict:
        data = {
            "operation": "clean"
        }
        return self.send_data(data)