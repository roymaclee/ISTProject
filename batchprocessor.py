import csv
import json
import xml.etree.ElementTree as ET
import os
from concurrent.futures import ThreadPoolExecutor

def csv_to_xml(input_path, output_path):
    try:
        with open(input_path, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            data = list(reader)
        root = ET.Element("rows")
        for row in data:
            row_elem = ET.SubElement(root, "row")
            for cell_value in row:
                cell_elem = ET.SubElement(row_elem, "cell")
                cell_elem.text = cell_value if cell_value else ""
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        print(f"Error converting {input_path} to XML: {e}")

def xml_to_csv(input_path, output_path):
    try:
        tree = ET.parse(input_path)
        root = tree.getroot()
        data = [[cell.text if cell.text else "" for cell in row.findall("cell")] for row in root.findall("row")]
        with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)
    except Exception as e:
        print(f"Error converting {input_path} to CSV: {e}")

def csv_to_json(input_path, output_path):
    try:
        with open(input_path, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            data = list(reader)
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error converting {input_path} to JSON: {e}")

def json_to_csv(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)
    except Exception as e:
        print(f"Error converting {input_path} to CSV: {e}")

def xml_to_json(input_path, output_path):
    try:
        tree = ET.parse(input_path)
        root = tree.getroot()
        data = {"rows": [[cell.text for cell in row.findall("cell")] for row in root.findall("row")]}
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error converting {input_path} to JSON: {e}")

def json_to_xml(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        root = ET.Element("rows")
        for row in data["rows"]:
            row_elem = ET.SubElement(root, "row")
            for cell in row:
                cell_elem = ET.SubElement(row_elem, "cell")
                cell_elem.text = cell if cell else ""
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        print(f"Error converting {input_path} to XML: {e}")

def batch_convert(folder_path, output_format):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.csv', '.json', '.xml'))]
    if not files:
        print("No valid files found for conversion.")
        return
    with ThreadPoolExecutor() as executor:
        for file in files:
            output_file = os.path.splitext(file)[0] + f".{output_format.lower()}"
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext == ".csv" and output_format == "XML":
                executor.submit(csv_to_xml, file, output_file)
            elif file_ext == ".csv" and output_format == "JSON":
                executor.submit(csv_to_json, file, output_file)
            elif file_ext == ".json" and output_format == "CSV":
                executor.submit(json_to_csv, file, output_file)
            elif file_ext == ".json" and output_format == "XML":
                executor.submit(json_to_xml, file, output_file)
            elif file_ext == ".xml" and output_format == "CSV":
                executor.submit(xml_to_csv, file, output_file)
            elif file_ext == ".xml" and output_format == "JSON":
                executor.submit(xml_to_json, file, output_file)
    print("Batch conversion completed.")
