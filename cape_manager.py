#!/bin/env python3

"""
Cape Manager

Easy utilities to manager SnR dev capes
"""

import argparse
import sys
import urllib.request
import json
from uuid import UUID
from typing import Any


def uname_to_uuid(uname: str) -> str:
    with urllib.request.urlopen("https://api.ashcon.app/mojang/v2/user/"+uname) as f:
        dat = json.load(f)
        return normalize_uuid(dat["uuid"])


def uuid_to_uname(uuid: str) -> str:
    with urllib.request.urlopen("https://api.ashcon.app/mojang/v2/user/"+uuid) as f:
        dat = json.load(f)
        return dat["username"]


def normalize_uuid(uuid: str) -> str:
    return str(UUID(uuid))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="Cape Manager",
            description="Manage SnR dev capes")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available actions")

    # Add subcommand
    add_parser = subparsers.add_parser("add", help="Add a cape to a user")
    add_parser.add_argument("identifier", metavar="username", help="The username of the user")
    add_parser.add_argument("-u", "--uuid", action="store_true",
                            help="Treat the identifier as a UUID")

    # Remove subcommand
    remove_parser = subparsers.add_parser("remove", help="Remove a cape from a user")
    remove_parser.add_argument("identifier", metavar="username", help="The username of the user")
    remove_parser.add_argument("-u", "--uuid", action="store_true",
                               help="Treat the identifier as a UUID")

    # Update subcommand
    update_parser = subparsers.add_parser("update", help="Update a user's username")
    update_parser.add_argument("identifier", nargs="?", metavar="username",
                               help="The username of the user")
    update_parser.add_argument("-u", "--uuid", action="store_true",
                               help="Treat the identifier as a UUID")

    # List subcommand
    list_parser = subparsers.add_parser("list", help="List users with capes")


    args = parser.parse_args(sys.argv[1:])

    with open("dev_capes.json") as f:
        full_data: dict[str, Any] = json.load(f)

    dev_capes: list[dict[str, str]] = full_data["dev"]

    write = True

    if args.command == "add":
        if args.uuid:
            uid = normalize_uuid(args.identifier)
            name = uuid_to_uname(uid)
            dev_capes.append({
                "id": uid,
                "name": name
            })
            print(f"Added cape to {name} ({uid})")
        else:
            uid = uname_to_uuid(args.identifier)
            name = args.identifier
            dev_capes.append({
                "id": uid,
                "name": name
            })
            print(f"Added cape to {name} ({uid})")
    elif args.command == "remove":
        if args.uuid:
            args.identifier = normalize_uuid(args.identifier)
            pre_len = len(dev_capes)
            dev_capes = [
                    v for v in dev_capes
                    if normalize_uuid(v["id"]) != args.identifier
            ]
            if pre_len == len(dev_capes):
                print(f"{args.identifier} didn't have a cape")
            else:
                print(f"Removed cape from {args.identifier}")
        else:
            pre_len = len(dev_capes)
            dev_capes = [
                    v for v in dev_capes
                    if v["name"] != args.identifier
            ]
            if pre_len == len(dev_capes):
                print(f"{args.identifier} didn't have a cape")
            else:
                print(f"Removed cape from {args.identifier}")
    elif args.command == "update":
        any = False
        for entry in dev_capes:
            if args.identifier:
                if args.uuid and normalize_uuid(entry["id"]) != normalize_uuid(args.identifer):
                    continue
                if not args.uuid and entry["name"] != args.identifier:
                    continue
            any = True
            print(f"Updating username for {entry['name']} ({entry['id']})")
            old_name = entry["name"]
            entry["name"] = uuid_to_uname(entry["name"])
            if entry["name"] == old_name:
                print("> Unchanged")
            else:
                print(f"> New username: {entry['name']}")
        if not any:
            print(f"Could not find user {args.identifier}")
    elif args.command == "list":
        write = False
        print("Cape holders:")
        for entry in dev_capes:
            print(f"\t[{entry['id']}] {entry['name']}")
    else:
        raise ValueError(f"Invalid command {args.command}")

    if write:
        dev_capes = sorted(dev_capes, key=lambda v: v["id"])

        full_data["dev"] = dev_capes

        with open("dev_capes.json", "w") as f:
            json.dump(full_data, f, indent=4)
