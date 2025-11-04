"""
Mathematica to LaTeX Converter - GUI Application
A user-friendly interface for converting Mathematica notebooks to LaTeX with advanced features
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import threading
from pathlib import Path

# Check Python version
if sys.version_info < (3, 7):
    print("Error: This application requires Python 3.7 or higher")
    print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}")
    sys.exit(1)

# Try to import the converter module with helpful error message
try:
    import mathematica_to_latex
except ImportError as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Import Error",
        "Could not import mathematica_to_latex module.\n\n"
        "Please ensure mathematica_to_latex.py is in the same directory as this file.\n\n"
        f"Error details: {str(e)}"
    )
    sys.exit(1)


class MathematicaConverterGUI:
    """GUI application for Mathematica to LaTeX conversion"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mathematica to LaTeX Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.input_files = []  # List to store multiple files
        self.output_dir = tk.StringVar()
        self.display_mode = tk.StringVar(value="both")
        self.auto_extract_graphics = tk.BooleanVar(value=False)
        
        # Check if advanced features are available
        self.supports_display_mode = self._check_function_parameters()
        
        # Create UI
        self.create_widgets()
        
        # Check for Wolfram Engine
        self.check_wolfram()
        
    def _check_function_parameters(self):
        """Check if convert_notebook_to_latex supports advanced parameters"""
        try:
            import inspect
            sig = inspect.signature(mathematica_to_latex.convert_notebook_to_latex)
            return 'display_mode' in sig.parameters
        except Exception:
            return False
        
    def check_wolfram(self):
        """Check if Wolfram Engine is available"""
        try:
            if hasattr(mathematica_to_latex, 'check_wolfram_engine'):
                if mathematica_to_latex.check_wolfram_engine():
                    self.log_message("✓ Wolfram Engine detected - auto graphics extraction available")
                    return
            # If we get here, Wolfram Engine not available
            self.log_message("ⓘ Wolfram Engine not found - graphics will use placeholders")
            self.graphics_check.config(state='disabled')
        except Exception as e:
            self.log_message(f"⚠ Could not check for Wolfram Engine: {e}")
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
        input_label = ttk.Label(main_frame, text="Input Mathematica Notebooks (.nb) - Select multiple to combine:")
        input_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        # Listbox to show selected files
        self.files_listbox = tk.Listbox(input_frame, height=4, width=70)
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=2, padx=(5, 0))
        
        add_button = ttk.Button(button_frame, text="Add Files...", command=self.browse_input)
        add_button.grid(row=0, column=0, pady=2, sticky=tk.W)
        
        remove_button = ttk.Button(button_frame, text="Remove", command=self.remove_selected)
        remove_button.grid(row=1, column=0, pady=2, sticky=tk.W)
        
        clear_list_button = ttk.Button(button_frame, text="Clear All", command=self.clear_file_list)
        clear_list_button.grid(row=2, column=0, pady=2, sticky=tk.W)
        
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
        
        self.mode_input = ttk.Radiobutton(
            mode_frame, 
            text="Input Cells Only (Code)", 
            variable=self.display_mode, 
            value="input-only"
        )
        self.mode_input.grid(row=0, column=0, padx=5)
        
        self.mode_output = ttk.Radiobutton(
            mode_frame, 
            text="Output Cells Only (Results)", 
            variable=self.display_mode, 
            value="output-only"
        )
        self.mode_output.grid(row=0, column=1, padx=5)
        
        self.mode_both = ttk.Radiobutton(
            mode_frame, 
            text="Input & Output Cells (Code + Results)", 
            variable=self.display_mode, 
            value="both"
        )
        self.mode_both.grid(row=0, column=2, padx=5)
        
        # Disable display mode if not supported
        if not self.supports_display_mode:
            self.mode_input.config(state='disabled')
            self.mode_output.config(state='disabled')
            self.mode_both.config(state='disabled')
        
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
        
        help_text = ("Add one or more Mathematica notebook files (.nb), choose display mode and options, then click Convert. " +
                    "Multiple files will be combined into a single LaTeX document with page breaks.")
        help_label = ttk.Label(footer_frame, text=help_text, foreground="gray", wraplength=850)
        help_label.grid(row=0, column=0)
        
    def browse_input(self):
        """Open file dialog to select input notebooks (multiple selection)"""
        try:
            filenames = filedialog.askopenfilenames(
                title="Select Mathematica Notebook(s) - Hold Ctrl/Cmd to select multiple",
                filetypes=[
                    ("Mathematica Notebooks", "*.nb"),
                    ("All Files", "*.*")
                ]
            )
            if filenames:
                for filename in filenames:
                    if filename not in self.input_files:
                        self.input_files.append(filename)
                        self.files_listbox.insert(tk.END, os.path.basename(filename))
                
                # Auto-set output directory to same as first input
                if not self.output_dir.get() and self.input_files:
                    self.output_dir.set(os.path.dirname(self.input_files[0]))
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting files: {e}")
    
    def remove_selected(self):
        """Remove selected file(s) from the list"""
        selection = self.files_listbox.curselection()
        if selection:
            # Remove in reverse order to maintain indices
            for index in reversed(selection):
                self.files_listbox.delete(index)
                del self.input_files[index]
    
    def clear_file_list(self):
        """Clear all files from the list"""
        self.files_listbox.delete(0, tk.END)
        self.input_files = []
    
    def browse_output(self):
        """Open directory dialog to select output directory"""
        try:
            directory = filedialog.askdirectory(
                title="Select Output Directory"
            )
            if directory:
                self.output_dir.set(directory)
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting directory: {e}")
    
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
        self.clear_file_list()
        self.output_dir.set("")
        self.display_mode.set("both")
        self.auto_extract_graphics.set(False)
        self.clear_status()
    
    def validate_inputs(self):
        """Validate user inputs before conversion"""
        if not self.input_files:
            messagebox.showerror("Error", "Please add at least one input file.")
            return False
        
        # Check all files exist
        for input_file in self.input_files:
            if not os.path.exists(input_file):
                messagebox.showerror("Error", f"Input file does not exist: {os.path.basename(input_file)}")
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
            input_files = self.input_files.copy()
            output_dir = self.output_dir.get()
            display_mode = self.display_mode.get()
            auto_extract = self.auto_extract_graphics.get()
            
            self.log_message("=" * 70)
            self.log_message("Starting conversion...")
            self.log_message(f"Number of files: {len(input_files)}")
            for i, f in enumerate(input_files, 1):
                self.log_message(f"  {i}. {os.path.basename(f)}")
            self.log_message(f"Output Directory: {output_dir}")
            self.log_message(f"Display Mode: {display_mode}")
            self.log_message(f"Auto-extract graphics: {'Yes' if auto_extract else 'No'}")
            self.log_message("=" * 70)
            self.log_message("")
            
            # Convert all files
            all_latex = []
            for i, input_file in enumerate(input_files, 1):
                self.log_message(f"Converting file {i}/{len(input_files)}: {os.path.basename(input_file)}...")
                
                try:
                    # Try with parameters if supported
                    if self.supports_display_mode:
                        latex_content = mathematica_to_latex.convert_notebook_to_latex(
                            input_file,
                            display_mode=display_mode,
                            auto_extract_graphics=auto_extract
                        )
                    else:
                        # Fall back to basic conversion
                        if i == 1:
                            self.log_message("  ⚠ Using basic conversion (advanced options not available)")
                        latex_content = mathematica_to_latex.convert_notebook_to_latex(input_file)
                except TypeError as e:
                    # Function signature mismatch - try basic call
                    self.log_message(f"  ⚠ Parameter error, using basic conversion: {e}")
                    latex_content = mathematica_to_latex.convert_notebook_to_latex(input_file)
                
                all_latex.append(latex_content)
                self.log_message(f"  ✓ Converted ({len(latex_content)} characters)")
            
            # Combine outputs if multiple files
            if len(all_latex) > 1:
                self.log_message("")
                self.log_message("Combining multiple notebooks...")
                import re
                combined = all_latex[0]
                for latex in all_latex[1:]:
                    content_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', 
                                             latex, re.DOTALL)
                    if content_match:
                        combined = combined.replace(r'\end{document}', 
                                                  '\n\n' + r'\newpage' + '\n\n' + 
                                                  content_match.group(1) + r'\end{document}')
                final_latex = combined
                self.log_message(f"  ✓ Combined {len(input_files)} notebooks")
            else:
                final_latex = all_latex[0]
            
            # Write output file
            if len(input_files) == 1:
                base_name = Path(input_files[0]).stem
            else:
                base_name = "combined_notebooks"
            output_file = os.path.join(output_dir, f"{base_name}.tex")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_latex)
            
            self.log_message("")
            self.log_message("✓ Conversion completed successfully!")
            self.log_message("")
            self.log_message(f"LaTeX output written to: {output_file}")
            self.log_message(f"File size: {len(final_latex)} characters")
            self.log_message("")
            self.log_message("To compile the LaTeX document:")
            self.log_message(f"  pdflatex {os.path.basename(output_file)}")
            self.log_message("")
            self.log_message("=" * 70)
            
            result_msg = f"Conversion completed successfully!\n\n"
            result_msg += f"Files converted: {len(input_files)}\n"
            result_msg += f"Output: {output_file}"
            
            self.root.after(0, lambda: messagebox.showinfo("Success", result_msg))
                
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
