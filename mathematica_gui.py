import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class MathematicaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Mathematica to LaTeX Converter")

        self.label = tk.Label(master, text="Select a Mathematica file:")
        self.label.pack(pady=10)

        self.file_path = tk.StringVar()
        self.entry = tk.Entry(master, textvariable=self.file_path, width=50)
        self.entry.pack(pady=10)

        self.browse_button = tk.Button(master, text="Browse...", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.convert_button = tk.Button(master, text="Convert to LaTeX", command=self.convert_file)
        self.convert_button.pack(pady=20)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(pady=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=(("Mathematica Files", "*.nb"),))
        if filename:
            self.file_path.set(filename)

    def convert_file(self):
        file = self.file_path.get()
        if not file:
            messagebox.showwarning("Warning", "Please select a Mathematica file!")
            return

        # Call the external mathematica-to-latex script
        try:
            subprocess.run(["mathematica-to-latex", file], check=True)
            messagebox.showinfo("Success", "Conversion completed! Check your directory.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Conversion failed. Make sure 'mathematica-to-latex' is available.")

if __name__ == '__main__':
    root = tk.Tk()
    gui = MathematicaGUI(root)
    root.mainloop()