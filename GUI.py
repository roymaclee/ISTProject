import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor
import threading
import batchprocessor  # Import the updated batch processor module

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter")
        self.root.geometry("600x400")

        # File Selection
        self.input_label = ttk.Label(root, text="Select Input File:")
        self.input_label.pack(pady=5)

        self.input_entry = ttk.Entry(root, width=60)
        self.input_entry.pack()

        self.browse_button = ttk.Button(root, text="Browse", command=self.select_input_file)
        self.browse_button.pack(pady=5)

        # Format Selection
        self.format_label = ttk.Label(root, text="Select Output Format:")
        self.format_label.pack(pady=5)

        self.format_var = tk.StringVar(value="JSON")
        self.format_menu = ttk.Combobox(root, textvariable=self.format_var, values=["CSV", "JSON", "XML"])
        self.format_menu.pack()

        # Convert Button
        self.convert_button = ttk.Button(root, text="Convert", command=self.start_conversion)
        self.convert_button.pack(pady=10)

        # Batch Processing Button
        self.batch_button = ttk.Button(root, text="Batch Convert (Folder)", command=self.batch_convert)
        self.batch_button.pack(pady=5)

        # Progress Bar
        self.progress_label = ttk.Label(root, text="")
        self.progress_label.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack()

    def select_input_file(self):
        file_path = filedialog.askopenfilename()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)

    def start_conversion(self):
        """Start file conversion in a separate thread."""
        threading.Thread(target=self.convert_file, daemon=True).start()

    def convert_file(self):
        """Convert a single file format."""
        input_path = self.input_entry.get()
        output_format = self.format_var.get()

        if not input_path:
            messagebox.showerror("Error", "Please select an input file.")
            return

        try:
            output_path = batchprocessor.process_conversion(input_path, output_format)
            messagebox.showinfo("Success", f"File converted successfully: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

    def batch_convert(self):
        """Start batch conversion in a separate thread."""
        threading.Thread(target=self.batch_process, daemon=True).start()

    def batch_process(self):
        """Process multiple files in batch with progress bar."""
        folder_path = filedialog.askdirectory()
        output_format = self.format_var.get()

        if not folder_path:
            messagebox.showerror("Error", "Please select a folder.")
            return

        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.csv', '.json', '.xml'))]

        if not files:
            messagebox.showerror("Error", "No compatible files found in the folder.")
            return

        self.progress_label.config(text="Batch Conversion in Progress...")
        self.progress["value"] = 0
        self.progress["maximum"] = len(files)

        with ThreadPoolExecutor() as executor:
            for file in files:
                executor.submit(batchprocessor.process_conversion, file, output_format)
                self.progress["value"] += 1
                self.root.update_idletasks()

        self.progress_label.config(text="Batch Conversion Completed!")
        messagebox.showinfo("Success", "Batch conversion completed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()
