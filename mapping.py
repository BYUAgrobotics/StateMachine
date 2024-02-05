#Mapping.py - finds the path to the USB and uploads the output files (initial and final mapping) to it

# Questions: should be we validating/checking that our initial and final flower and leaf counts are correct?

# Notes:
# healthy after = healthy before
# unhealthy after = 0
# flowers after = 1

import csv
import os

def find_usb_drives():
    # List all drives under /media/pi
    usb_drives = [f"/media/pi/{d}" for d in os.listdir("/media/pi")]

    # Filter out non-existent drives
    usb_drives = [drive for drive in usb_drives if os.path.exists(drive)]
    
    return usb_drives

def get_output(plant_list, txt_file_name):
    
    # Find USB drives
    # usb_drives = find_usb_drives()

    # Print the found USB drives
    # if usb_drives:
    #     print("USB Drives:")
    #     for usb_drive in usb_drives:
    #         print(usb_drive)
    # else:
    #     print("Failed to export files. No USB drives found.")
    #     return

    # Specify the output file to go to the USB
    #usb_drive_path = usb_drives[0] # grabs the first USB in the list --> replace here for testing
    
    usb_drive_path = "C:/Users/Avary/Documents/BYU Winter 2024/Agricultural Robotics" # TESTING CODE
    
    txt_file_path = f"{usb_drive_path}/{txt_file_name}"

    # Constructing Output
    column_headers = ["Plant Number", "Healthy", "Unhealthy", "Flowers"]
    data = [column_headers] + plant_list

    # Write data to UTF-8 encoded plain text file with spaces after commas
    with open(txt_file_path, mode='w', encoding='utf-8') as file:
        for row in data:
            line = ', '.join(map(str, row))  # Join elements with commas and spaces
            file.write(line + '\n')

    #Success statement
    print(f"T{txt_file_name}'created successfully.")

# Plant Data Example
initial_plant_list = [["Plant A1", 5, 2, 1], ["Plant A2", 7, 3, 2]] #filler code, this is the format that it should be in
final_plant_list =[["Plant A1", 5, 0, 1], ["Plant A2", 7, 0, 1]] #filler code 

get_output(initial_plant_list, "Initial_Mapping_BYU.txt")
get_output(final_plant_list, "Final_Mapping_BYU.txt")
