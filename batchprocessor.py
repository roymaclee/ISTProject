import os
import json
import csv
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

# ------------------------------
# File Conversion Functions
# ------------------------------

def csv_to_json(input_file, output_file):
    """Convert CSV to JSON"""
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            data = list(reader)

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    except Exception as e:
        raise RuntimeError(f"Error converting CSV to JSON: {e}")


def json_to_csv(input_file, output_file):
    """Convert JSON to CSV"""
    try:
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)

    except Exception as e:
        raise RuntimeError(f"Error converting JSON to CSV: {e}")


def csv_to_xml(input_file, output_file):
    """Convert CSV to XML"""
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            data = list(reader)

        root = ET.Element("rows")
        for row in data:
            row_elem = ET.SubElement(root, "row")
            for cell_value in row:
                cell_elem = ET.SubElement(row_elem, "cell")
                cell_elem.text = cell_value if cell_value is not None else ""

        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

    except Exception as e:
        raise RuntimeError(f"Error converting CSV to XML: {e}")


def xml_to_csv(input_file, output_file):
    """Convert XML to CSV"""
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()

        data = []
        for row_elem in root.findall("row"):
            row_data = [cell_elem.text if cell_elem.text else "" for cell_elem in row_elem.findall("cell")]
            data.append(row_data)

        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)

    except Exception as e:
        raise RuntimeError(f"Error converting XML to CSV: {e}")


def xml_to_json(input_file, output_file):
    """Convert XML to JSON"""
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()

        def xml_to_dict(element):
            return {
                "tag": element.tag,
                "attributes": dict(element.attrib),
                "text": element.text if element.text else "",
                "children": [xml_to_dict(child) for child in element]
            }

        data_dict = xml_to_dict(root)

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, indent=4)

    except Exception as e:
        raise RuntimeError(f"Error converting XML to JSON: {e}")


def json_to_xml(input_file, output_file):
    """Convert JSON to XML"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        def dict_to_xml(d):
            elem = ET.Element(d["tag"], d["attributes"])
            elem.text = d["text"]
            for child_dict in d.get("children", []):
                child_elem = dict_to_xml(child_dict)
                elem.append(child_elem)
            return elem

        root_elem = dict_to_xml(data)
        tree = ET.ElementTree(root_elem)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

    except Exception as e:
        raise RuntimeError(f"Error converting JSON to XML: {e}")


# ------------------------------
# Process Conversion
# ------------------------------

def process_conversion(input_file, output_format):
    """Determine the appropriate conversion function based on file extension"""
    file_ext = os.path.splitext(input_file)[1].lower()
    output_file = os.path.splitext(input_file)[0] + f".{output_format.lower()}"

    try:
        if file_ext == ".csv":
            if output_format.lower() == "json":
                csv_to_json(input_file, output_file)
            elif output_format.lower() == "xml":
                csv_to_xml(input_file, output_file)
        elif file_ext == ".json":
            if output_format.lower() == "csv":
                json_to_csv(input_file, output_file)
            elif output_format.lower() == "xml":
                json_to_xml(input_file, output_file)
        elif file_ext == ".xml":
            if output_format.lower() == "csv":
                xml_to_csv(input_file, output_file)
            elif output_format.lower() == "json":
                xml_to_json(input_file, output_file)
        else:
            raise ValueError("Unsupported file format")

        return output_file

    except Exception as e:
        raise RuntimeError(f"Conversion failed: {e}")


# ------------------------------
# Batch Processing
# ------------------------------

def batch_process(folder_path, output_format):
    """Process multiple files in batch with concurrent execution"""
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.csv', '.json', '.xml'))]

    if not files:
        raise ValueError("No compatible files found in the folder.")

    results = []
    with ThreadPoolExecutor() as executor:
        for file in files:
            results.append(executor.submit(process_conversion, file, output_format))

    return [res.result() for res in results if res.result() is not None]
