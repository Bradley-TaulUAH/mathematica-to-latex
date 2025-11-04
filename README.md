# Mathematica to LaTeX Converter

> **📘 BEGINNER-FRIENDLY README**  
> This guide is written for people who are new to GitHub, Python, and programming in general. If you've never used GitHub before, don't worry! We'll walk you through every step in plain English with detailed explanations.

A comprehensive tool for converting Mathematica notebook files (.nb) to professional LaTeX documents, featuring both a desktop GUI and advanced command-line interface.

**What this tool does:** Converts your Mathematica homework, research, or project files into beautiful LaTeX documents that you can compile into PDFs.

## Features

### Advanced Conversion Engine (Integrated from PR #3 & #4)
- **Professional LaTeX output**: Proper document structure with sections, paragraphs, tables, and figures
- **Display modes**: Choose "input-only" (code), "output-only" (results), or "both" (code + results)
- **Symbol translation**: 50+ Mathematica symbols automatically converted (Greek letters, operators, special characters)
- **Automatic graphics extraction**: Extract graphics using Wolfram Engine (when available)
- **Table formatting**: GridBox tables → LaTeX tabular environments
- **Code listings**: Syntax-highlighted Mathematica code blocks
- **Math mode handling**: Automatic detection and proper LaTeX math wrapping
- **Multi-notebook support**: Combine multiple notebooks into single document

### User-Friendly GUI
- **Desktop popup interface**: Native GUI with tkinter (no web browser needed)
- **File browser dialogs**: Easy file and directory selection
- **Display mode selector**: Radio buttons for input-only/output-only/both
- **Graphics toggle**: Enable/disable automatic graphics extraction
- **Real-time status**: Live progress updates in scrolling text area
- **Progress indicator**: Visual progress bar during conversion

## What You Need Before Starting

