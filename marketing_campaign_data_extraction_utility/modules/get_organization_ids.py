import json
import requests
from modules import config


def enrich_with_org_id(org_object, selected_organization_ids):

    org_name = org_object['BusinessName']

    # Do the initial lookup with the business name in the source CSV. If there is a valid response from Apollo,
    # get the count of companies returned from the search result.
    org_id_lookup_response = lookup_org_id(org_name)
    organizations_count = org_id_lookup_response["pagination"]["total_entries"]
    organizations = org_id_lookup_response["organizations"]

    # If a single company count is returned, extract that company's organization id, append it to the 
    # selected_organization_ids list, and add it as a value for a new org_id key in the org_object dict.
    if organizations_count == 1:
        selected_organization_ids.append(organizations[0]["id"])
        org_object.update({"org_id": organizations[0]["id"]})
        print(f"Selected organization: {org_name} added to list\n")

    # If more than one company count is returned, list out all the results and prompt the user.
    elif organizations_count > 1:
        print(f"Searching for {org_name} resulted in the following results:")

        # Loop through the companies returned from Apollo and display them as a numbered list.
        for i, org in enumerate(organizations):
            print(f"{i + 1}. {org['name']} - [website: {org['website_url']}]")

        print("0. Manual entry\n")

        # Give the user the option to enter a manual entry if the correct company is not listed.
        # Also give the user the option to skip searching for this company in case it does not exist in Apollo.
        choice = input("Enter the number for the correct company, enter 0 for manual entry, or hit ENTER to skip: ")

        # Get the user's selection or manual entry to get the organization id, append it to the 
        # selected_organization_ids list, and add it as a value for a new org_id key in the org_object dict.
        get_company_from_list(choice, organizations, org_object, selected_organization_ids)
        
    # If a 0 company count is returned, prompt for manual entry 
    else:
        print(f"Searching for {org_name} did not provide any results.")
        choice = "0"
        get_company_from_list(choice, organizations, org_object, selected_organization_ids)


def get_company_from_list(choice, organizations, org_object, selected_organization_ids):

    while True:

        # Check if the user entered a number.
        if choice.isdigit():
            index = int(choice) - 1

            # If 0 was entered, prompt for manual entry.
            if index == -1:
                manually_entered_org_name = input("Manually enter the organization name: ")

                # If input is not empty do another lookup in Apollo with the entered value
                if manually_entered_org_name:
                    response = lookup_org_id(manually_entered_org_name)

                    # Get the count of companies returned.
                    organizations_count = response["pagination"]["total_entries"]
                    organizations = response["organizations"]

                    # If a single company count is returned, extract that company's organization id and append
                    # it to the selected_organization_ids list and add it as a value for a new org_id key in the org_object dict.
                    if organizations_count == 1:
                        selected_organization_id = organizations[0]["id"]
                        selected_organization_ids.append(selected_organization_id)
                        org_object.update({"org_id": organizations[0]["id"]})
                        print(f"Selected organization: {manually_entered_org_name} added to list\n")
                        break 
                    
                    # If multiple companies are returned, list the results, 
                    # return to the beginning of the loop and prompt the user again.
                    elif organizations_count > 1:
                        for i, org in enumerate(organizations):
                            print(f"{i + 1}. {org['name']} - [website: {org['website_url']}]")

                        print("0. Manual entry\n")

                        choice = input("Enter the number for the correct company, enter 0 for manual entry, or hit ENTER to skip: ")
                        continue

                    else:
                        print(f"No results found for '{manually_entered_org_name}'.\n")
                        choice = input("Enter 0 to try again, or hit ENTER to skip: ")
                        continue

                else:
                    print("Manual entry cannot be empty.")
                    choice = input("Enter 0 to try again, or hit ENTER to skip: ")
                    continue

            # If the user entered a valid number listed, then append that company's organization id
            # to the selected_organization_ids list and also add it as a value to a new org_id key in the org_object dict. 
            elif 0 <= index < len(organizations):
                selected_organization_id = organizations[index]["id"]
                selected_organization_ids.append(selected_organization_id)
                org_object.update({"org_id": organizations[index]["id"]})
                print(f"Selected organization: {organizations[index]['name']} added to list\n")
                break
            
            # If the user entered an invalid number.
            else:
                print("Invalid selection. Please choose a valid number, enter 0 for manual entry, or hit ENTER to skip: ")
                for i, org in enumerate(organizations):
                    print(f"{i + 1}. {org['name']} - [website: {org['website_url']}]")

                print("0. Manual entry")
                print("ENTER key to skip")

                choice = input("Enter the number for the correct company, enter 0 for manual entry, or hit ENTER to skip: ")
                continue

        # If the user hit ENTER or any other non numerical key to skip, 
        # do not append anything to the selected_organization_ids list,
        # but add a new org_id key to the org_object dict with a 0 value       
        else:
            print("Skipping organization selection.")
            org_object.update({"org_id": "0"})
            break


def lookup_org_id(org_name):

    headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
    }

    payload = json.dumps({
        "api_key": config.apollo_auth_token,
        "q_organization_name" : org_name,
        "per_page": "100"
    })

    response = requests.request("POST", 'https://api.apollo.io/v1/mixed_companies/search', headers=headers, data=payload).json()

    return response