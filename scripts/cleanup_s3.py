#!/usr/bin/env python3
import datetime
import itertools
import sys

import boto3

BUCKET = "uploooadit-files"


class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)


def grouper(iterable, n):
    while True:
        yield itertools.chain((next(iterable),), itertools.islice(iterable, n - 1))


def old_objects(client):
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET):
        now = datetime.datetime.now(tz=UTC())
        for item in page["Contents"]:
            age = (now - item["LastModified"]).total_seconds()
            if age > 60:
                yield item


def main():
    session = boto3.Session(profile_name="ooo")
    client = session.client("s3")
    s3 = session.resource("s3")
    bucket = s3.Bucket(BUCKET)

    for items in grouper(old_objects(client), 1000):
        objects = [{"Key": x["Key"]} for x in items]
        bucket.delete_objects(Delete={"Objects": objects})
        print(objects[-1]["Key"])


if __name__ == "__main__":
    sys.exit(main())
