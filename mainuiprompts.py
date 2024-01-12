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

def region_table_prompts():
        print("\nMenu:")
        print("1. Select a single region number")
        print("2. Select a range of region numbers")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, 3): ")
        if choice == '1':
            region_number = input("Enter the region number: ")
            if dentalreport.validate_region_number(region_number):
                return region_number,0, True
            else:
                print("Invalid region number. Please enter a valid FDI teeth number (11-48).")
                image_path = 'pic4.png'
                img = Image.open(image_path)
                img.show()
        elif choice == '2':
            start_region = input("Enter the starting region number: ")
            end_region = input("Enter the ending region number: ")
            if dentalreport.validate_region_number(start_region) and dentalreport.validate_region_number(end_region):
                    return start_region, end_region, False
            else:
                    print("Invalid region number. Please enter a valid FDI teeth number (11-48).")
                    image_path = 'pic4.png'
                    img = Image.open(image_path)
                    img.show()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def prompt_num_of_implants():
    implants = input("Number of implants:")
    return int(implants)