import json
import base64

# get header of ID Token
def get_header(id_token: str) -> dict:
    if isinstance(id_token, bytes):
        id_token = id_token.decode('utf-8')
    header, _, _ = id_token.split('.')
    header_decoded = json.loads(base64.urlsafe_b64decode(header + '==').decode())
    return header_decoded

# replace header of ID Token
def replace_header(id_token: str, new_header: dict) -> str:
    if isinstance(id_token, bytes):
        id_token = id_token.decode('utf-8')
    header, payload, signature = id_token.split('.')
    new_header_encoded = base64.urlsafe_b64encode(json.dumps(new_header).encode()).rstrip(b'=').decode()
    new_token = f"{new_header_encoded}.{payload}.{signature}"
    return new_token

# get payload of ID Token
def get_payload(id_token: str) -> dict:
    if isinstance(id_token, bytes):
        id_token = id_token.decode('utf-8')
    _, payload, _ = id_token.split('.')
    payload_decoded = json.loads(base64.urlsafe_b64decode(payload + '==').decode())
    return payload_decoded

# replace payload of ID Token
def replace_payload(id_token: str, new_payload: dict) -> str:
    if isinstance(id_token, bytes):
        id_token = id_token.decode('utf-8')
    header, payload, signature = id_token.split('.')
    new_payload_encoded = base64.urlsafe_b64encode(json.dumps(new_payload).encode()).rstrip(b'=').decode()
    new_token = f"{header}.{new_payload_encoded}.{signature}"
    return new_token

# get signature of ID Token
def get_signature(id_token: str) -> str:
    if isinstance(id_token, bytes):
        id_token = id_token.decode('utf-8')
    _, _, signature = id_token.split('.')
    return signature

# replace signature of ID Token
def replace_signature(id_token: str, new_signature: str) -> str:
    if isinstance(id_token, bytes):
        id_token = id_token.decode('utf-8')
    header, payload, _ = id_token.split('.')
    new_token = f"{header}.{payload}.{new_signature}"
    return new_token