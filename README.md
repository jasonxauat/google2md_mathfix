# Google Docs Markdown Fixer

A lightweight utility to fix formatting issues in Markdown files exported from Google Docs.

**Specific Use Case**: This tool is designed to fix the "aggressive escaping" issues that occur when **Gemini-generated content** (especially mathematical formulas) is saved to **Google Docs** and then exported as **Markdown**.

It specifically handles:
- **LaTeX Math Repair**: Restores formulas broken by escaping (e.g., `\\tau` becoming `\tau`).
- **Special Character Fixes**: Restores `_`, `=`, `.`, `+`, `[` which are often incorrectly escaped.

[ [中文说明](README_CN.md) ]

## Features
- **Fix Aggressive Escaping**: Automatically restores `_`, `=`, `.`, `+`, `[` and other characters that Google Docs incorrectly escapes.
- **LaTeX Math Repair**: Ensures LaTeX formulas (e.g., `\tau`, `\boldsymbol`) render correctly.
- **Batch Processing**: Scans and fixes all `.md` files in the `google_md` directory.
- **Word Conversion**: Optionally converts fixed Markdown files to `.docx` (requires Pandoc).

## Installation

### Prerequisites
- [Python 3.x](https://www.python.org/downloads/)
- [Pandoc](https://pandoc.org/) (Optional, strictly for `.docx` conversion)

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/google2md_mathfix.git
   ```
2. (Optional) Install development dependencies if you plan to build the executable:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare Files**: 
   - **Option A (Markdown)**: Place your exported Google Docs Markdown files (the broken ones) into the `google_md` folder.
   - **Option B (Word)**: Place your Google Docs `.docx` files into the `google_docx` folder (or the root directory). The script will first convert them to Markdown, fix the equations, and then process them.
2. **Run the Script**:
   ```bash
   python fix_md.py
   ```
   Or use the main processor which also handles Word conversion:
   ```bash
   python main.py
   ```
3. **Check Output**:
   - Fixed Markdown files will overwrite the originals in `google_md` (if changes are needed).
   - Converted Word documents will appear in `word_output`.

## Script Details
- **`main.py`**: The main entry point. Orchestrates the scanning, fixing, and conversion process. It supports processing both the current directory and the `google_md` folder.
- **`fix_md.py`**: Contains the core logic and Regex patterns for repairing the Markdown content. Can be run standalone to just fix files without conversion.
- **`md_to_docx.py`**: A utility script that handles calling Pandoc to convert Markdown to Word documents.
- **`reset_test.py`**: A testing utility that intentionally "corrupts" a clean Markdown file (re-applies escaping) to verify if `fix_md.py` can repair it correctly.

## Build Executable (Optional)
If you want to create a standalone `.exe` file to run without Python installed:

1. **Install PyInstaller**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Build**:
   ```bash
   pyinstaller google2md_mathfix.spec
   ```
3. **Locate Executable**:
   The generated file will be in the `dist` folder: `dist/google2md_mathfix.exe`.
   You can copy this `.exe` file to any folder containing your markdown files (or `google_md` folder) and run it directly.

## How it Works
The script applies a series of strictly ordered Regular Expressions to reverse the escaping done by Google Docs.
1. Restores `\\` to `\` (critical for LaTeX).
2. Restores `_`, `=`, `-` etc. to their original characters.
3. Restores horizontal rules (`---`) often broken as `## ---`.

## License
MIT License
