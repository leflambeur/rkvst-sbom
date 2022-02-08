import json
import os
import argparse

from software_package import SoftwarePackage
from archivist.archivist import Archivist

def loadJSON(jsonInput):
    try:
        validJSON = json.loads(jsonInput)
    except ValueError:
        raise(f'Invalid JSON {jsonInput}')
    return validJSON

def getCommand(package, command):
    try:
        found_command = getattr(package, command)
        return found_command
    except AttributeError:
        raise(f"Can't find {command} in SoftwarePackage")

def main():

    parser = argparse.ArgumentParser(description='RKVST SBOM CLI Tool')

    parser.add_argument('--url', '-u', default='https://app.rkvst.io', help='URL to upload to')
    parser.add_argument('--assetID', '-id', help='The Asset ID being submitted to')
    parser.add_argument('--command', '-cmd', nargs=1, default='release', choices=['create', 'release', 'release_plan', 
        'release_accepted', 'patch', 'private_patch', 
        'vuln_disclosure', 'vuln_update', 'vuln_report', 
        'deprecation'], help='The type of event being submitted')
    parser.add_argument('--requiredAttributes', '-req', help='Required Event Attributes JSON')
    parser.add_argument('--customEvent', '-evt', help='Custom Event Attributes JSON')
    parser.add_argument('--latestSBOM', '-sbom', help='Latest SBOM Attributes JSON')
    parser.add_argument('--customAsset', '-asset', help='Custom Asset Attributes JSON')
    parser.add_argument('--client_id', '-c', help='Specify Application CLIENT_ID inline')
    parser.add_argument('--client_secret', '-s', help='Specify Application CLIENT_SECRET inline')
    parser.add_argument('attachments', metavar='<attachments>', nargs='+', help='file to be uploaded')

    args = parser.parse_args()
    
    for envopt in 'client_id client_secret'.split():
        if getattr(args, envopt) is None:
            try:
                setattr(args, envopt, os.environ[f"SBOM_{envopt.upper()}"])
            except KeyError:
                print(f"use --{envopt} or set SBOM_{envopt.upper()} as an envvar")

    arch = Archivist(
        args.url,
        (args.client_id, args.client_secret),
    )

    package = SoftwarePackage(arch)

    for command in args.command:
        print("Doing " + command)
        attrs = loadJSON(args.requiredAttributes)
        attachments = args.attachments
        custom_attrs = loadJSON(args.customEvent)
        if command == 'release':
            asset_id = args.assetID
            package.read(asset_id)
            latest_sbom=loadJSON(args.latestSBOM)
            custom_asset_attrs=loadJSON(args.customAsset)
            command = getCommand(package, command)
            event = command(attrs=attrs, attachments=attachments, custom_attrs=custom_attrs, latest_sbom=latest_sbom, custom_asset_attrs=custom_asset_attrs)
            print("Release Complete\n\n" + str(event))
        elif command == 'create':
            custom_asset_attrs=loadJSON(args.customAsset)
            command = getCommand(package, command)
            event = command(attrs=attrs, attachments=attachments, custom_attrs=custom_attrs)
            print("Create Complete\n\n" + str(event))
        else:
            asset_id = args.assetID
            package.read(asset_id)
            command = getCommand(package, command)
            event = command(attrs=attrs, attachments=attachments, custom_attrs=custom_attrs)
            print("Event Complete\n\n" + str(event))

if __name__ == "__main__":
    main()