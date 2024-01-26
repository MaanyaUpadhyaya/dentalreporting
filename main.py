import os
import sys
import mainuiprompts
import imageprocess
import dentalreport
import mainuiprompts
import dicomreader
from docxtpl import DocxTemplate
import argparse


if len(sys.argv) != 1:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='selected_folder', help='folder name')
    parser.add_argument('-rn', dest='region_numbers', help='region numbers')
    parser.add_argument('-im', dest='num_of_implants', help='virtual implant number')
    parser.add_argument('-pt', dest='is_pterygoid', help='Study type: \n1. Regular \n2.Pterygoid')
    parser.add_argument('-rt', dest='report_type', help='Report type: \n1. Select a single region number \n2. Select a range of region numbers \n3. Select multiple non-consecutive region numbers')
    args = parser.parse_args()

    selected_folder = args.selected_folder
    report_type = int(args.report_type)
    is_pterygoid = args.is_pterygoid == '2'
    num_of_implants = args.num_of_implants
    print(f'Selected Folder: {selected_folder}')
    print(f'UserInput Region Numbers: {args.region_numbers}')
    print(f'Number of Implants: {num_of_implants}')
    region_numbers = mainuiprompts.parse_region_numbers(report_type, args.region_numbers, is_pterygoid)
    print(f'Reporting Region Numbers: {region_numbers}')

else:
    selected_folder = mainuiprompts.prompt_patient_folder()
    print("\nPlease enter following details:")

    is_pterygoid = mainuiprompts.get_typeof_study()
    region_numbers = mainuiprompts.region_table_prompts(is_pterygoid)
    num_of_implants = mainuiprompts.prompt_num_of_implants()

ds, attributes = dentalreport.get_dcm_attriutes(selected_folder)

pixel_spacing = ds.get('PixelSpacing', 'Null')
pixels = int(pixel_spacing[1] * 1000)

quadrant, region_name = dentalreport.get_quadrant_and_region(region_numbers,is_pterygoid)
print(f"\nThe selected tooth is in the Quadrant: {quadrant} Region: {region_name}")

attributes['RegionName'] = region_name
attributes['date_now'] = dentalreport.get_current_date()
attributes['PatientAge'] = dentalreport.find_patient_age(attributes['PatientBirthDate'])
attributes['PixelSpacing'] = pixels 


mapping = dentalreport.allocate_indices(is_pterygoid)

attributes = dentalreport.initial_mapping(attributes,mapping)
attributes = dentalreport.get_mapping_singles(attributes, region_numbers, is_pterygoid)

attributes = dentalreport.virtual_implant_table(attributes, num_of_implants)
        
images = imageprocess.find_panoramic_view_image(selected_folder)

template_file = 'report_template.docx' 
         
filename = dicomreader.get_patinet_name(ds)
report_filename = f"{filename}_{dentalreport.get_current_datetime()}.docx"
folder = "./reports/"
report_filepath = os.path.join(folder, report_filename)
        
template = DocxTemplate(template_file)

dentalreport.render_save_report(template,attributes,images,report_filepath)

print("\nSuccessfully generated report!!")
print("\tAt:reports")
print("\tAs:", report_filename)
print()

