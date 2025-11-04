"""
Mathematica to LaTeX Converter - GUI Application
A user-friendly interface for converting Mathematica notebooks to LaTeX with advanced features
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
import mathematica_to_latex


class MathematicaConverterGUI:
    """GUI application for Mathematica to LaTeX conversion"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mathematica to LaTeX Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.display_mode = tk.StringVar(value="both")
        self.auto_extract_graphics = tk.BooleanVar(value=False)
        
        # Create UI
        self.create_widgets()
        
        # Check for Wolfram Engine
        self.check_wolfram()
        
    def check_wolfram(self):
        """Check if Wolfram Engine is available"""
        if mathematica_to_latex.check_wolfram_engine():
            self.log_message("✓ Wolfram Engine detected - auto graphics extraction available")
        else:
            self.log_message("ⓘ Wolfram Engine not found - graphics will use placeholders")
            self.graphics_check.config(state='disabled')
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            title_frame, 
            text="Mathematica to LaTeX Converter",
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
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_file, width=70)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        input_button = ttk.Button(input_frame, text="Browse...", command=self.browse_input)
        input_button.grid(row=0, column=1)
        
        # Output directory selection
        output_label = ttk.Label(main_frame, text="Output Directory:")
        output_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, width=70)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        output_button = ttk.Button(output_frame, text="Browse...", command=self.browse_output)
        output_button.grid(row=0, column=1)
        
        # Display mode selection
        mode_label = ttk.Label(main_frame, text="Display Mode:")
        mode_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=5, column=0, sticky=tk.W, pady=5)
        
        mode_input = ttk.Radiobutton(
            mode_frame, 
            text="Input Cells Only (Code)", 
            variable=self.display_mode, 
            value="input-only"
        )
        mode_input.grid(row=0, column=0, padx=5)
        
        mode_output = ttk.Radiobutton(
            mode_frame, 
            text="Output Cells Only (Results)", 
            variable=self.display_mode, 
            value="output-only"
        )
        mode_output.grid(row=0, column=1, padx=5)
        
        mode_both = ttk.Radiobutton(
            mode_frame, 
            text="Input & Output Cells (Code + Results)", 
            variable=self.display_mode, 
            value="both"
        )
        mode_both.grid(row=0, column=2, padx=5)
        
        # Graphics extraction option
        graphics_frame = ttk.Frame(main_frame)
        graphics_frame.grid(row=6, column=0, sticky=tk.W, pady=10)
        
        self.graphics_check = ttk.Checkbutton(
            graphics_frame,
            text="Auto-extract graphics (requires Wolfram Engine)",
            variable=self.auto_extract_graphics
        )
        self.graphics_check.grid(row=0, column=0, padx=5)
        
        # Convert button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, pady=20)
        
        self.convert_button = ttk.Button(
            button_frame, 
            text="Convert to LaTeX", 
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
            length=400
        )
        self.progress.grid(row=8, column=0, pady=10)
        
        # Status/Output area
        status_label = ttk.Label(main_frame, text="Status & Output:")
        status_label.grid(row=9, column=0, sticky=tk.W, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(
            main_frame, 
            height=15, 
            width=90,
            wrap=tk.WORD
        )
        self.status_text.grid(row=10, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(10, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Footer with help text
        footer_frame = ttk.Frame(self.root, padding="10")
        footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        help_text = ("Select a Mathematica notebook file (.nb), choose display mode and options, then click Convert. " +
                    "The output will be a professional LaTeX document.")
        help_label = ttk.Label(footer_frame, text=help_text, foreground="gray", wraplength=850)
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
        self.display_mode.set("both")
        self.auto_extract_graphics.set(False)
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
            input_file = self.input_file.get()
            output_dir = self.output_dir.get()
            display_mode = self.display_mode.get()
            auto_extract = self.auto_extract_graphics.get()
            
            self.log_message("=" * 70)
            self.log_message("Starting conversion...")
            self.log_message(f"Input: {input_file}")
            self.log_message(f"Output Directory: {output_dir}")
            self.log_message(f"Display Mode: {display_mode}")
            self.log_message(f"Auto-extract graphics: {'Yes' if auto_extract else 'No'}")
            self.log_message("=" * 70)
            self.log_message("")
            
            # Perform the conversion using the advanced converter
            latex_content = mathematica_to_latex.convert_notebook_to_latex(
                input_file,
                display_mode=display_mode,
                auto_extract_graphics=auto_extract
            )
            
            # Write output file
            base_name = Path(input_file).stem
            output_file = os.path.join(output_dir, f"{base_name}.tex")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            self.log_message("")
            self.log_message("✓ Conversion completed successfully!")
            self.log_message("")
            self.log_message(f"LaTeX output written to: {output_file}")
            self.log_message(f"File size: {len(latex_content)} characters")
            self.log_message("")
            self.log_message("To compile the LaTeX document:")
            self.log_message(f"  pdflatex {os.path.basename(output_file)}")
            self.log_message("")
            self.log_message("=" * 70)
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Conversion completed successfully!\n\nOutput: {output_file}"
            ))
                
        except Exception as e:
            error_msg = f"An error occurred during conversion:\n{str(e)}"
            self.log_message("")
            self.log_message(f"✗ ERROR: {error_msg}")
            self.log_message("")
            import traceback
            self.log_message("Traceback:")
            self.log_message(traceback.format_exc())
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
