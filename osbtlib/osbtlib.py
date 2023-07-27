from .proxy import ProxyClient
from .attacker_idp import AttackerIdPClient
from .brower import BrowserSimulator
from .cli import CLIClient
from . import id_token

class Osbtlib:
    def __init__(
        self, 
        proxy_extension_url: str = "http://localhost:5555",
        attacker_idp_url: str = "http://localhost:9997",
        cli_server_url: str = "http://localhost:54454"
    ):
        self.proxy = ProxyClient(proxy_extension_url)
        self.attacker_idp = AttackerIdPClient(attacker_idp_url)
        self.cli = CLIClient(cli_server_url)
        self.id_token = id_token
