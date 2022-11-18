# This script will take the output file and update an Airtable base with any URLs that are missing
from os.path import exists
from pyairtable import Table
from pyairtable.formulas import match
import csv

def load_env(order):
    settings = {}

    if exists('.env'):   
        with open('.env', "r") as f:
            for line in f:
                key, value = line.split("=")
                settings[key] = value.strip()

    ordered_settings = []
    for key in order:
        if not key in settings:
            settings[key] = input(f"Enter {key}: ")

        ordered_settings.append(settings[key])

    with open('.env', 'w') as f:
        for key in settings:
            f.write(f"{key}={settings[key]}\n")

    return ordered_settings

AIRTABLE_BASE, AIRTABLE_API_KEY, AIRTABLE_TABLE_NAME = load_env(['AIRTABLE_BASE', 'AIRTABLE_API_KEY', 'AIRTABLE_TABLE_NAME'])
INPUT_FILE="output/jobs.csv"

print("Starting Airtable Update")

table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE, AIRTABLE_TABLE_NAME)
print("Connected to Airtable")

print("Processing CSV..")
updated = 0
skipped = 0
with open(INPUT_FILE) as f:
    csvreader = csv.reader(f)
    header = next(csvreader)
    for row in csvreader:
        title, salary, location, link = row
        existing = table.first(formula=match({"URL": link}))
        if not existing:
            table.insert({"URL": link, "Title": title, "Rate": salary, "Region": location})
            updated = updated + 1
            print("Saved new record")
        else:
            skipped = skipped + 1
            print("Skipped existing record")

print(f"All done. Added {updated} records and skipped {skipped} existing records")