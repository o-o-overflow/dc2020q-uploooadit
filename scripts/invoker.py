#!/usr/bin/env python3
import argparse
import sys
import time
import traceback
import uuid

import daemon
import requests

SECRET = b"Congratulations!\nOOO{some really long string which blah blah blah}\n"
URL = "http://127.0.0.1:8080/files/"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true")
    arguments = parser.parse_args()

    if arguments.daemon:
        with daemon.DaemonContext():
            run_loop()
    else:
        run_loop()


def put_file():
    response = requests.post(
        URL,
        data=SECRET,
        headers={
            "Content-Type": "text/plain",
            "User-Agent": "invoker",
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


def run_loop():
    while True:
        try:
            put_file()
        except Exception:
            traceback.print_exc()
        time.sleep(2)


if __name__ == "__main__":
    sys.exit(main())
