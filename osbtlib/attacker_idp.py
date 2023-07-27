import requests

class AttackerIdPClient:
    def __init__(self, url: str):
        self.url = url

    # Add task 
    def add_task(self, name: str, args: dict) -> str:
        payload = {
            'name': name,
            'args': args
        }
        try:
            req = requests.post(self.url + '/task', json=payload)
            return req.json()['taskId']
        except Exception as e:
            print("Add Task Error: ", e)

    # Get task
    def get_task(self, task_id: str) -> dict:
        try:
            req = requests.get(self.url + f'/task/{task_id}')
            return req.json()
        except Exception as e:
            print("Get Task Error: ", e)

    # Delete task
    def delete_task(self) -> dict:
        try:
            req = requests.delete(self.url + '/task')
            return req.json()
        except Exception as e:
            print("Delete Task Error: ", e)
    


    