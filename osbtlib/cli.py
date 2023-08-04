import requests
from .exceptions import SendResultError

class CLIClient:
    def __init__(self, server_url="http://localhost:54454"):
        self.server_url = server_url

    def send_result(self, test_name, description, outcome, err_msg, countermeasure):
        data = {
            "test_name": test_name,
            "description": description,
            "outcome": outcome,
            "err_msg": err_msg,
            "countermeasure": countermeasure
        }
        try:
            response = requests.post(f"{self.server_url}/result/add", json=data)

            if response.status_code != 200:
                raise SendResultError(f"Failed to send result: {response.text}")

            return response.json()
        except Exception as e:
            raise SendResultError(f"Send Result Error: {str(e)}")