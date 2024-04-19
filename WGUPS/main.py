# C950 - WGUPS
# Code By: Robert King
# Student ID: 011133982

# Import classes and data files
import Truck
from Package import Package
import CSV
from CreateHashTable import CreateHashMap

import csv
import datetime

# Obtain addresses
with open("CSV/WGUPS_Addresses.csv") as dataFile:
    CSV_Address = csv.reader(dataFile)
    CSV_AddressList = []
    for row in CSV_Address:
        CSV_AddressList.append(row)

# Obtain distances
with open("CSV/WGUPS_Distance.csv") as dataFile1:
    CSV_Distance = csv.reader(dataFile1)
    CSV_DistanceList = []
    for row in CSV_Distance:
        CSV_DistanceList.append(row)

# Obtain packages
with open("CSV/WGUPS_Packages.csv") as dataFile2:
    CSV_Packages = csv.reader(dataFile2)
    CSV_PackageList = []
    for row in CSV_Packages:
        CSV_PackageList.append(row)


# print(f'{CSV_Packages}') # Test package data import

# Method to create package objects from CSV file
def add_packages(filename, hash_table):
    with open(filename) as package_file:
        package_data = csv.reader(package_file)
        next(package_data) # Skip first line to remove header
        for package in package_data:  # Set attributes
            pack_id = package[0]
            pack_address = package[1]
            pack_city = package[2]
            pack_state = package[3]
            pack_zip = package[4]
            pack_deadline = package[5]
            pack_weight = package[6]
            pack_status = "At hub"

            # Use attribute variables to create new Package object
            pack = Package(pack_id, pack_address, pack_city, pack_state,
                           pack_zip, pack_deadline, pack_weight, pack_status)

            # Insert the package into the hash table
            hash_table.insert(pack_id, pack)


# Create hash table and load in packages
hash_Table = CreateHashMap()
add_packages("CSV/WGUPS_Packages.csv", hash_Table)

