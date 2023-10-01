from .proxy import ProxyClient
from .attacker_op import AttackerOPClient
from .browser import BrowserSimulator
from .cli import CLIClient
from . import id_token
from . import requestbin

class Osbtlib:
    def __init__(
        self, 
        proxy_extension_url: str = "http://localhost:5555",
        attacker_op_url: str = "http://localhost:9997",
        cli_server_url: str = "http://localhost:54454"
    ):
        self.proxy = ProxyClient(proxy_extension_url)
        self.attacker_op = AttackerOPClient(attacker_op_url)
        self.cli = CLIClient(cli_server_url)
        self.id_token = id_token
        self.requestbin = requestbin
