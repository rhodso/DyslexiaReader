import tkinter as tk
import os

class ContentDisplayApp:
    def __init__(self, config_file):
        self.config_file = config_file
        self.preferences = self.read_config()
        self.text_widget = None
        self.root = None

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

    # Function to set the content of the text widget
    def set_content(self, content):
        if self.text_widget:
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, content)
            self.text_widget.config(state=tk.DISABLED)
        else:
            self._initialize_ui(content)

    # Function to initialize the UI and display content
    def _initialize_ui(self, content):
        self.root = tk.Tk()
        self.root.title("Display Content")

        # Configure the text widget based on preferences
        self.text_widget = tk.Text(
            self.root,
            wrap=tk.WORD,
            bg=self.preferences["background_color"],
            fg=self.preferences["text_color"],
            font=(self.preferences["font"], self.preferences["font_size"])
        )
        self.text_widget.pack(expand=True, fill=tk.BOTH)

        # Insert content
        self.text_widget.insert(tk.END, content)
        self.text_widget.config(state=tk.DISABLED)

    # Function to run the application
    def run(self):
        if self.root:
            self.root.mainloop()

# Example usage
if __name__ == "__main__":
    app = ContentDisplayApp("config.txt")
    app.set_content("Here's some text")
    app.run()

