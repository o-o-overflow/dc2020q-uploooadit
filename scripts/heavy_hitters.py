#!/usr/bin/env python3
import gzip
import sys
from collections import Counter
from datetime import datetime

import boto3

BUCKET = "uploooadit"


def main():
    session = boto3.Session(profile_name="ooo")
    s3 = session.client("s3")

    ec2 = session.resource("ec2")
    network_acl = ec2.NetworkAcl("acl-053f40ce8fec8e8d8")
    for entry in network_acl.entries:
        if entry["Egress"]:
            continue
        if 100 <= entry["RuleNumber"] < 1000:
            print(f"Unbanning {entry['CidrBlock']}")
            network_acl.delete_entry(Egress=False, RuleNumber=entry["RuleNumber"])

    ip_counter = Counter()
    max_timestamp = "0"
    min_timestamp = "3"

    for item in s3.list_objects(Bucket=BUCKET)["Contents"][-5:]:
        with gzip.GzipFile(
            fileobj=s3.get_object(Bucket=BUCKET, Key=item["Key"])["Body"]
        ) as fp:
            for line in fp.read().decode("utf-8").split("\n"):
                if not line:
                    continue
                parts = line.split(" ", 6)
                timestamp = parts[2]

                max_timestamp = max(max_timestamp, timestamp)
                min_timestamp = min(min_timestamp, timestamp)

                ip = parts[5].split(":", 1)[0]
                ip_counter[ip] += 1

    duration = datetime.fromisoformat(max_timestamp) - datetime.fromisoformat(
        min_timestamp
    )
    seconds = int(duration.total_seconds())
    print(f"Duration: {seconds} seconds")
    assert seconds > 300

    rule_number = 100
    for ip, count in ip_counter.most_common(10):
        rate = count / seconds
        if rate > 1:
            cidr = f"{ip}/32"
            print(f"Banning {cidr:>17s}\t{rate:5.02f} rps")
            network_acl.create_entry(
                CidrBlock=cidr,
                Egress=False,
                Protocol="-1",
                RuleAction="deny",
                RuleNumber=rule_number,
            )
            rule_number += 1


if __name__ == "__main__":
    sys.exit(main())
