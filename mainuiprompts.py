import tkinter as tk
from tkinter import filedialog
import dicomreader
import dentalreport
from PIL import Image

def parse_region_numbers(report_type, rn, is_pterygoid):
    try:
        if report_type == 1:
            rn = [int(rn)]
        elif report_type == 2:
            region_nums = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
            if is_pterygoid:
                region_nums.insert(0, 19)
                region_nums.insert(17, 29)
            start_index = region_nums.index(int(rn[0]))
            end_index = region_nums.index(int(rn[1]))
            rn = region_nums[start_index:end_index + 1] 
        else:
            rn = list(filter(None, map(str.strip, rn.split(','))))
            rn = [int(num) for num in rn]
    except ValueError:
        print("Invalid input. Please provide valid region numbers.")
    return rn


def valid_choice(choice, max_choice):
    if choice.isdigit():
        choice = int(choice)
        return choice in list(range(1, max_choice+1))
    return False

def select_patient_folder():
        confirm = input("\nSelect a patient folder? (yes/no): ").lower()
        selected_folder = get_selected_folder()
        if confirm == 'no' or confirm == 'n':
            print("Thank you for using Autofill Reports!!\n")
            exit()
        elif selected_folder == "":
            print("No folder selected. Please select a patient folder.")
            exit()
        elif dicomreader.get_dicom_file(selected_folder) == None:
            print("This folder has no dicom file.Please select another folder.")
            exit()
        else:
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
        print("Invalid choice. Please enter 1 or 2")
        exit()
    is_pterygoid = choice == '2'
    return is_pterygoid

def region_table_prompts(is_pterygoid):
    print("\nMenu:")
    print("1. Select a single region number")
    print("2. Select a range of region numbers")
    print("3. Select non-consecutive region numbers")
    choice = input("Enter your choice (1, 2, 3): ")
    choice = int(choice) if valid_choice(choice, 3) else None
    if not choice:
        print("Invalid choice. Please enter 1, 2, or 3.")
        exit()
    region_numbers = None
    if choice == 1:
        region_numbers = input("Enter the region number: ")
    elif choice == 2:
        start_region = input("Enter the starting region number: ")
        end_region = input("Enter the ending region number: ")
        region_numbers = [start_region, end_region]
    else:
        region_numbers = input("Enter the multiple non-consecutive region numbers:")
       
    region_numbers = parse_region_numbers(choice, region_numbers,is_pterygoid)
    if region_numbers == "":
        exit()    
    else:
        all_valid = all(dentalreport.validate_region_number(region,is_pterygoid) for region in region_numbers)
        if not all_valid:
                print("Invalid region numbers. Please enter a valid FDI teeth number.")
                image_path = 'regionmap.png'
                img = Image.open(image_path)
                img.show()
                exit()
        return region_numbers
        

def prompt_num_of_implants():
    implants = input("Number of implants:")
    return int(implants)
