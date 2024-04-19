# C950 - WGUPS
# Code By: Robert King
# Student ID: 011133982
import csv

# Import classes and data files
import Truck
import Package
import CSV
import datetime
from CreateHashTable import CreateHashMap

# Obtain addresses
with open("CSV/WGUPS_Addresses.csv") as dataFile:
    CSV_Address = csv.reader(dataFile)
    CSV_Address = list(CSV_Address)

# Obtain distances
with open("CSV/WGUPS_Distance.csv") as dataFile1:
    CSV_Distance = csv.reader(dataFile1)
    CSV_Distance = list(CSV_Distance)

# Obtain packages
with open("CSV/WGUPS_Packages.csv") as dataFile2:
    CSV_Packages = csv.reader(dataFile2)
    CSV_Packages = list(CSV_Packages)

# print(f'{CSV_Packages}') # Test package data import
