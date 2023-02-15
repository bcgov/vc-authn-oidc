import json
from oidcop.server import Server


def init_server() -> Server:
    _str = open(".json").read()
    cnf = json.loads(_str)
    return Server(cnf, cwd="/oidc")
