import requests
import json
from .exceptions import GetHistoryError

def get_requestbin_history(pipedream_token: str, source_id: str):
    try:
        headers = {"Authorization": f"Bearer {pipedream_token}"}
        url = f"https://api.pipedream.com/v1/sources/{source_id}/event_summaries?expand=event"
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Directly return JSON if the response is OK
        else:
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    
    except requests.HTTPError as http_err:
        raise GetHistoryError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise GetHistoryError(f"An error occurred: {err}")