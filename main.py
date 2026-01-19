import os
import re
import sys
import subprocess
import shutil

def get_application_path():
    """
    Get the directory where the application is running.
    Works for both script (python file.py) and frozen exe (PyInstaller).
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def check_pandoc():
    """Check if pandoc is installed and accessible."""
    try:
        subprocess.run(['pandoc', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def fix_content(content):
    """
    Applies regex replacements to fix Google Docs export issues.
    """
    replacements = [
        (r'\\\\', r'\\'),      # Replace \\ with \ 
        (r'\\_', r'_'),        # Replace \_ with _
        (r'\\=', r'='),        # Replace \= with =
        (r'\\-', r'-'),        # Replace \- with -
        (r'\\\+', r'+'),       # Replace \+ with +
        (r'\\\.', r'.'),       # Replace \. with .
        (r'\\\[', r'['),       # Replace \[ with [
        (r'\\\]', r']'),       # Replace \] with ]
        (r'\\<', r'<'),        # Replace \< with <
        (r'\\>', r'>'),        # Replace \> with >
        (r'\\\{', r'{'),       # Replace \{ with {
        (r'\\\}', r'}'),       # Replace \} with }
        (r'\\\*', r'*'),       # Replace \* with *
        (r'\\\|', r'|'),       # Replace \| with |
        (r'#+[ \t]*---', r'---'), # Replace any header-interpreted separator (# ---, ## ---, ### ---)
    ]
    
    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)
        
    # Prepend YAML header if missing
    yaml_header = "---\noutput: word_document\n---\n\n"
    if not content.startswith("---"):
        content = yaml_header + content
        
    return content

def process_docs():
    app_path = get_application_path()
    print(f"Working directory: {app_path}")
    
    # Define output directory
    output_dir = os.path.join(app_path, 'word_output')

    __version__ = "1.0.0"
    print(f"Google Docs Markdown Fixer v{__version__}")
    print(f"Working directory: {app_path}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Check Pandoc
    has_pandoc = check_pandoc()
    if not has_pandoc:
        print("WARNING: Pandoc not found. Markdown files will be fixed, but conversion to Word will be skipped.")
        print("Please install Pandoc (https://pandoc.org/) to enable Word conversion.")

    count_fixed = 0
    count_converted = 0

    # Define directories to scan
    scan_dirs = [app_path]
    google_md_path = os.path.join(app_path, 'google_md')
    if os.path.exists(google_md_path):
        scan_dirs.append(google_md_path)

    # Files to ignore in root directory
    ignored_files = ['readme.md', 'readme_cn.md']

    for current_dir in scan_dirs:
        print(f"Scanning directory: {current_dir}")
        
        for filename in os.listdir(current_dir):
            if filename.endswith(".md"):
                # If we are in the root app_path, skip ignored files
                if current_dir == app_path and filename.lower() in ignored_files:
                    print(f"Skipping ignored file: {filename}")
                    continue
                    
                filepath = os.path.join(current_dir, filename)
                print(f"Processing: {filename}")
                
                # --- 1. Fix Markdown Content ---
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    fixed_content = fix_content(content)
                    
                    if fixed_content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)
                        print(f"  [Fix] Applied formatting fixes.")
                        count_fixed += 1
                    else:
                        print(f"  [Fix] No formatting changes needed.")
                except Exception as e:
                    print(f"  [Error] Failed to read/write file: {e}")
                    continue

                # --- 2. Convert to Docx ---
                if has_pandoc:
                    output_filename = os.path.splitext(filename)[0] + ".docx"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    try:
                        cmd = ['pandoc', filepath, '-o', output_path]
                        subprocess.run(cmd, check=True)
                        print(f"  [Convert] Created: word_output/{output_filename}")
                        count_converted += 1
                    except subprocess.CalledProcessError as e:
                        print(f"  [Convert] Failed: {e}")
                    except Exception as e:
                        print(f"  [Convert] Error: {e}")

    print(f"\nSummary:")
    print(f"  Files Fixed: {count_fixed}")
    if has_pandoc:
        print(f"  Files Converted: {count_converted}")
    else:
        print(f"  Conversion skipped (Pandoc missing).")
        
    print(f"\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    process_docs()