### Software Requirements
- **Python** version 3.7 or higher (don't worry if you don't know what this means, we'll explain below)
- **tkinter** - This is a program that creates popup windows. It usually comes automatically with Python, so you probably already have it!

### What is Python?
Python is a programming language. Think of it like a language that computers understand. When you "run" a Python program, you're telling your computer to do specific tasks using Python instructions.

### What is GitHub?
You're on GitHub right now! GitHub is like Google Drive for computer code. People store their programs here and share them with others. This README file you're reading is stored on GitHub.

---

## Installation (Step-by-Step for Beginners)

### Step 1: Check if Python is Installed

**On Windows:**
1. Press the Windows key and type `cmd`
2. Press Enter to open the Command Prompt (a black window with text)
3. Type `python --version` and press Enter
4. If you see something like "Python 3.9.7", you have Python! If you see an error, you need to install Python.

**On Mac:**
1. Press Cmd+Space and type `terminal`
2. Press Enter to open Terminal (a white or black window with text)
3. Type `python3 --version` and press Enter
4. If you see something like "Python 3.9.7", you have Python! If you see an error, you need to install Python.

**On Linux:**
1. Open Terminal (usually Ctrl+Alt+T)
2. Type `python3 --version` and press Enter
3. You probably already have Python!

### Step 2: Install Python (If You Don't Have It)

**If Step 1 showed an error**, you need to download Python:

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow "Download Python" button
3. Run the downloaded file
4. **IMPORTANT on Windows:** Check the box that says "Add Python to PATH" before clicking Install
5. Click "Install Now"
6. Wait for it to finish, then click "Close"

### Step 3: Download This Tool from GitHub

There are two ways to do this:

#### Option A: Download as ZIP (Easiest for Beginners)
1. Look at the top of this page on GitHub
2. Find the green button that says "Code"
3. Click it
4. Click "Download ZIP"
5. Find the downloaded ZIP file (probably in your Downloads folder)
6. Right-click the ZIP file and choose "Extract All..." (Windows) or just double-click it (Mac)
7. Remember where you extracted it! You'll need to find this folder in the next step.

#### Option B: Clone the Repository Using Git (More Advanced, But Useful to Learn!)

**What does "clone a repository" mean?**
- **Repository** (or "repo") = A folder containing all the code for this project
- **Clone** = Make a complete copy of that folder on your computer
- When you clone, you get all the files, not just a snapshot

**Why clone instead of downloading ZIP?**
- ✅ You can easily get updates if we improve the tool (just type `git pull`)
- ✅ You can track changes over time
- ✅ Useful skill if you want to contribute or work with code in the future

**Do you have Git installed?**

First, let's check if you already have Git:

**On Windows:**
1. Press Windows key and type `cmd`, press Enter
2. Type `git --version` and press Enter
3. If you see something like "git version 2.x.x", you have Git! Skip to "Cloning the Repository" below.
4. If you see "command not found" or an error, continue to "Installing Git" below.

**On Mac:**
1. Press Cmd+Space, type `terminal`, press Enter
2. Type `git --version` and press Enter
3. If you see a version number, you have Git! Skip to "Cloning the Repository" below.
4. If Mac asks you to install developer tools, click "Install" and wait.

**On Linux:**
1. Open Terminal (Ctrl+Alt+T)
2. Type `git --version` and press Enter
3. You probably have Git already!

**Installing Git (If You Don't Have It):**

**Windows:**
1. Go to [git-scm.com/downloads](https://git-scm.com/downloads)
2. Click "Download for Windows"
3. Run the downloaded .exe file
4. Click "Next" through all the options (the defaults are fine)
5. Click "Install" and wait
6. Click "Finish"
7. **Important:** Close and reopen Command Prompt before continuing

**Mac:**
1. Git usually installs automatically when you check for the first time
2. If not, go to [git-scm.com/downloads](https://git-scm.com/downloads) and download the Mac version
3. Open the downloaded .dmg file and follow instructions

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install git

# Fedora
sudo dnf install git

# Arch
sudo pacman -S git
```

**Cloning the Repository (Step-by-Step):**

**On Windows:**
1. Open Command Prompt (press Windows key, type `cmd`, press Enter)
2. Decide where you want to put the tool. Your Desktop is usually a good choice.
3. Navigate to that location by typing:
   ```bash
   cd Desktop
   ```
   Press Enter. (If you want a different location, replace `Desktop` with that folder name)
4. Now clone the repository by typing this exact command:
   ```bash
   git clone https://github.com/Bradley-TaulUAH/mathematica-to-latex.git
   ```
   Press Enter.
5. You'll see text appearing as it downloads. Lines like "Receiving objects" and "Resolving deltas" are normal!
6. When it's done (you'll see the command prompt again), you now have a folder called `mathematica-to-latex` on your Desktop!
7. Go into that folder by typing:
   ```bash
   cd mathematica-to-latex
   ```
   Press Enter.
8. You're now inside the tool's folder! Continue to Step 4 below.

**On Mac:**
1. Open Terminal (press Cmd+Space, type `terminal`, press Enter)
2. Decide where you want to put the tool. Your Desktop is usually a good choice.
3. Navigate to that location by typing:
   ```bash
   cd ~/Desktop
   ```
   Press Enter. (The `~` means "my home folder")
4. Now clone the repository by typing this exact command:
   ```bash
   git clone https://github.com/Bradley-TaulUAH/mathematica-to-latex.git
   ```
   Press Enter.
5. You'll see text appearing as it downloads. This is normal!
6. When it's done (you'll see the command prompt again), you now have a folder called `mathematica-to-latex` on your Desktop!
7. Go into that folder by typing:
   ```bash
   cd mathematica-to-latex
   ```
   Press Enter.
8. You're now inside the tool's folder! Continue to Step 4 below.

**On Linux:**
1. Open Terminal (Ctrl+Alt+T)
2. Navigate to where you want the tool:
   ```bash
   cd ~/Desktop
   ```
   Press Enter.
3. Clone the repository:
   ```bash
   git clone https://github.com/Bradley-TaulUAH/mathematica-to-latex.git
   ```
   Press Enter.
4. Go into the folder:
   ```bash
   cd mathematica-to-latex
   ```
   Press Enter.

**What just happened?**
- Git downloaded all the files from GitHub to your computer
- You now have a folder called `mathematica-to-latex` with all the tool's files inside
- This folder is connected to GitHub, so you can get updates later by typing `git pull`

**Troubleshooting:**

❌ **"Permission denied" error?**
- Make sure you're not trying to clone into a protected folder like C:\Program Files
- Try cloning to your Desktop or Documents folder instead

❌ **"Repository not found" or "Access denied"?**
- Check that you typed the URL exactly: `https://github.com/Bradley-TaulUAH/mathematica-to-latex.git`
- Make sure you have internet connection

❌ **"Failed to connect" or timeout?**
- Check your internet connection
- If you're behind a corporate firewall, you might need to ask your IT department
- Try Option A (Download ZIP) instead

**Getting Updates in the Future:**

One big advantage of cloning is you can easily get updates!

1. Open Terminal/Command Prompt
2. Navigate to the tool's folder:
   ```bash
   cd Desktop/mathematica-to-latex
   ```
3. Type:
   ```bash
   git pull
   ```
   Press Enter.
4. Git will download any new changes we've made since you first cloned!

**Still confused?** That's okay! Just use Option A (Download ZIP) instead. It works just as well!

### Step 4: Verify Everything Works (Optional but Recommended)

**On Windows:**
1. Open Command Prompt again (press Windows key, type `cmd`, press Enter)
2. Navigate to the folder where you extracted/downloaded the tool:
   ```bash
   cd Desktop\mathematica-to-latex
   ```
   (Adjust the path based on where you put it)
3. Type this and press Enter:
   ```bash
   python -c "import tkinter; print('✓ tkinter is available!')"
   ```
4. If you see "✓ tkinter is available!", you're good to go!

**On Mac/Linux:**
1. Open Terminal
2. Navigate to the folder:
   ```bash
   cd ~/Desktop/mathematica-to-latex
   ```
   (Adjust the path based on where you put it)
3. Type this and press Enter:
   ```bash
   python3 -c "import tkinter; print('✓ tkinter is available!')"
   ```
4. If you see "✓ tkinter is available!", you're good to go!

**If you see an error about tkinter:**
- **Ubuntu/Debian Linux:** Type `sudo apt-get install python3-tk` and press Enter
- **Mac:** tkinter should come with Python. If not, you may need to reinstall Python from python.org
- **Windows:** tkinter should come with Python. If not, reinstall Python and make sure to check all the boxes during installation.

---

That's it! You've successfully installed everything you need. No external dependencies required for the GUI.

## How to Use This Tool (Beginner-Friendly Instructions)

### 🚀 Quick Start - Get Converting in 30 Seconds!

This is the easiest way to start using the tool:

**On Windows:**
1. Open Command Prompt (press Windows key, type `cmd`, press Enter)
2. Navigate to the folder where you downloaded the tool:
   ```bash
   cd Desktop\mathematica-to-latex
   ```
   (Change `Desktop` if you put it somewhere else)
3. Type this and press Enter:
   ```bash
   python run_gui.py
   ```
4. A window will pop up! (If nothing happens, see troubleshooting below)

**On Mac/Linux:**
1. Open Terminal (press Cmd+Space, type `terminal`, press Enter on Mac)
2. Navigate to the folder where you downloaded the tool:
   ```bash
   cd ~/Desktop/mathematica-to-latex
   ```
   (Change `Desktop` if you put it somewhere else)
3. Type this and press Enter:
   ```bash
   python3 run_gui.py
   ```
4. A window will pop up! (If nothing happens, see troubleshooting below)

**What is "navigate to the folder"?**
Think of your computer's files like a filing cabinet. "Navigating" means telling the computer which drawer (folder) you want to look in. The `cd` command means "change directory" (directory = folder).

---

### 📱 Desktop GUI Mode (Recommended - With Pictures!)

This is what you'll see and how to use it:

#### Starting the GUI:

**Windows:**
```bash
python mathematica_gui.py
```

**Mac/Linux:**
```bash
python3 mathematica_gui.py
```

#### Using the GUI Window:

Once the window appears, you'll see several buttons and options. Here's what each one does:

**1. Adding Your Mathematica Files:**
- Look for the button that says **"Add Files..."**
- Click it
- A file browser window will appear (just like when you open a file in Word)
- Find your Mathematica notebook file (it ends with `.nb`)
- Click on it to select it
- Click "Open"

**💡 TIP: Selecting Multiple Files at Once**
- Hold down the **Ctrl** key (Windows/Linux) or **Cmd** key (Mac) while clicking
- This lets you select multiple files
- All selected files will be combined into one LaTeX document
- Great for combining all your homework problems into one PDF!

**2. Choosing Where to Save:**
- Look for the **"Output Directory"** section
- Click the **"Browse..."** button
- Pick the folder where you want the LaTeX file saved
- If you don't pick anything, it will save in the same folder as your input file

**3. Display Mode Options:**
You'll see three radio buttons (circles you can click):
- **"Input Cells Only (Code)"**: Only shows the Mathematica commands you typed
- **"Output Cells Only (Results)"**: Only shows the answers and results
- **"Input & Output Cells (Code + Results)"**: Shows both (✓ Recommended - this is usually what you want!)

**4. Graphics Options:**
- There's a checkbox that says **"Auto-extract graphics"**
- If you have Wolfram Engine or Mathematica installed, check this box
- It will automatically extract any graphs or figures from your notebook
- If you don't have these installed, leave it unchecked (the tool will still work!)

**5. Converting Your File:**
- After selecting your file(s) and options, click the big **"Convert to LaTeX"** button
- You'll see a progress bar fill up
- The status area at the bottom will show what's happening:
  ```
  Converting file 1/1: YourFile.nb...
  ✓ Converted (25403 characters)
  ✓ Conversion completed successfully!
  LaTeX output: YourFile.tex
  ```
- When you see the checkmark (✓), you're done!

**6. Finding Your Converted File:**
- Go to the output folder you selected (or the same folder as your input file)
- Look for a file with the same name but ending in `.tex` instead of `.nb`
- Example: `HW 8-1 pb 4.nb` becomes `HW 8-1 pb 4.tex`
- This is your LaTeX file!

#### What to Do with the .tex File:

Now that you have a `.tex` file, you need to compile it into a PDF. Here are your options:

**Option 1: Online (Easiest)**
1. Go to [Overleaf.com](https://www.overleaf.com) (it's free!)
2. Create an account if you don't have one
3. Click "New Project" → "Upload Project"
4. Upload your `.tex` file
5. Click the green "Recompile" button
6. Your PDF appears on the right side!

**Option 2: On Your Computer**
1. Install a LaTeX distribution:
   - Windows: MiKTeX or TeX Live
   - Mac: MacTeX
   - Linux: `sudo apt-get install texlive-full` (Ubuntu/Debian)
2. Open your `.tex` file in TeXstudio or TeXmaker (free LaTeX editors)
3. Click the green arrow or "Build & View" button
4. Your PDF appears!

---

### 🌐 Web GUI Mode (Alternative - Uses Your Browser)

If the desktop GUI doesn't work, or if you prefer using your web browser:

**Step 1: Install Flask** (a program that creates websites on your computer):

**Windows:**
```bash
pip install flask werkzeug
```

**Mac/Linux:**
```bash
pip3 install flask werkzeug
```

Wait for it to finish downloading and installing.

**Step 2: Start the Web Server:**

**Windows:**
```bash
python web_gui.py
```

**Mac/Linux:**
```bash
python3 web_gui.py
```

You'll see some text appear. Look for a line that says something like:
```
* Running on http://127.0.0.1:5000/
```

**Step 3: Open Your Browser:**
1. Open any web browser (Chrome, Firefox, Safari, Edge, etc.)
2. In the address bar at the top, type: `http://localhost:5000`
3. Press Enter
4. You'll see a web page with the converter interface!

**Step 4: Use the Web Interface:**
- Drag and drop your `.nb` file onto the page, OR click to browse for it
- Choose your display mode (Input Only / Output Only / Both)
- Click "Convert"
- Wait a moment, then click "Download LaTeX" to get your file

**Step 5: Stop the Server When Done:**
- Go back to the Command Prompt/Terminal window
- Press **Ctrl+C** (this stops the server)
- You can close the window now

### Web GUI Mode (Alternative)

If you prefer a web interface or tkinter is not available, you can use the web-based GUI:

1. Install Flask:
```bash
pip install flask werkzeug
```

2. Start the web server:
```bash
python web_gui.py
```

3. Open your browser to `http://localhost:5000`

### ⚙️ Command-Line Mode (For Advanced Users)

**What is "Command-Line"?**
Command-line means typing commands directly instead of clicking buttons. It's faster once you learn it, and it's useful for processing many files at once.

**Basic Format:**

**Windows:**
```bash
python mathematica_to_latex.py "YourFile.nb"
```

**Mac/Linux:**
```bash
python3 mathematica_to_latex.py "YourFile.nb"
```

**What are "options"?**
Options are extra instructions you can add to customize the conversion. You add them after the filename, like this:
```bash
python mathematica_to_latex.py "YourFile.nb" --mode output-only
```

**Available Options:**

| Option | What It Does | Example |
|--------|-------------|---------|
| `-o filename.tex` | Choose a different output filename | `-o homework.tex` |
| `--mode input-only` | Only show code (no results) | `--mode input-only` |
| `--mode output-only` | Only show results (no code) | `--mode output-only` |
| `--mode both` | Show both code and results (default) | `--mode both` |
| `--auto-extract-graphics` | Extract graphs and figures automatically | `--auto-extract-graphics` |

**Examples with Explanations:**

**Example 1: Basic Conversion**
Convert a single file with default settings:

**Windows:**
```bash
python mathematica_to_latex.py "HW 8-1 pb 4.nb"
```

**Mac/Linux:**
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 4.nb"
```

What happens: Creates `HW 8-1 pb 4.tex` in the same folder, showing both code and results.

---

**Example 2: Only Show Results**
Great for when you want a clean document without the code:

**Windows:**
```bash
python mathematica_to_latex.py "HW 8-1 pb 4.nb" --mode output-only -o results.tex
```

**Mac/Linux:**
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 4.nb" --mode output-only -o results.tex
```

What happens: Creates `results.tex` showing only the final answers and results.

---

**Example 3: Extract Graphics Automatically**
If you have Wolfram Engine or Mathematica installed:

**Windows:**
```bash
python mathematica_to_latex.py "HW 8-1 pb 5-all.nb" --auto-extract-graphics
```

**Mac/Linux:**
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 5-all.nb" --auto-extract-graphics
```

What happens: Converts the file AND extracts any graphs/plots as separate image files.

---

**Example 4: Combine Multiple Files**
Combine all your homework problems into one document:

**Windows:**
```bash
python mathematica_to_latex.py "HW 8-1 pb 4.nb" "HW 8-1 pb 5-all.nb" "HW 8-1 pb 8.nb" -o combined.tex
```

**Mac/Linux:**
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 4.nb" "HW 8-1 pb 5-all.nb" "HW 8-1 pb 8.nb" -o combined.tex
```

What happens: Creates `combined.tex` with all three problems in one file, separated by page breaks.

---

## ❓ Frequently Asked Questions (FAQ)

### "I typed the command but nothing happened!"

**Possible reasons:**
1. You might be in the wrong folder. Use `cd` to navigate to the `mathematica-to-latex` folder first.
2. On Mac/Linux, you might need to use `python3` instead of `python`.
3. Make sure you included the filename in quotes: `"YourFile.nb"`

### "I get an error that says 'python is not recognized' or 'command not found'"

This means Python isn't installed, or it wasn't added to your PATH. Go back to Step 2 of Installation and install Python. On Windows, make sure you check "Add Python to PATH" during installation.

### "The GUI window won't open!"

Try these solutions:
1. Make sure tkinter is installed (see Step 4 of Installation)
2. Try using the web GUI instead (see Web GUI Mode section above)
3. On Linux, you might need to install python3-tk: `sudo apt-get install python3-tk`

### "My .tex file has errors when I try to compile it"

The converter does its best, but complex Mathematica notebooks might need some manual fixes:
1. Open your `.tex` file in a text editor
2. Look for the line where the error occurs (the LaTeX compiler will tell you)
3. Common fixes:
   - Missing math symbols: Add `$` around math expressions
   - Special characters: Replace `&` with `\&`, `%` with `\%`, etc.

### "Can I convert multiple files at once?"

Yes! Two ways:
1. **Using GUI**: Hold Ctrl (Windows/Linux) or Cmd (Mac) while selecting multiple files
2. **Using command-line**: List all files separated by spaces:
   ```bash
   python mathematica_to_latex.py "file1.nb" "file2.nb" "file3.nb" -o combined.tex
   ```

### "Where did my converted file go?"

By default, it's saved in the same folder as your input file with a `.tex` extension. For example:
- Input: `C:\Users\YourName\Documents\homework.nb`
- Output: `C:\Users\YourName\Documents\homework.tex`

### "Do I need Mathematica installed to use this?"

No! You only need the `.nb` files. The converter reads them directly. However:
- If you want automatic graphics extraction, you do need Wolfram Engine or Mathematica
- Without it, you can still convert everything else perfectly fine

### "Can I use this for my homework/thesis/paper?"

Yes! That's exactly what it's designed for. The tool converts your Mathematica work into professional LaTeX documents suitable for:
- Homework assignments
- Research papers
- Theses and dissertations
- Technical documentation
- Any academic or professional document

---

## 🔧 Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named 'tkinter'"

**Solution:**
- **Windows:** Reinstall Python from python.org and make sure all components are selected
- **Mac:** Tkinter should come with Python. If not, try: `brew install python-tk`
- **Ubuntu/Debian Linux:** `sudo apt-get install python3-tk`
- **Fedora Linux:** `sudo dnf install python3-tkinter`
- **Arch Linux:** `sudo pacman -S tk`

### Issue: "Permission denied" error

**Solution:**
You don't have permission to write to that folder. Either:
1. Choose a different output folder (like your Documents or Desktop)
2. Or on Mac/Linux, you might need to use `sudo` (but this is usually not recommended)

### Issue: LaTeX compilation fails with "File ended while scanning use of..."

**Solution:**
This usually means there's a special character that wasn't converted properly. Open the `.tex` file and look for:
- Unmatched `$` signs (every math formula needs opening and closing `$`)
- Unescaped special characters like `&`, `%`, `#`, `_`
- Empty commands like `\paragraph{}`

The converter tries to fix these automatically, but complex notebooks might need manual review.

### Issue: Graphics/figures don't appear in the PDF

**Solutions:**
1. Make sure you checked "Auto-extract graphics" in the GUI (or used `--auto-extract-graphics` in command-line)
2. You need Wolfram Engine or Mathematica installed for automatic extraction
3. Alternative: Manually export figures from Mathematica and include them in LaTeX using `\includegraphics{filename.png}`

### Issue: "The system cannot find the path specified"

**Solution:**
You're in the wrong folder. Make sure to use `cd` to navigate to the folder where you downloaded the tool. Example:
```bash
cd Desktop\mathematica-to-latex
```

---

## 🎓 How It Works (Behind the Scenes)

**For curious beginners:** Here's what happens when you click "Convert":

1. **Reading:** The converter opens your `.nb` file and reads all the content
2. **Parsing:** It breaks down the file into pieces (cells, code, output, formulas, etc.)
3. **Converting:** Each piece is translated from Mathematica language to LaTeX language
4. **Symbol Translation:** Special symbols are converted:
   - Mathematica: `α` → LaTeX: `\alpha`
   - Mathematica: `∫` → LaTeX: `\int`
   - And 50+ more symbols!
5. **Formatting:** The converter adds proper LaTeX structure (sections, paragraphs, boxes, etc.)
6. **Output:** Everything is saved to a `.tex` file

Think of it like translating a book from English to Spanish - the meaning stays the same, but the words change.

## ✅ What This Tool Can Convert

The converter handles:
- ✓ Mathematical symbols (α, β, π, ∞, ℏ, etc.)
- ✓ Mathematical operators (≤, ≥, ≠, ±, ×, ÷, etc.)
- ✓ Integrals, sums, products, and limits
- ✓ Fractions and equations
- ✓ Section headers and titles
- ✓ Text and comments
- ✓ Code cells (shown as syntax-highlighted listings)
- ✓ Output cells (shown in colored boxes)
- ✓ Tables (converted to professional LaTeX tables)
- ✓ Multiple notebooks combined into one document

## ⚠️ Limitations (What It Can't Do Perfectly)

This tool is very good, but it's not perfect:
- ⚠️ Very complex nested structures might need manual fixes
- ⚠️ Some rare Mathematica functions don't have LaTeX equivalents
- ⚠️ Interactive elements (sliders, buttons) can't be converted to static LaTeX
- ⚠️ 3D graphics might need manual adjustment
- ⚠️ Custom Mathematica packages might not convert completely

**But don't worry!** The tool still gives you a great starting point that you can polish manually if needed.

---

## 📸 What It Looks Like

### Desktop GUI Interface
When you run the tool, you'll see a clean popup window with:
- File selection buttons
- Display mode options (radio buttons)
- Graphics extraction checkbox
- Output directory selector
- Big "Convert to LaTeX" button
- Status area showing progress

The interface is designed to be simple and self-explanatory - if you can use Microsoft Word, you can use this!

---

## 🎯 Example Files Included

The tool comes with generic example files in the `examples/` directory that you can use to test it:

| File | What It Contains | Description |
|------|-----------------|-------------|
| `simple_calculus.nb` | Basic calculus operations | Differentiation, integration, solving equations |
| `physics_example.nb` | Quantum harmonic oscillator | Energy levels, wave functions, physics formulas |
| `symbolic_math.nb` | Symbolic mathematics | Trig identities, matrix operations, simplification |

**⚠️ Important: Use Your Own Files for Actual Work**

These examples are **generic demonstrations only**. For homework, research, or any real work:
- Use your own Mathematica `.nb` files from your computer
- The converter works on **any** `.nb` file, regardless of location
- Keep personal/private notebooks in a separate location (not in this repository)
- See `examples/README.md` for privacy guidelines

**Try it out:**
1. Run the GUI: `python mathematica_gui.py` (or `python3` on Mac/Linux)
2. Click "Add Files..."
3. Navigate to the `examples/` folder and select one of the example files
4. Click "Convert to LaTeX"
5. Look at the generated `.tex` file to see what the converter produces!

**To convert your own files:**
- Your `.nb` files can be anywhere on your computer (Desktop, Documents, etc.)
- Just navigate to them using the "Add Files..." button
- The tool doesn't need files to be in any specific location

---

## 💡 Pro Tips for Best Results

1. **Clean up your Mathematica notebook first:** Remove any unnecessary cells or outputs before converting
2. **Use descriptive section headers:** These become section titles in LaTeX
3. **Combine multiple files wisely:** Put related problems together, but don't combine too many (keeps files manageable)
4. **Check the output:** Always open the `.tex` file in a text editor to verify it looks good
5. **Compile in Overleaf first:** It's easier than setting up LaTeX on your computer, and you can see errors clearly
6. **Save your .nb files:** Keep the original Mathematica files in case you need to reconvert

---

## 🆘 Getting Help

**If something goes wrong and this README didn't help:**

1. **Check the error message:** The tool tries to give helpful error messages. Read them carefully!
2. **Try the example files:** If the examples work but your file doesn't, there might be something unusual in your file
3. **Ask for help on GitHub:**
   - Go to the "Issues" tab at the top of this page
   - Click "New Issue"
   - Describe what you tried and what error you got
   - Someone will help you!

**When asking for help, include:**
- What operating system you're using (Windows 10, Mac, Ubuntu, etc.)
- The exact command you typed
- The full error message (copy and paste it)
- Whether the example files work

---

## 🤝 Contributing (For Advanced Users)

**What is "contributing"?**
Contributing means helping make this tool better. If you know how to program and want to improve the converter, you can:
1. Fork this repository (make your own copy)
2. Make improvements
3. Submit a Pull Request (ask us to include your improvements)

If you don't know how to program, you can still help by:
- Reporting bugs (things that don't work)
- Suggesting new features
- Improving this documentation

---

## 📜 License

**What is a "license"?**
A license tells you what you're allowed to do with this software. This project uses the MIT License, which means:
- ✓ You can use it for free
- ✓ You can use it for homework, research, commercial work - anything!
- ✓ You can modify it if you want
- ✓ You can share it with others

**The only rule:** Include the original copyright notice if you share it.

**In plain English:** Do whatever you want with this tool. It's free and open for everyone!

---

## 📁 Project Structure (For Curious Users)

**What are all these files?**

```
mathematica-to-latex/
├── mathematica_to_latex.py     # Main converter (877 lines of code!)
├── mathematica_gui.py           # Desktop GUI interface
├── web_gui.py                   # Web browser interface
├── run_gui.py                   # Smart launcher (picks best option)
├── mathematica_converter.py     # Simple converter (backup)
├── requirements.txt             # List of dependencies (empty - no deps!)
├── README.md                    # This file you're reading
├── README_DETAILED.md           # Even more detailed guide
├── USAGE.md                     # Usage examples
├── .gitignore                   # Tells Git what files to ignore
├── HW 8-1 pb 4.nb              # Example file #1
├── HW 8-1 pb 5-all.nb          # Example file #2
├── HW 8-1 pb 8.nb              # Example file #3
└── templates/                   # Web interface templates
    └── index.html               # Web interface HTML
```

**What is each file for?**
- `.py` files = Python programs (the actual code)
- `.nb` files = Mathematica notebooks (examples)
- `.md` files = Documentation (instructions and guides)
- `.txt` files = Text files with lists
- `.html` files = Web pages

---

## 🧪 Testing the Converter

**Want to make sure everything works?**

### Test 1: Basic Conversion (Command-Line)

**Windows:**
```bash
python mathematica_to_latex.py "HW 8-1 pb 8.nb"
```

**Mac/Linux:**
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 8.nb"
```

**Expected result:** Creates `HW 8-1 pb 8.tex` in the same folder. Open it in a text editor - you should see LaTeX code!

### Test 2: GUI Test

**Windows:**
```bash
python mathematica_gui.py
```

**Mac/Linux:**
```bash
python3 mathematica_gui.py
```

**Expected result:** A window pops up with buttons and options.

### Test 3: Multi-File Combination

Try combining all three example files:

**Windows:**
```bash
python mathematica_to_latex.py "HW 8-1 pb 4.nb" "HW 8-1 pb 5-all.nb" "HW 8-1 pb 8.nb" -o test_combined.tex
```

**Mac/Linux:**
```bash
python3 mathematica_to_latex.py "HW 8-1 pb 4.nb" "HW 8-1 pb 5-all.nb" "HW 8-1 pb 8.nb" -o test_combined.tex
```

**Expected result:** Creates `test_combined.tex` with all three problems in one file.

---

## 🎓 Additional Resources

**Want to learn more about LaTeX?**
- [Overleaf Documentation](https://www.overleaf.com/learn) - Great tutorials
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX) - Comprehensive guide
- [Detexify](http://detexify.kirelabs.org/classify.html) - Draw a symbol to find its LaTeX command

**Want to learn more about Python?**
- [Python.org Tutorial](https://docs.python.org/3/tutorial/) - Official beginner guide
- [Automate the Boring Stuff](https://automatethe boringsstuff.com/) - Practical Python for beginners

**Want to learn more about GitHub?**
- [GitHub Guides](https://guides.github.com/) - Official tutorials
- [Git Handbook](https://guides.github.com/introduction/git-handbook/) - Understanding Git basics

---

## 🌟 Final Notes for Complete Beginners

**Don't be intimidated!** This tool is designed to be user-friendly. Here's what you really need to know:

1. **Install Python** (free, takes 5 minutes)
2. **Download this tool** (click "Code" → "Download ZIP" at the top of this page)
3. **Run the GUI** (double-click or use command prompt)
4. **Select your file** and click "Convert"
5. **Done!** You have a LaTeX file.

Everything else in this README is just helpful details in case you need them.

**Still confused?** That's okay! Open an Issue on GitHub (the "Issues" tab at the top) and describe what you're trying to do. We're here to help!

**Remember:** Everyone was a beginner once. Don't hesitate to ask questions. The only "stupid" question is the one you don't ask!

---

**Happy Converting! 🎉**

*Made with ❤️ for students and researchers who want beautiful LaTeX documents from their Mathematica work.*
