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

    print("Doing " + command)
     
    match command:

        case 'release':
            sbom=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            latest_sbom=json.loads(sys.argv[6])
            custom_asset_attrs=json.loads(sys.argv[7])
            release = package.release(sbom=sbom, attachments=attachments, custom_attrs=custom_attrs, latest_sbom=latest_sbom, custom_asset_attrs=custom_asset_attrs)
            print("Release Complete\n\n" + str(release))

        case 'release_plan':
            sbom_planned=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            release_plan = package.release_plan(sbom_planned=sbom_planned, attachments=attachments, custom_attrs=custom_attrs)
            print("Release Plan Complete\n\n" + str(release_plan))
        
        case 'release_accepted':
            sbom_accepted=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            release_accepted = package.release_accepted(sbom_accepted=sbom_accepted, attachments=attachments, custom_attrs=custom_attrs)
            print("Release Accepted Complete\n\n" + str(release_accepted))

        case 'patch':
            sbom_patch=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            patch = package.patch(sbom_patch=sbom_patch, attachments=attachments, custom_attrs=custom_attrs)
            print("Patch Complete\n\n" + str(patch))

        case 'private_patch':
            sbom_patch=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            private_patch = package.private_patch(sbom_patch=sbom_patch, attachments=attachments, custom_attrs=custom_attrs)
            print("Private Patch Complete\n\n" + str(private_patch))
        
        case 'vuln_disclosure':
            vuln=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            vuln_disclosure = package.vuln_disclosure(vuln=vuln, attachments=attachments, custom_attrs=custom_attrs)
            print("Vulnerability Disclosure Complete\n\n" + str(vuln_disclosure))

        case 'vuln_update':
            vuln=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            vuln_update = package.vuln_update(vuln=vuln, attachments=attachments, custom_attrs=custom_attrs)
            print("Vulnerability Update Complete\n\n" + str(vuln_update))

        case 'deprecation':
            sbom_eol=json.loads(sys.argv[3])
            attachments=json.loads(sys.argv[4])
            custom_attrs=json.loads(sys.argv[5])
            deprecation = package.deprecation(sbom_eol=sbom_eol, attachments=attachments, custom_attrs=custom_attrs)
            print("Deprecation Complete\n\n" + str(deprecation))

if __name__ == "__main__":
    main()