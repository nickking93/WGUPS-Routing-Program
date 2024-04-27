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
    next(CSV_Address)
    for row in CSV_Address:
        CSV_AddressList.append(row)

# Obtain distances
with open("CSV/WGUPS_Distance.csv") as dataFile1:
    CSV_Distance = csv.reader(dataFile1)
    CSV_DistanceList = []
    next(CSV_Distance)
    for row in CSV_Distance:
        CSV_DistanceList.append(row)

# Obtain packages
with open("CSV/WGUPS_Packages.csv") as dataFile2:
    CSV_Packages = csv.reader(dataFile2)
    CSV_PackageList = []
    next(CSV_Packages)
    for row in CSV_Packages:
        CSV_PackageList.append(row)


# print(f'{CSV_Packages}') # Test package data import

# Method to create package objects from CSV file
def add_packages(filename, hash_table):
    with open(filename) as package_file:
        package_data = csv.reader(package_file)
        next(package_data)  # Skip first line to remove header
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
    distance = CSV_DistanceList[x][y]
    if distance == '':
        distance = CSV_DistanceList[y][x]

    return float(distance)


# Method to parse address number from full address string
def get_address_id(address):
    for r in CSV_AddressList:
        if address in r[2]:
            return int(r[0])


# Create the 3 truck objects with default attributes based on assignment assumptions and package special notes
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


# Method to assign trucks with packages using nearest neighbor
def assign_packages(truck):
    unsorted = []

    # Move packages into a list of unsorted packages to sort and assign them
    for idNum in truck.packages:
        package = hash_Table.ht_search(idNum)
        unsorted.append(package)
    truck.packages.clear()

    # Find nearest package to truck and insert back into truck's package array
    while len(unsorted) > 0:
        destination = 2000
        next_package = None

        # Check the distance between truck and each package and determine next package
        for package in unsorted:
            if calculate_distance(get_address_id(truck.address), get_address_id(package.address)) <= destination:
                destination = calculate_distance(get_address_id(truck.address), get_address_id(package.address))
                next_package = package

        # Assign next package to truck and remove from unsorted list
        truck.packages.append(next_package.ID)
        unsorted.remove(next_package)

        truck.totalMiles += destination  # Add mileage from each truck to the trucks total mileage
        truck.address = next_package.address  # Update trucks starting location to package location in each iteration

        # Update time for truck and next package
        truck.time += datetime.timedelta(hours=destination / 18)
        destination.delivery_time = truck.time
        destination.departure_time = truck.depart_time


# Sort the packages using the truck objects created previously
# assign_packages(truck1)
# assign_packages(truck2)
# truck3.depart_time = min(truck1.time, truck2.time)
# assign_packages(truck3)

# Main class displays user interface in console
def main():
    # print(CSV_AddressList)
    # print(CSV_PackageList)
    # print(CSV_DistanceList)

    # Display welcome message and menu
    print("WGU Parcel Service:")
    ans = True  # Stores user menu choice
    while ans:
        print("""
            1. Print status of all packages and total miles
            2. Print status of individual package at a specific time
            3. Print status of all packages at a specific time 
            4. Exit
            """)
        ans = input("Choose an option 1-4: ")
        if ans == "1":
            # TODO write code to print all packages and all miles by all trucks
            ans = False

        elif ans == "2":
            # TODO write code to print a single package at a given time.
            ans = False

        elif ans == "3":
            # TODO write code to print all packages at a given time.
            ans = False

        elif ans == "4":
            ans = False

        elif ans != "":
            print("\n Not a valid option. Please choose an option 1-4.")


if __name__ == "__main__":
    # main()
    pass
