import os
import sys
from datetime import datetime
from modules import config, get_org_objects, get_organization_ids, get_key_contact_fields, create_enriched_csv_report


# Record the start time
start_time = datetime.now()
print(f"Process start time: {start_time}")

# Set parent directory
script_path = os.path.abspath(__file__)
dir_path = os.path.dirname(script_path)

# Run this if executing from cx_Freeze binary. Get source csv path.
if os.path.isfile(dir_path + '/../' + config.org_source_csv):
    input_path = dir_path + '/../' + config.org_source_csv
    print("Input file found:" + input_path)
    
#Run this if executing from python interpreter. Get source csv path.
elif os.path.isfile(dir_path + '/' + config.org_source_csv):
    input_path = dir_path + '/' + config.org_source_csv
    print("Input file found:" + input_path)

else:
    print("Input file not found. Please check the name of the file in env_config.yaml")
    os.system('pause')
    sys.exit()

# Get all fields from each org in source csv
print('getting list of Organizations...')
org_objects = get_org_objects.get_org_objects(input_path)

# Create a list to store selected organization IDs
selected_organization_ids = []

# For each organization found in source csv, get the Apollo organization ids to use for contacts lookup.
for org_object in org_objects:
    get_organization_ids.enrich_with_org_id(org_object, selected_organization_ids)

# Lookup the key contact information and add it to organizations found in the source csv.
get_key_contact_fields.get_fields_from_apollo(selected_organization_ids, org_objects)

# Create a new organizations csv that's enriched with contact information.
create_enriched_csv_report.create_enriched_csv(org_objects)

end_time = datetime.now()
total_run_time = end_time - start_time
print(f"Process started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Process finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total run time: {total_run_time}")
input("Press any key to exit...")