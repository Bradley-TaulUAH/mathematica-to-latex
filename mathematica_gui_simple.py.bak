"""
Mathematica to LaTeX/Markdown Converter - GUI Application
A user-friendly interface for converting Mathematica notebooks to LaTeX and Markdown
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from mathematica_converter import MathematicaConverter


class MathematicaConverterGUI:
    """GUI application for Mathematica to LaTeX/Markdown conversion"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mathematica to LaTeX/Markdown Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.output_format = tk.StringVar(value="both")
        
        # Initialize converter
        self.converter = MathematicaConverter()
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            title_frame, 
            text="Mathematica to LaTeX/Markdown Converter",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Main content frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # Input file selection
        input_label = ttk.Label(main_frame, text="Input Mathematica Notebook (.nb):")
        input_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_file, width=60)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        input_button = ttk.Button(input_frame, text="Browse...", command=self.browse_input)
        input_button.grid(row=0, column=1)
        
        # Output directory selection
        output_label = ttk.Label(main_frame, text="Output Directory:")
        output_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, width=60)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        output_button = ttk.Button(output_frame, text="Browse...", command=self.browse_output)
        output_button.grid(row=0, column=1)
        
        # Output format selection
        format_label = ttk.Label(main_frame, text="Output Format:")
        format_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=5, column=0, sticky=tk.W, pady=5)
        
        latex_radio = ttk.Radiobutton(
            format_frame, 
            text="LaTeX only", 
            variable=self.output_format, 
            value="latex"
        )
        latex_radio.grid(row=0, column=0, padx=5)
        
        markdown_radio = ttk.Radiobutton(
            format_frame, 
            text="Markdown only", 
            variable=self.output_format, 
            value="markdown"
        )
        markdown_radio.grid(row=0, column=1, padx=5)
        
        both_radio = ttk.Radiobutton(
            format_frame, 
            text="Both formats", 
            variable=self.output_format, 
            value="both"
        )
        both_radio.grid(row=0, column=2, padx=5)
        
        # Convert button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, pady=20)
        
        self.convert_button = ttk.Button(
            button_frame, 
            text="Convert", 
            command=self.convert,
            style="Accent.TButton"
        )
        self.convert_button.grid(row=0, column=0, padx=5)
        
        self.clear_button = ttk.Button(
            button_frame, 
            text="Clear", 
            command=self.clear_fields
        )
        self.clear_button.grid(row=0, column=1, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate', 
            length=300
        )
        self.progress.grid(row=7, column=0, pady=10)
        
        # Status/Output area
        status_label = ttk.Label(main_frame, text="Status:")
        status_label.grid(row=8, column=0, sticky=tk.W, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(
            main_frame, 
            height=12, 
            width=80,
            wrap=tk.WORD
        )
        self.status_text.grid(row=9, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(9, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Footer with help text
        footer_frame = ttk.Frame(self.root, padding="10")
        footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        help_text = "Select a Mathematica notebook file (.nb), choose output format, and click Convert."
        help_label = ttk.Label(footer_frame, text=help_text, foreground="gray")
        help_label.grid(row=0, column=0)
        
    def browse_input(self):
        """Open file dialog to select input notebook"""
        filename = filedialog.askopenfilename(
            title="Select Mathematica Notebook",
            filetypes=[
                ("Mathematica Notebooks", "*.nb"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-set output directory to same as input
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(filename))
    
    def browse_output(self):
        """Open directory dialog to select output directory"""
        directory = filedialog.askdirectory(
            title="Select Output Directory"
        )
        if directory:
            self.output_dir.set(directory)
    
    def log_message(self, message):
        """Add a message to the status text area"""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_status(self):
        """Clear the status text area"""
        self.status_text.delete(1.0, tk.END)
    
    def clear_fields(self):
        """Clear all input fields and status"""
        self.input_file.set("")
        self.output_dir.set("")
        self.output_format.set("both")
        self.clear_status()
    
    def validate_inputs(self):
        """Validate user inputs before conversion"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file.")
            return False
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Input file does not exist.")
            return False
        
        if not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output directory.")
            return False
        
        if not os.path.exists(self.output_dir.get()):
            try:
                os.makedirs(self.output_dir.get())
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create output directory: {e}")
                return False
        
        return True
    
    def convert(self):
        """Perform the conversion"""
        if not self.validate_inputs():
            return
        
        # Clear previous status
        self.clear_status()
        
        # Disable button and start progress
        self.convert_button.config(state='disabled')
        self.progress.start()
        
        # Run conversion in a separate thread
        thread = threading.Thread(target=self.perform_conversion)
        thread.daemon = True
        thread.start()
    
    def perform_conversion(self):
        """Perform the actual conversion (runs in separate thread)"""
        try:
            self.log_message("Starting conversion...")
            self.log_message(f"Input: {self.input_file.get()}")
            self.log_message(f"Output Directory: {self.output_dir.get()}")
            self.log_message(f"Format: {self.output_format.get()}")
            self.log_message("-" * 60)
            
            success, message = self.converter.convert_file(
                self.input_file.get(),
                self.output_format.get(),
                self.output_dir.get()
            )
            
            if success:
                self.log_message(message)
                self.log_message("-" * 60)
                self.log_message("✓ Conversion completed successfully!")
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success", 
                    "Conversion completed successfully!"
                ))
            else:
                self.log_message(f"✗ Error: {message}")
                self.root.after(0, lambda: messagebox.showerror("Error", message))
                
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            self.log_message(f"✗ {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            # Re-enable button and stop progress
            self.root.after(0, lambda: self.convert_button.config(state='normal'))
            self.root.after(0, self.progress.stop)


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = MathematicaConverterGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
