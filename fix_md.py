import os
import re

def fix_content(content):
    """
    Applies regex replacements to fix Google Docs export issues AND Pandoc conversion issues.
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
        (r'\\\$', r'$'),       # Replace \$ with $ (Fix for Pandoc docx->md)
        (r'## ---', r'---'),   # Replace ## --- with --- (restore horizontal rule)
    ]
    
    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)
        
    # Prepend YAML header for Word conversion
    yaml_header = "---\noutput: word_document\n---\n\n"
    if not content.startswith("---"):
        content = yaml_header + content
        
    return content

def fix_google_md(directory):
    """
    Scans all .md files in the given directory and fixes formatting issues
    caused by Google Docs export (aggressive escaping).
    """
    print(f"Scanning directory: {directory}")

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            print(f"Processing: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            fixed_content = fix_content(content)
            
            if fixed_content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"  Fixed.")
            else:
                print(f"  No changes needed.")

if __name__ == "__main__":
    target_dir = os.path.join(os.getcwd(), 'google_md')
    if os.path.exists(target_dir):
        fix_google_md(target_dir)
    else:
        print(f"Directory not found: {target_dir}")
