#!/usr/bin/env python3
import sys
import time
import traceback

import requests
import uuid

SECRET = b"Congratulations!\nOOO{some really long string which blah blah blah}\n"
URL = "http://127.0.0.1:8000/files/"
USER_AGENT = "victim"


def put_file():
    response = requests.post(
        URL,
        data=SECRET,
        headers={
            "Content-Type": "text/plain",
            "User-Agent": "victim",
            "X-guid": str(uuid.uuid4()),
        },
        timeout=1,
    )
    if response.status_code == 201:
        sys.stdout.write(".")
        sys.stdout.flush()
    else:
        print()
        print(response)


def main():
    while True:
        try:
            put_file()
        except Exception:
            traceback.print_exc()
        time.sleep(2)


if __name__ == "__main__":
    sys.exit(main())
