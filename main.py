import os
import re
import sys
import subprocess
import shutil

# Import shared fix logic
from fix_md import fix_content

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





def process_docx_files(app_path):
    """
    Scans for .docx files and converts them to .md.
    Locations:
      1. 'google_docx' folder -> converts to 'google_md'
      2. Root folder -> converts to Root folder
    """
    # Pairs of (Source Dir, Output Dir)
    dirs_to_process = [
        (os.path.join(app_path, 'google_docx'), os.path.join(app_path, 'google_md')),
        (app_path, app_path)
    ]
    
    count_docx = 0
    
    for docx_dir, md_dir in dirs_to_process:
        if not os.path.exists(docx_dir):
            continue
            
        if not os.path.exists(md_dir):
            os.makedirs(md_dir)
            
        print(f"Scanning for DOCX in: {docx_dir}")
        
        for filename in os.listdir(docx_dir):
            if filename.lower().endswith(".docx"):
                # Skip temporary Word files (start with ~$)
                if filename.startswith("~$"):
                    continue
                    
                docx_path = os.path.join(docx_dir, filename)
                # Create corresponding md filename
                md_filename = os.path.splitext(filename)[0] + ".md"
                md_path = os.path.join(md_dir, md_filename)
                
                # If source and dest are same (root), output is just filename
                rel_output = os.path.relpath(md_path, app_path)
                print(f"Preprocessing: {filename} -> {rel_output}")
                
                try:
                    # Convert docx to md using Pandoc (with wrap=none to avoid line breaks breaking formulas)
                    cmd = ['pandoc', docx_path, '-f', 'docx', '-t', 'markdown-simple_tables-multiline_tables-grid_tables', '--wrap=none', '-o', md_path]
                    subprocess.run(cmd, check=True)
                    print(f"  [Pre-process] Converted to Markdown.")
                    count_docx += 1
                except subprocess.CalledProcessError as e:
                    print(f"  [Pre-process] Failed: {e}")
                except Exception as e:
                    print(f"  [Pre-process] Error: {e}")
                
    if count_docx > 0:
        print(f"Pre-processed {count_docx} DOCX files to Markdown.\n")

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
    else:
        # Step 0: Pre-process DOCX files if any
        process_docx_files(app_path)

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
                    
                    # Determine target output directory
                    if current_dir == google_md_path:
                        target_output_dir = output_dir # word_output
                    else:
                        target_output_dir = app_path   # root
                        
                    output_path = os.path.join(target_output_dir, output_filename)
                    
                    try:
                        cmd = ['pandoc', filepath, '-o', output_path]
                        subprocess.run(cmd, check=True)
                        
                        # Pretty print relative path for the user
                        rel_output = os.path.relpath(output_path, app_path)
                        print(f"  [Convert] Created: {rel_output}")
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
