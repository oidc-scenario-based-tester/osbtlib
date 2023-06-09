import json
import socket

def send_data(data: str):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 5555))
        s.sendall(data)
        s.close()
    except Exception as e:
        print("Error: ", e)

def add_header(name: str, value: str):
    data = {
        "operation": "add_header",
        "name": name,
        "value": value
    }
    json_data = json.dumps(data)
    bytes_data = json_data.encode('utf-8')
    send_data(bytes_data)

def modify_header(name: str, value: str):
    data = {
        "operation": "modify_header",
        "name": name,
        "value": value
    }
    json_data = json.dumps(data)
    bytes_data = json_data.encode('utf-8')
    send_data(bytes_data)

def add_body_param(name: str, value: str):
    data = {
        "operation": "add_body_param",
        "name": name,
        "value": value
    }
    json_data = json.dumps(data)
    bytes_data = json_data.encode('utf-8')
    send_data(bytes_data)

def modify_body_param(name: str, value: str):
    data = {
        "operation": "modify_body_param",
        "name": name,
        "value": value
    }
    json_data = json.dumps(data)
    bytes_data = json_data.encode('utf-8')
    send_data(bytes_data)

def intercept(condition: str):
    data = {
        "operation": "intercept",
        "condition": condition
    }
    json_data = json.dumps(data)
    bytes_data = json_data.encode('utf-8')
    send_data(bytes_data)

if __name__ == "__main__":
    # add_header("HOGE-HUGA", "hogehoge")
    # modify_header("HOGE-HUGA", "hugahuga")
    # add_body_param("hoge", "piyo")
    # modify_body_param("username", "yuasa2")
    # intercept("huga")