import csv

# Read from the source csv and store the contents in a dictionary
def get_org_objects(input_path):

    with open(input_path, mode='r', encoding="utf-8-sig", newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        org_list = list(reader)

    return org_list