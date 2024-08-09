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
with open("CSV/WGUPS_Addresses.csv") as addressFile:
    CSV_Address = csv.reader(addressFile)
    CSV_AddressList = []
    next(CSV_Address)
    for row in CSV_Address:
        CSV_AddressList.append(row)

# Obtain distances
with open("CSV/WGUPS_Distance.csv") as distanceFile:
    CSV_Distance = csv.reader(distanceFile)
    CSV_DistanceList = []
    next(CSV_Distance)
    for row in CSV_Distance:
        CSV_DistanceList.append(row)

# Obtain packages
with open("CSV/WGUPS_Packages.csv") as packageFile:
    CSV_Packages = csv.reader(packageFile)
    CSV_PackageList = []
    next(CSV_Packages)
    for row in CSV_Packages:
        CSV_PackageList.append(row)


# Method to create package objects from CSV file
def add_packages(filename, hash_table):
    with open(filename) as package_file:
        package_data = csv.reader(package_file)
        next(package_data)  # Skip first line to remove header
        for package in package_data:  # Set attributes
            pack_id = int(package[0])
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


# Method to get address ID number
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
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


# Sort the packages using the truck objects created previously
assign_packages(truck1)
assign_packages(truck2)
truck3.depart_time = min(truck1.time, truck2.time)
assign_packages(truck3)
totalMiles = truck1.totalMiles + truck2.totalMiles + truck3.totalMiles


# Main class displays user interface in console
def main():
    # Display welcome message and menu
    print("WGU Parcel Tracking Service:")
    ans = True  # Stores user menu choice
    while ans:
        print("""
            1. Print status of all packages and total miles
            2. Print status of individual package at a specific time
            3. Print status of all packages at a specific time 
            4. Exit
            """)
        ans = input("Enter the number representing your choice(1-4): ")
        if ans == "1":
            # Print combined miles and every package that will be delivered
            print(f'WGUPS trucks have {totalMiles:.1f} miles on their combined routes today.')
            print(f'Truck 1 has {truck1.totalMiles:.1f} miles.')
            print(f'Truck 2 has {truck2.totalMiles:.1f} miles.')
            print(f'Truck 3 has {truck3.totalMiles:.1f} miles.')
            print("All packages scheduled today: ")
            for packageID in range(1, 41):
                package = hash_Table.ht_search(packageID)

                if package.ID in truck1.packages:
                    package.truck = 'Truck 1'

                elif package.ID in truck2.packages:
                    package.truck = 'Truck 2'

                elif package.ID in truck3.packages:
                    package.truck = 'Truck 3'

                print(str(package))

            ans = False

        elif ans == "2":
            # Take as input a time and package number and display the information
            ans_2 = True
            while ans_2:
                try:
                    user_time = input("Using the format HH:MM:SS, please enter a time: ")
                    user_package = input("Please enter a package number: ")
                    (h, m, s) = user_time.split(":")
                    format_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    package = hash_Table.ht_search(int(user_package))
                    package.get_status(format_time)

                    # Check if time is passed 10:30 and update package 9's incorrect address
                    if format_time >= datetime.timedelta(hours=10, minutes=20, seconds=0):
                        package.address = '410 S. State St.'
                        package.city = 'Salt Lake City'
                        package.state = 'Utah'
                        package.zipcode = '84111'

                    if package.ID in truck1.packages:
                        package.truck = 'Truck 1'

                    elif package.ID in truck2.packages:
                        package.truck = 'Truck 2'

                    elif package.ID in truck3.packages:
                        package.truck = 'Truck 3'

                    print(str(package))
                    ans_2 = False

                except ValueError:
                    print("One or both values were not valid. Please try again: ")
                    ans_2 = True

            ans = False

        elif ans == "3":
            # Take as input a time and display information for all packages
            ans_3 = True
            while ans_3:
                try:
                    user_time = input("Using the format HH:MM:SS, please enter a time: ")
                    (h, m, s) = user_time.split(":")
                    format_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    for packageID in range(1, 41):
                        package = hash_Table.ht_search(packageID)
                        package.get_status(format_time)

                        # Check if time is passed 10:30 and update package 9's incorrect address
                        if format_time >= datetime.timedelta(hours=10, minutes=20, seconds=0) and packageID == 9:
                            package.address = '410 S. State St.'
                            package.city = 'Salt Lake City'
                            package.state = 'Utah'
                            package.zipcode = '84111'

                        if package.ID in truck1.packages:
                            package.truck = 'Truck 1'

                        elif package.ID in truck2.packages:
                            package.truck = 'Truck 2'

                        elif package.ID in truck3.packages:
                            package.truck = 'Truck 3'

                        print(str(package))
                    ans_3 = False
                except ValueError:
                    print("Invalid time entered. Please try again: ")
                    ans_3 = True
            ans = False

        elif ans == "4":
            ans = False

        elif ans != "":
            print("\n Not a valid option. Please choose an option 1-4.")


if __name__ == "__main__":
    main()
