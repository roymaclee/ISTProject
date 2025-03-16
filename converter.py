import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import xml.etree.ElementTree as ET
import json


# ------------------------------
# CSV <-> XML Functions
# ------------------------------
def csv_to_xml():
    """Convert a CSV file to an XML file."""
    # Ask the user to select a CSV file
    csv_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV Files", "*.csv")]
    )
    if csv_path:
        try:
            # Read the CSV as a list of lists
            with open(csv_path, 'r', newline='', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                data = list(reader)

            # Ask the user where to save the XML file
            xml_path = filedialog.asksaveasfilename(
                defaultextension=".xml",
                title="Save XML file",
                filetypes=[("XML Files", "*.xml")]
            )
            if xml_path:
                # Create an XML tree: <rows> with <row> and <cell> children
                root = ET.Element("rows")
                for row in data:
                    row_elem = ET.SubElement(root, "row")
                    for cell_value in row:
                        cell_elem = ET.SubElement(row_elem, "cell")
                        # cell_value might be None or empty; set text accordingly
                        cell_elem.text = cell_value if cell_value is not None else ""

                # Write the XML file with a declaration
                tree = ET.ElementTree(root)
                tree.write(xml_path, encoding="utf-8", xml_declaration=True)

                messagebox.showinfo("Success", f"CSV successfully converted to XML:\n{xml_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


def xml_to_csv():
    """Convert an XML file (in the expected format) back to a CSV file."""
    # Ask the user to select an XML file
    xml_path = filedialog.askopenfilename(
        title="Select XML file",
        filetypes=[("XML Files", "*.xml")]
    )
    if xml_path:
        try:
            # Parse the XML file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Gather the data in a list of lists
            data = []
            # Expecting structure: <rows><row><cell>...</cell>...</row>...</rows>
            for row_elem in root.findall("row"):
                row_data = []
                for cell_elem in row_elem.findall("cell"):
                    row_data.append(cell_elem.text if cell_elem.text else "")
                data.append(row_data)

            # Ask where to save the CSV
            csv_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                title="Save CSV file",
                filetypes=[("CSV Files", "*.csv")]
            )
            if csv_path:
                # Write the CSV file
                with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(data)

                messagebox.showinfo("Success", f"XML successfully converted to CSV:\n{csv_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


# ------------------------------
# CSV <-> JSON Functions
# ------------------------------
def csv_to_json():
    # Ask the user to select a CSV file
    csv_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV Files", "*.csv")]
    )
    if csv_path:
        try:
            # Read the CSV file as a list of lists
            with open(csv_path, 'r', newline='', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                data = list(reader)  # each element is a list of cells in a row

            # Ask where to save the JSON file
            json_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                title="Save JSON file",
                filetypes=[("JSON Files", "*.json")]
            )
            if json_path:
                # Write the list of lists to JSON
                with open(json_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, indent=4)

                messagebox.showinfo("Success", f"CSV successfully converted to JSON:\n{json_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


def json_to_csv():
    # Ask the user to select a JSON file
    json_path = filedialog.askopenfilename(
        title="Select JSON file",
        filetypes=[("JSON Files", "*.json")]
    )
    if json_path:
        try:
            # Read the JSON file
            with open(json_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            # Check if the JSON is a list of lists (CSV format)...
            if isinstance(data, list) and all(isinstance(row, list) for row in data):
                rows = data
            # ...or if it is a nested dictionary (from XML conversion)
            elif isinstance(data, dict) and data.get("tag") == "rows":
                rows = []
                for row_dict in data.get("children", []):
                    if row_dict.get("tag") == "row":
                        row = []
                        for cell in row_dict.get("children", []):
                            if cell.get("tag") == "cell":
                                row.append(cell.get("text", ""))
                        rows.append(row)
            else:
                messagebox.showerror("Error", "JSON must contain a list of lists or a nested XML structure.")
                return

            # Ask where to save the CSV file
            csv_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                title="Save CSV file",
                filetypes=[("CSV Files", "*.csv")]
            )
            if csv_path:
                # Write the rows back to CSV
                with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(rows)

                messagebox.showinfo("Success", f"JSON successfully converted to CSV:\n{csv_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


# ------------------------------
# XML <-> JSON Functions
# ------------------------------
def xml_to_dict(element):
    """
    Recursively convert an ElementTree Element into a dictionary.
    The returned dictionary has the keys:
      - "tag": element's tag name
      - "attributes": dictionary of element's attributes
      - "text": element's text content (empty string if None)
      - "children": list of dictionaries for each child
    """
    d = {
        "tag": element.tag,
        "attributes": dict(element.attrib),
        "text": element.text if element.text else "",
        "children": []
    }
    for child in element:
        d["children"].append(xml_to_dict(child))
    return d


def dict_to_xml(d):
    """
    Reconstruct an ElementTree Element from a dictionary of the form:
      {
        "tag": "tag_name",
        "attributes": { ... },
        "text": "some text",
        "children": [ {...}, {...}, ... ]
      }
    """
    elem = ET.Element(d["tag"], d["attributes"])
    elem.text = d["text"]
    for child_dict in d["children"]:
        child_elem = dict_to_xml(child_dict)
        elem.append(child_elem)
    return elem


def xml_to_json():
    """Convert an XML file to a JSON file (nested dictionaries)."""
    # Ask the user to select an XML file
    xml_path = filedialog.askopenfilename(
        title="Select XML file",
        filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
    )
    if xml_path:
        try:
            # Parse the XML
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Convert the root Element to a dictionary
            data_dict = xml_to_dict(root)

            # Ask user where to save the JSON file
            json_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                title="Save JSON file",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
            )
            if json_path:
                # Write the dictionary to JSON
                with open(json_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data_dict, json_file, indent=4)

                messagebox.showinfo("Success", f"XML successfully converted to JSON:\n{json_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


def json_to_xml():
    """Convert a JSON file (nested dictionaries or list-of-lists) back to XML."""
    # Ask the user to select a JSON file
    json_path = filedialog.askopenfilename(
        title="Select JSON file",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if json_path:
        try:
            # Load the JSON data
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check if data is a nested dictionary (from xml_to_json)
            if isinstance(data, dict) and "tag" in data:
                root_elem = dict_to_xml(data)
            # Or if it's a list-of-lists (from csv_to_json)
            elif isinstance(data, list) and all(isinstance(row, list) for row in data):
                root_elem = ET.Element("rows")
                for row in data:
                    row_elem = ET.SubElement(root_elem, "row")
                    for cell in row:
                        cell_elem = ET.SubElement(row_elem, "cell")
                        cell_elem.text = cell if cell is not None else ""
            else:
                messagebox.showerror("Error", "JSON format not recognized for XML conversion.")
                return

            # Ask user where to save the XML file
            xml_path = filedialog.asksaveasfilename(
                defaultextension=".xml",
                title="Save XML file",
                filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
            )
            if xml_path:
                tree = ET.ElementTree(root_elem)
                tree.write(xml_path, encoding="utf-8", xml_declaration=True)
                messagebox.showinfo("Success", f"JSON successfully converted to XML:\n{xml_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")


# ------------------------------
# Main UI
# ------------------------------
def main():
    root = tk.Tk()
    root.title("File Converter")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    # CSV <-> XML Buttons
    btn_csv_to_xml = tk.Button(frame, text="CSV to XML", command=csv_to_xml, width=20, height=2)
    btn_csv_to_xml.grid(row=0, column=0, padx=5, pady=5)

    btn_xml_to_csv = tk.Button(frame, text="XML to CSV", command=xml_to_csv, width=20, height=2)
    btn_xml_to_csv.grid(row=0, column=1, padx=5, pady=5)

    # CSV <-> JSON Buttons
    btn_csv_to_json = tk.Button(frame, text="CSV to JSON", command=csv_to_json, width=20, height=2)
    btn_csv_to_json.grid(row=1, column=0, padx=5, pady=5)

    btn_json_to_csv = tk.Button(frame, text="JSON to CSV", command=json_to_csv, width=20, height=2)
    btn_json_to_csv.grid(row=1, column=1, padx=5, pady=5)

    # XML <-> JSON Buttons
    btn_xml_to_json = tk.Button(frame, text="XML to JSON", command=xml_to_json, width=20, height=2)
    btn_xml_to_json.grid(row=2, column=0, padx=5, pady=5)

    btn_json_to_xml = tk.Button(frame, text="JSON to XML", command=json_to_xml, width=20, height=2)
    btn_json_to_xml.grid(row=2, column=1, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()

