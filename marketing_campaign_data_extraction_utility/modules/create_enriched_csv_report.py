import csv
from modules import config


def create_enriched_csv(org_objects):
    # Create a list of dictionaries with consistent keys for CSV writing
    csv_data = []

    for entry in org_objects:
        if 'key_contacts' in entry:
            for contact in entry['key_contacts']:
                csv_entry = {
                    'LoanRange': entry['LoanRange'],
                    'BusinessName': entry['BusinessName'],
                    'Sum of JobsRetained': entry['Sum of JobsRetained'],
                    'Lender': entry['Lender'],
                    'org_id': entry['org_id'],
                    'key_contact_name': contact.get('key_contact_name', ''),
                    'key_contact_title': contact.get('key_contact_title', ''),
                    'key_contact_email': contact.get('key_contact_email', ''),
                    'key_contact_email_status': contact.get('key_contact_email_status', ''),
                    'key_contact_org_phone': contact.get('key_contact_org_phone', '')
                }
                csv_data.append(csv_entry)
        else:
            csv_entry = {
                'LoanRange': entry['LoanRange'],
                'BusinessName': entry['BusinessName'],
                'Sum of JobsRetained': entry['Sum of JobsRetained'],
                'Lender': entry['Lender'],
                'org_id': entry['org_id'],
                'key_contact_name': '',
                'key_contact_title': '',
                'key_contact_email': '',
                'key_contact_email_status': '',
                'key_contact_org_phone': ''
            }
            csv_data.append(csv_entry)

    # Define the file name for the CSV output
    csv_file = config.enriched_data_output_path

    # Define the field names for the CSV header
    fieldnames = ['LoanRange', 'BusinessName', 'Sum of JobsRetained', 'Lender', 'org_id', 'key_contact_name', 'key_contact_title', 'key_contact_email', 'key_contact_email_status', 'key_contact_org_phone']

    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data
        writer.writerows(csv_data)
    
    print("Data enriched with key contact information has been written to:")
    print(csv_file + "\n")