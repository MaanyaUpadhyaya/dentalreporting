import tkinter as tk
from tkinter import filedialog
import dicomreader
import dentalreport
from PIL import Image

def select_patient_folder():
        confirm = input("\nSelect a patient folder? (yes/no): ").lower()
        if confirm == 'no' or confirm == 'n':
            print("Thank you for using Autofill Reports!!\n")
            exit()
        else:
            selected_folder = get_selected_folder()
            print("Selected Patient from:", selected_folder)
            return selected_folder

def get_selected_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path

def prompt_patient_folder():
    while True:
        selected_folder = select_patient_folder()
        patient_id = dicomreader.get_patient_id_from_folder(selected_folder)
        if patient_id == 'Null':
            print("Patient ID not found. Please select a different patient folder.")
        else:
            return selected_folder

def get_typeof_study():
    print("\nSelect type of study:")
    print("1. Regular study")
    print("2. Pterygoid study")
    choice = input("Enter your choice (1, 2): ")
    if choice != '1' and choice != '2':
        print("Invalid choice. Please enter 1, 2, or 3.")
        exit()
    is_pterygoid = choice == 2 
    return is_pterygoid

def region_table_prompts():
        print("\nMenu:")
        print("1. Select a single region number")
        print("2. Select a range of region numbers")
        print("3. Select multiple non-consecutive region numbers")
        choice = input("Enter your choice (1, 2, 3): ")
        image_path = 'regionmap.png'

        if choice == '1':
            region_number = input("Enter the region number: ")
            if dentalreport.validate_region_number(region_number):
                return [region_number]
            else:
                print("Invalid region number. Please enter a valid FDI teeth number (11-48).")
                img = Image.open(image_path)
                img.show()
        elif choice == '2':
            start_region = input("Enter the starting region number: ")
            end_region = input("Enter the ending region number: ")
            if dentalreport.validate_region_number(start_region) and dentalreport.validate_region_number(end_region):
                    return list(range(int(start_region), int(end_region)+1))
            else:
                    print("Invalid region number. Please enter a valid FDI teeth number (11-48).")
                    img = Image.open(image_path)
                    img.show()
        elif choice == '3':
            rn = input("Enter the multiple non-consecutive region numbers:")
            region_numbers = rn.split(',')
            region_numbers = list(filter(None, map(str.strip, region_numbers)))
            valid_regions = True
            for region in region_numbers:
                if not dentalreport.validate_region_number(region):
                    valid_regions = False
            if valid_regions:
                    return region_numbers
            else:
                    print("Invalid region number. Please enter a valid FDI teeth number (11-48).")
                    img = Image.open(image_path)
                    img.show()
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def prompt_num_of_implants():
    implants = input("Number of implants:")
    return int(implants)
