from software_package import SoftwarePackage
from archivist import archivist
import sys
import json
import os
import requests

def generate_token():

    try:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
    except:
        exit( "Error: Missing CLIENT_ID or CLIENT_SECRET.")

    print("Found Credentials")

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        
    }

    print("Generating Token")
    token_request = requests.post("https://app.rkvst.io/archivist/iam/v1/appidp/token", headers=headers, data=params).json()

    return token_request.get("access_token")
    


def main():

    command = sys.argv[1]
    asset_id = sys.argv[2]
    try:
            authtoken = generate_token()
    except:
        exit(
            "ERROR: Auth token not found. Please check your CLIENT_ID and AUTH_TOKEN."
        )

    print("Token Generated")
    
    arch = archivist.Archivist(
        "https://app.rkvst.io",
        auth=authtoken,
        )
    
    package = SoftwarePackage(arch)

    package.read(asset_id)

    print("Doing" + command)
    
    match command:

        case 'release':
            attrs=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            latest_sbom=json.loads(sys.argv[6])
            custom_asset_attrs=json.loads(sys.argv[7])
            package.release(attrs, attachments=attachments, custom_attrs=custom_attrs, latest_sbom=latest_sbom, custom_asset_attrs=custom_asset_attrs)
            return("Release Complete")

        case 'release_plan':
            attrs=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            package.release_plan(attrs, attachments=attachments, custom_attrs=custom_attrs)
            return("Release Plan Complete")
        
        case 'release_accepted':
            attrs=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            package.release_accepted(attrs, attachments=attachments, custom_attrs=custom_attrs)
            return("Release Accepted Complete")

        case 'patch':
            attrs=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            package.patch(attrs, attachments=attachments, custom_attrs=custom_attrs)
            return("Patch Complete")

        case 'private_patch':
            attrs=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            package.private_patch(attrs, attachments=attachments, custom_attrs=custom_attrs)
            return("Private Patch Complete")
        
        case 'vuln_disclosure':
            attrs=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            package.vuln_disclosure(attrs, attachments=attachments, custom_attrs=custom_attrs)
            return("Vulnerability Disclosure Complete")

        case 'vuln_update':
            attrs=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            package.vuln_update(attrs, attachments=attachments, custom_attrs=custom_attrs)
            return("Vulnerability Update Complete")

        case 'deprecation':
            attrs=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            package.deprecation(attrs, attachments=attachments, custom_attrs=custom_attrs)
            return("Deprecation Complete")

if __name__ == "__main__":
    main()
    