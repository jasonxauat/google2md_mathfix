import os
import re

def fix_google_md(directory):
    """
    Scans all .md files in the given directory and fixes formatting issues
    caused by Google Docs export (aggressive escaping).
    """
    print(f"Scanning directory: {directory}")
    
    # List of regex replacements. Order matters!
    # Regex note: in python string r'\\', it's one backslash. In regex, \\ matches literal backslash.
    # So r'\\\\' matches literal \\ in text.
    # r'\\\+' matches literal \ followed by +.
    
    replacements = [
        (r'\\\\', r'\\'),      # Replace \\ with \ 
        (r'\\_', r'_'),        # Replace \_ with _
        (r'\\=', r'='),        # Replace \= with =
        (r'\\-', r'-'),        # Replace \- with -
        (r'\\\+', r'+'),       # Replace \+ with +  <-- Fixed regex
        (r'\\\.', r'.'),       # Replace \. with .
        (r'\\\[', r'['),       # Replace \[ with [
        (r'\\\]', r']'),       # Replace \] with ]
        (r'\\<', r'<'),        # Replace \< with <
        (r'\\>', r'>'),        # Replace \> with >
        (r'\\\{', r'{'),       # Replace \{ with {
        (r'\\\}', r'}'),       # Replace \} with }
        (r'\\\*', r'*'),       # Replace \* with *
        (r'\\\|', r'|'),       # Replace \| with |
        (r'## ---', r'---'),   # Replace ## --- with --- (restore horizontal rule)
    ]

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            print(f"Processing: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for pattern, repl in replacements:
                content = re.sub(pattern, repl, content)

            # Prepend YAML header for Word conversion
            yaml_header = "---\noutput: word_document\n---\n\n"
            if not content.startswith("---"):
                content = yaml_header + content
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  Fixed.")
            else:
                print(f"  No changes needed.")

if __name__ == "__main__":
    target_dir = os.path.join(os.getcwd(), 'google_md')
    if os.path.exists(target_dir):
        fix_google_md(target_dir)
    else:
        print(f"Directory not found: {target_dir}")
