import json
import requests
from modules import config


def get_fields_from_apollo(selected_organization_ids, org_objects):

    payload = json.dumps({
        "api_key": config.apollo_auth_token,
        "organization_ids" : selected_organization_ids,
        "person_seniorities": config.seniority_level,
        "per_page": "100"
    })

    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
    }

    response = requests.request("POST", 'https://api.apollo.io/v1/mixed_people/search', headers=headers, data=payload).json()

    # For every person returned, match their organization_id with the org_objects's org_id and add them as a key contact.
    for person in response["people"]:
        org_id_from_response = person.get("organization_id", None)

        for org in org_objects:
            if org.get("org_id") == org_id_from_response:
                # Check if the organization_id exists in org_objects
                if "key_contacts" not in org:
                    org["key_contacts"] = []

                key_contact = {
                    "key_contact_name": person.get("name", {}),
                    "key_contact_title": person.get("title", {}),
                    "key_contact_email": person.get("email", {}),
                    "key_contact_email_status": person.get("email_status", {}),
                    "key_contact_org_phone": person.get("organization", {}).get("primary_phone", {}).get("number", {})
                }

                org["key_contacts"].append(key_contact)