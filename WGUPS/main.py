# C950 - WGUPS
# Code By: Robert King
# Student ID: 011133982

# Import classes and data files
import Truck
from Package import Package
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
            hash_table.ht_insert(pack_id, pack)


# Method to determine distance between address x and y
def calculate_distance(x, y):
    distance = CSV_Distance[x][y]
    if distance == '':
        distance = CSV_Distance[y][x]

    return float(distance)


# Method to parse address number from full address string
def parse_address(address):
    for r in CSV_Address:
        if address in r[2]:
            return int(r[0])


# Create the 3 truck objects with default attributes based on assignment assumptions and supporting data
truck1 = Truck.Truck(16, 18, None,
                     [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=8))

truck2 = Truck.Truck(16, 18, None,
                     [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

truck3 = Truck.Truck(16, 18, None,
                     [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Create hash table and load in packages
hash_Table = CreateHashMap()
add_packages("CSV/WGUPS_Packages.csv", hash_Table)

