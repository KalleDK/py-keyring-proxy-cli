from typing import Optional

import keyring
import typer
from typing_extensions import Annotated

from keyring_proxy.socketproxy import SocketServer
from keyring_proxy.stdioproxy import StdioProxyFrontend, COMMAND_NAME

cli = typer.Typer()

socket_app = typer.Typer()
cli.add_typer(socket_app, name="socket")


@cli.command("cred")
def proxy_credential(service: str, username: Annotated[Optional[str], typer.Argument()] = None):
    try:
        cred = keyring.get_credential(service, username)
    except Exception as e:
        print(f"Error: {e}")
        return
    if cred is None:
        print("No credential found")
    else:
        print(f"Username: {cred.username!r}")
        print(f"Psername: {cred.password!r}")


@cli.command("get")
def proxy_get_password(service: str, username: str):
    password = keyring.get_password(service, username)
    if password is None:
        print("No password found")
    else:
        print(f"Password: {password!r}")


@cli.command("set")
def proxy_set_password(service: str, username: str, password: str):
    try:
        keyring.set_password(service, username, password)
        print("Password set")
    except Exception as e:
        print(f"Error: {e}")


@cli.command("del")
def proxy_del_password(service: str, username: str):
    try:
        keyring.delete_password(service, username)
        print("Password deleted")
    except Exception as e:
        print(f"Error: {e}")


@cli.command(COMMAND_NAME)
def proxy_json(data: str):
    client = StdioProxyFrontend()
    print(client.handle(data))


@socket_app.command("serve")
def socket_serve():
    server = SocketServer()
    server.serve()


def main():
    cli()


if __name__ == "__main__":
    main()
