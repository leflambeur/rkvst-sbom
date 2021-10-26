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
    token_request = requests.post("https://dev-serhiy-0-avid.scratch-7.dev.wild.jitsuin.io/archivist/iam/v1/appidp/token", headers=headers, data=params).json()

    return token_request.get("access_token")



def main():

    command = sys.argv[1]
    asset_id = sys.argv[2]
    try:
            authtoken = "eyJhbGciOiJSUzI1NiIsImtpZCI6InN0dW50aWRwIiwidHlwIjoiSldUIn0.eyJhdWQiOiJzdHVudC1pZHAiLCJlbWFpbCI6InN0dW50LWlkcEBqaXRzdWluLmNvbSIsImV4cCI6MTY2Njc5ODgxOCwiaWF0IjoxNjM1MjYyODE4LCJpc3MiOiJzdHVudC1pZHBAaml0c3Vpbi5jb20iLCJqaXRfdGllciI6IlBSRU1JVU0iLCJuYW1lIjoic3R1bnQtaWRwQGppdHN1aW4uY29tIiwic3ViIjoic3R1bnQtaWRwQGppdHN1aW4uY29tIn0.MT5xZcK1grk4HW1-gzwoqysyndl5kOfGU_vU3WcBSTufod4yi7bsUM4lbrNEypUYOeNsE0MH_OOrb4xuX8HEF39RnkMqRfInAZvKBmF6JsLTtlllxyYKY6QNbcxntmZdkkTMiE6zBj3qEuU1YVHzyXUEp4q9Gw0ge-zqd6R_zfgxbC--zE0t9BYek2orWRvy_wbW71F2JjFEizxZAHbh9RG_u-N0oxdybsTp36-cRCYgRgCZ7tvTLgMJyFgSGIPHL04k6y0YiJ4Y6xBql7NyHJ8SjF-8gIU5QSCpmKZh8SgsT925yG6D_Vmx5Ij7lbadX0UVCAw4w2Ptj_bZ8Gn3WRUiYP8bjaM66UQaboND3OEfNDPcCD7Ar5UjY5RGCWNyt5-zXtaQel21bDvVY3kj0OqB7iOYkibdGkSc3r9F0ZUZR9oezoVIL4bgmMoN8ZTC-5p7H3tn4YWxoREiv-FVtgygMiVQsU5zy_zNJ5rxGma5y1pKApmn10mFe8ZR_8IM5HCIVNjJkghNeA6PwBQACyK1PJTkYjYcK2Mmhmnt1G6exJkbvljB5Snw6_YS7GXtsI0YCQXlyXzj8ZqDmFTAYZXRtpp6USNd3I0XmbA7m6DDGOtsJQDPUAZVoOZEs-9tdlqm34qEyh8o9_t_bKetPZ8aXDUO06qrCTvPhy-nAbA"


    except:
        exit(
            "ERROR: Auth token not found. Please check your CLIENT_ID and AUTH_TOKEN."
        )

    print("Token Generated")
    
    arch = archivist.Archivist(
        "https://dev-serhiy-0-avid.scratch-7.dev.wild.jitsuin.io",
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
