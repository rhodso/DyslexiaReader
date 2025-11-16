import tkinter as tk
from tkinter import filedialog, messagebox
import os
from display_content import ContentDisplayApp
from pdf_reader import PDFReader

class PDFPreferencesApp:
    def __init__(self, _root, config_file="config.txt"):
        self.root = _root
        self.config_file = config_file
        self.preferences = self.read_config()
        self.selected_pdf_path = None
        self.setup_ui()

    # Function to read preferences from the config file
    def read_config(self):
        local_preferences = {
            "background_color": "#FBFF69",
            "text_color": "#000000",
            "font_size": 12,
            "font": "Arial"
        }
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as file:
                for line in file:
                    key, value = line.strip().split("=", 1)
                    if key in local_preferences:
                        local_preferences[key] = value if key in ["background_color", "text_color", "font"] else int(value)
        return local_preferences

    # Function to save preferences to the config file
    def save_config(self):
        with open(self.config_file, "w", encoding="utf-8") as file:
            for key, value in self.preferences.items():
                file.write(f"{key}={value}\n")

    # Function to open file dialog and select a PDF file
    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.selected_pdf_path = file_path
            pdf_name = os.path.basename(file_path)  # Extract just the file name
            self.pdf_label.config(text=f"Selected: {pdf_name}")
        else:
            self.selected_pdf_path = None
            self.pdf_label.config(text="No file selected")

    # Function to update the status label
    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")
        self.root.update_idletasks()

    # Function to handle the "Go" button click
    def on_go(self):
        # Save preferences to the config file
        self.preferences["background_color"] = self.bg_color_var.get()
        self.preferences["text_color"] = self.text_color_var.get()
        self.preferences["font_size"] = self.font_size_var.get()
        self.preferences["font"] = self.font_var.get()

        self.save_config()

        # Check if a PDF file is selected
        if not self.selected_pdf_path:
            messagebox.showerror("Error", "No PDF file selected.")
            return

        # Update status to "Reading PDF"
        self.update_status("Reading PDF")

        # Read the content of the PDF
        try:
            reader = PDFReader()
            pdf_content = reader.read_pdf(self.selected_pdf_path)
        except FileNotFoundError as e:
            self.update_status("Ready")
            messagebox.showerror("Error", str(e))
            return
        except Exception as e:
            self.update_status("Ready")
            messagebox.showerror("Error", f"Failed to read the PDF: {e}")
            return

        # Update status to "Formatting output"
        self.update_status("Formatting output")

        # Display the content using the ContentDisplayApp
        display_app = ContentDisplayApp(self.config_file)
        display_app.set_content(pdf_content)
        
		# Update status back to "Ready"
        self.update_status("Ready")
        
        display_app.run()

    # Function to set up the UI
    def setup_ui(self):
        # PDF selection
        pdf_frame = tk.Frame(self.root)
        pdf_frame.pack(pady=10)
        select_pdf_button = tk.Button(pdf_frame, text="Select PDF", command=self.select_pdf)
        select_pdf_button.pack()
        self.pdf_label = tk.Label(pdf_frame, text="No file selected")
        self.pdf_label.pack()

        # Preferences configuration
        preferences_frame = tk.Frame(self.root)
        preferences_frame.pack(pady=10)

        tk.Label(preferences_frame, text="Background Color:").grid(row=0, column=0, sticky="e")
        self.bg_color_var = tk.StringVar(value=self.preferences["background_color"])
        bg_color_entry = tk.Entry(preferences_frame, textvariable=self.bg_color_var)
        bg_color_entry.grid(row=0, column=1)

        tk.Label(preferences_frame, text="Text Color:").grid(row=1, column=0, sticky="e")
        self.text_color_var = tk.StringVar(value=self.preferences["text_color"])
        text_color_entry = tk.Entry(preferences_frame, textvariable=self.text_color_var)
        text_color_entry.grid(row=1, column=1)

        tk.Label(preferences_frame, text="Font Size:").grid(row=2, column=0, sticky="e")
        self.font_size_var = tk.IntVar(value=self.preferences["font_size"])
        font_size_spinbox = tk.Spinbox(preferences_frame, from_=8, to=72, textvariable=self.font_size_var)
        font_size_spinbox.grid(row=2, column=1)

        tk.Label(preferences_frame, text="Font:").grid(row=3, column=0, sticky="e")
        self.font_var = tk.StringVar(value=self.preferences["font"])
        font_entry = tk.Entry(preferences_frame, textvariable=self.font_var)
        font_entry.grid(row=3, column=1)

        # Go button
        go_button = tk.Button(self.root, text="Go", command=self.on_go)
        go_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Ready")
        self.status_label.pack(pady=5)

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    root.title("NatReader")
    app = PDFPreferencesApp(root, "config.txt")
    root.mainloop()

