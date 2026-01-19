import os
import subprocess
import shutil

def check_pandoc():
    """Check if pandoc is installed and accessible."""
    try:
        subprocess.run(['pandoc', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_md_to_docx(source_dir, output_dir):
    """
    Converts all .md files in source_dir to .docx in output_dir using Pandoc.
    """
    if not check_pandoc():
        print("Error: Pandoc not found. Please install Pandoc (https://pandoc.org/) and add it to your PATH.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    print(f"Scanning directory: {source_dir}")
    
    count = 0
    for filename in os.listdir(source_dir):
        if filename.endswith(".md"):
            input_path = os.path.join(source_dir, filename)
            
            # Construct output filename
            # Replace extension .md with .docx
            output_filename = os.path.splitext(filename)[0] + ".docx"
            output_path = os.path.join(output_dir, output_filename)
            
            print(f"Converting: {filename} -> {output_filename}")
            
            try:
                # Basic Pandoc command: pandoc input.md -o output.docx
                # You can add --reference-doc=custom.docx here if needed
                cmd = ['pandoc', input_path, '-o', output_path]
                
                subprocess.run(cmd, check=True)
                print(f"  Success.")
                count += 1
            except subprocess.CalledProcessError as e:
                print(f"  Failed: {e}")
            except Exception as e:
                print(f"  Error: {e}")

    print(f"\nConversion complete. {count} files processed.")
    print(f"Output files are in: {output_dir}")

if __name__ == "__main__":
    # Settings
    cwd = os.getcwd()
    
    # Default directories relative to script location
    # Assuming the script is run from the project root or code directory
    target_dir = os.path.join(cwd, 'google_md')
    output_dir = os.path.join(cwd, 'word_output')
    
    if os.path.exists(target_dir):
        convert_md_to_docx(target_dir, output_dir)
    else:
        print(f"Source directory not found: {target_dir}")
        print("Please ensure you are running this script from the correct location.")
