#!/usr/bin/env python3
import itertools
import sys

import boto3

BUCKET = "uploooadit-files"


def grouper(iterable, n):
    while True:
        yield itertools.chain((next(iterable),), itertools.islice(iterable, n - 1))


def main():
    session = boto3.Session(profile_name="ooo")
    s3 = session.resource("s3")
    bucket = s3.Bucket(BUCKET)

    for items in grouper(iter(bucket.objects.all()), 1000):
        objects = [{"Key": x.key} for x in items]
        bucket.delete_objects(Delete={"Objects": objects})
        print(objects[-1]["Key"])


if __name__ == "__main__":
    sys.exit(main())
