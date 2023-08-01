import requests

class AttackerOPClient:
    def __init__(self, url: str):
        self.url = url

    # Add task 
    def __add_task(self, name: str, args: dict) -> str:
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
    def __get_task(self, task_id: str) -> dict:
        try:
            req = requests.get(self.url + f'/task/{task_id}')
            return req.json()
        except Exception as e:
            print("Get Task Error: ", e)

    # Delete task
    def __delete_task(self) -> dict:
        try:
            req = requests.delete(self.url + '/task')
            return req.json()
        except Exception as e:
            print("Delete Task Error: ", e)

    # ID Token Replacement for Responses
    def replace_id_token(self, new_id_token: str) -> bool:
        try:
            name = 'IDSpoofing'
            args = {
                'id_token': new_id_token
            }
            task_id = self.__add_task(name, args)
            if not task_id:
                return False
            
            return True

        except Exception as e:
            print("Replace ID Token Error: ", e) 
    
    # Provide malicious endpoints using the Discovery service
    def set_malicious_endpoints(self, endpoints: dict) -> bool:
        try:
            name = 'MaliciousEndpoint'
            args = endpoints
            task_id = self.__add_task(name, args)
            if not task_id:
                return False
            
            return True

        except Exception as e:
            print("Set Malicious Endpoints Error: ", e)

    # Redirect to Honest OP upon an authentication request
    def idp_confusion(self, honest_op_auth_endpoint: str) -> bool:
        try:
            name = 'IdPConfusion'
            args = {
                'honest_idp_auth_endpoint': honest_op_auth_endpoint
            }
            task_id = self.__add_task(name, args)
            if not task_id:
                return False
            
            return True
        
        except Exception as e:
            print("IDP Confusion Error: ", e)

    # clean
    def clean(self) -> bool:
        try:
            res = self.__delete_task()
            if not res:
                return False
            return True
        except Exception as e:
            print("Clean Error: ", e)