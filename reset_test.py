import os
import re

def recreate_bad_google_md(source_file, target_file):
    print(f"Reading clean file: {source_file}")
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply aggressive escaping to simulate Google Docs export
    # Note: Logic must be reverse of the fix script roughly.
    # We want to turn `\` into `\\`, `_` into `\_`, etc.
    # Order matters! Escape backslash first.
    
    replacements = [
        (r'\\', r'\\\\'),  # \ -> \\
        (r'_', r'\\_'),    # _ -> \_
        (r'=', r'\\='),
        (r'-', r'\\-'),
        (r'\+', r'\\+'),
        (r'\.', r'\\.'),
        (r'\[', r'\\['),
        (r'\]', r'\\]'),
        (r'<', r'\\<'),
        (r'>', r'\\>'),
        # (r'{', r'\\{'), # Google docs might not escape ALL curly braces, but let's be safe
        # (r'}', r'\\}'),
        # (r'\*', r'\\*'), 
    ]
    
    # Note: Naive replacement might double escape if we are not careful.
    # But since we start with CLEAN file, `\` is just `\`.
    
    for char_pat, repl in replacements:
        # regex substitute? Or string replace?
        # char_pat is regex. 
        # But we need to use negative lookbehind/lookahead to avoid re-escaping?
        # No, source file is clean. Just replace.
        content = re.sub(char_pat, repl, content)
        
    print(f"Writing corrupted file: {target_file}")
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    md_dir = os.path.join(os.getcwd(), 'md')
    google_md_dir = os.path.join(os.getcwd(), 'google_md')
    
    source = os.path.join(md_dir, '0.md')
    # Overwrite the damaged 1.md so we have a fresh start for testing
    target = os.path.join(google_md_dir, '1.md') 
    
    if os.path.exists(source):
        recreate_bad_google_md(source, target)
    else:
        print("Source file 0.md not found.")
