import json
import os
import argparse

from software_package import SoftwarePackage
from archivist.archivist import Archivist

def loadJSON(jsonInput):
    try:
        validJSON = json.loads(jsonInput)
    except ValueError:
        exit(
            'Invalid JSON'
        )
    return validJSON

def main():

    parser = argparse.ArgumentParser(description='RKVST SBOM CLI Tool')

    parser.add_argument('--url', '-u', default='https://app.rkvst.io', help='URL to upload to')
    parser.add_argument('--assetID', '-id', nargs=1, help='The Asset ID being submitted to')
    parser.add_argument('--command', '-cmd', nargs=1, default='release', help='The type of event being submitted')
    parser.add_argument('--requiredAttributes', '-req', help='Required Event Attributes JSON')
    parser.add_argument('--customEvent', '-evt', help='Custom Event Attributes JSON')
    parser.add_argument('--latestSBOM', '-sbom', help='Latest SBOM Attributes JSON')
    parser.add_argument('--customAsset', '-asset', help='Custom Asset Attributes JSON')
    parser.add_argument('attachments', metavar='<sbom-file>', nargs='+', help='SBOM to be uploaded')

    client_group = parser.add_mutually_exclusive_group(required=True)
    client_group.add_argument('--clientId', '-c', nargs=1, help='Specify Application CLIENT_ID inline')
    client_group.add_argument('--envClientId', '-i', action='store_true',  help='Specify if your Application CLIENT_ID is an Env Var')

    secret_group = parser.add_mutually_exclusive_group(required=True)
    secret_group.add_argument('--secret', '-s', nargs=1, help='Specify Application SECRET inline')
    secret_group.add_argument('--envSecret', '-e', action='store_true',  help='Specify if your Application SECRET is an Env Var')

    args = parser.parse_args()

    command_options = ['release', 'release_plan', 
        'release_accepted', 'patch', 'private_patch', 
        'vuln_disclosure', 'vuln_update', 'vuln_report', 
        'deprecation']

    command = args.command
    
    if args.envClientId == True:
        client_id = os.getenv("CLIENT_ID")
        if client_id is None:
            exit(
                "ERROR: CLIENT_ID EnvVar not found"
            )
    else:
        client_id = args.clientId

    if args.envSecret == True:
        client_secret= os.getenv("SECRET")
        if client_secret is None:
            exit(
                "ERROR: SECRET EnvVar not found"
            )
    else:
        client_secret = args.secret

    rkvst_url = args.url

    arch = Archivist(
        rkvst_url,
        (client_id, client_secret),
    )

    asset_id = args.assetID

    package = SoftwarePackage(arch)

    package.read(asset_id)

    print("Doing " + command)

    for command in command_options:
        attrs=loadJSON(args.requiredAttributes)
        attachments=loadJSON(args.attachments)
        custom_attrs=loadJSON(args.customEvent)
        if command == 'release':
            latest_sbom=loadJSON(args.latestSBOM)
            custom_asset_attrs=loadJSON(args.customAsset)
            release = package.command(attrs=attrs, attachments=attachments, custom_attrs=custom_attrs, latest_sbom=latest_sbom, custom_asset_attrs=custom_asset_attrs)
            print("Release Complete\n\n" + str(release))
        else:
            event = package.command(attrs=attrs, attachments=attachments, custom_attrs=custom_attrs)
            print("Event Complete\n\n" + str(event))
    else:
        exit(
            'Invalid Command'
            )

if __name__ == "__main__":
    main()