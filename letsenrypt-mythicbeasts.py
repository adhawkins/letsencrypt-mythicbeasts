#!/usr/bin/env python3

import click
import os
import time

import authentication
from MythicBeastsDNS import MythicBeastsDNS


@click.group()
def cli():
    pass


@cli.command()
def addRecord():
    print(f"Adding record... {domain} -> {validation}")

    client.AddTXTRecord(domain, validation)

    count = 1
    while True:
        records = client.LookupRecord(domain, "TXT")
        if records is not None:
            break

        # print(f"Record not found yet, sleeping for 1 second...({count})")
        count += 1
        time.sleep(1)

    print("Resolved TXT records:")
    for record in records:
        print(f" - {record}")


@cli.command()
def deleteRecord():
    print(f"Deleting record... {domain}")

    client.DeleteTXTRecord(domain)

    # count = 1
    # while True:
    #     records = client.LookupRecord(domain, "TXT")
    #     if records is None:
    #         break

    #     # print(f"Record still exists, sleeping for 1 second...({count})")
    #     count += 1
    #     time.sleep(1)


if __name__ == "__main__":
    domain = "_acme-challenge." + os.getenv("CERTBOT_DOMAIN")
    validation = os.getenv("CERTBOT_VALIDATION")

    client = MythicBeastsDNS(authentication.KEY, authentication.SECRET)

    cli()
