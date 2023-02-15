import json

from oidcop.server import Server


def init_server() -> Server:
    _str = open("oidc_op_config.json").read()
    cnf = json.loads(_str)
    return Server(cnf)
