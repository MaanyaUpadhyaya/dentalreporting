import pydicom
from datetime import datetime
from docxtpl import InlineImage
from docx.shared import RGBColor
from docxtpl import DocxTemplate
import json
import numpy as np

from docx.shared import RGBColor
import dicomreader

def validate_region_number(region_number):
    valid_region_numbers = [
        '11', '12', '13', '14', '15', '16', '17', '18',
        '21', '22', '23', '24', '25', '26', '27', '28',
        '31', '32', '33', '34', '35', '36', '37', '38', 
        '41', '42', '43', '44', '45', '46', '47', '48'
    ]
    return region_number in valid_region_numbers

def get_quadrant_and_region(region_number):
    quadrant = int((int(region_number) - 1) / 8) + 1
    region_names = {
        '11': 'Upper right third molar',
        '12': 'Upper right second molar',
        '13': 'Upper right first molar',
        '14': 'Upper right second premolar',
        '15': 'Upper right first premolar',
        '16': 'Upper right canine',
        '17': 'Upper right lateral incisor',
        '18': 'Upper right central incisor',
        '21': 'Lower left third molar',
        '22': 'Lower left second molar',
        '23': 'Lower left first molar',
        '24': 'Lower left second premolar',
        '25': 'Lower left first premolar',
        '26': 'Lower left canine',
        '27': 'Lower left lateral incisor',
        '28': 'Lower left central incisor',
        '41': 'Lower right central incisor',
        '42': 'Lower right lateral incisor',
        '43': 'Lower right canine',
        '44': 'Lower right first premolar',
        '45': 'Lower right second premolar',
        '46': 'Lower right first molar',
        '47': 'Lower right second molar',
        '48': 'Lower right third molar',
    }
    region_name = region_names.get(region_number, 'Null')
    return quadrant, region_name

def get_dcm_attriutes(folder):
    dcm_file = dicomreader.get_dicom_file(folder)
    json_file = 'middle.json'  

    with open(json_file) as f:
        json_data = json.load(f)

    attribute_tags = json_data['content']
    attributes = dicomreader.read_dcm_attributes(dcm_file, attribute_tags)
    ds = pydicom.read_file(dcm_file)
    return ds, attributes

def find_patient_age(dob):
    if len(dob) != 8:
        return "Invalid date format"
    year = int(dob[:4])
    month = int(dob[4:6])
    day = int(dob[6:])
    today = datetime.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

slice_mapping = {
    18: 9,
    17: 9,
    16: 9,
    15: 5,
    14: 5,
    13: 5,
    12: 4,
    11: 4,
    21: 4,
    22: 4,
    23: 5,
    24: 5,
    25: 5,
    26: 9,
    27: 9,
    28: 9,
}
def allocate_indices(rn):
    region_number = int(rn)
    if region_number not in slice_mapping:
        return None 
    output_mapping = {}
    current_index = 1
    regions = list(slice_mapping.keys())
    region_index = 0
    for i in range(region_index, len(slice_mapping)):
        region = regions[i]
        output_mapping[region] = (current_index, current_index + slice_mapping[region] - 1)
        current_index += slice_mapping[region]
    return output_mapping

def get_mapping_range(attributes, region_number):
    n = 1
    default_mapping = allocate_indices(region_number)
    regions = list(default_mapping.keys())
    start_index = regions.index(int(region_number))
    for i in range(start_index,len(regions)) :
            region  = regions[i]
            attributes = begin_end_mapping(attributes,n,region,default_mapping)
            n = n+1
    return attributes

def get_mapping_single(attributes, region_number):
    default_mapping = allocate_indices(region_number)
    region_number = int(region_number) if not isinstance(region_number, int) else region_number
    if region_number in default_mapping:
        attributes = begin_end_mapping(attributes,1,region_number,default_mapping)
    return attributes

def initial_mapping(attributes, mapping):
    for region_number in mapping:
        current = mapping[region_number]
        if isinstance(current, tuple):
            attributes['r'+str(region_number) + '_begin'] = str(current[0])
            attributes['r'+str(region_number) + '_end'] = str(current[1])
    return attributes

def begin_end_mapping(attributes, n, region_number,mapping):
    current = mapping[region_number]
    if isinstance(current, tuple):
        attributes['region_r'+str(n)] = region_number
        attributes['r'+str(n) + '_begin'] = str(current[0])
        attributes['r'+str(n) + '_end'] = str(current[1])
    return attributes

def virtual_implant_table(attributes, num_implants):
    virtual_implant_table = [{"V" + str(i): f"V{i}" for i in range(1, num_implants+1)}]
    attributes['implants'] = virtual_implant_table
    attributes['num_implants'] = num_implants
    return attributes

def render_save_report(template,attributes, report_filepath):
    to_fill_in = {'img_pan':'panaroma.jpg'}
    for key, value in to_fill_in.items():
        image = InlineImage(template, value)
        attributes[key] = image
    template.render(attributes) 
    template.save(report_filepath)

