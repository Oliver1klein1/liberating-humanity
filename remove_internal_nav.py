#!/usr/bin/env python3
"""
Remove internal navigation from all XHTML files
Keep only the external navigation from preview.html
"""

import os
import re
from pathlib import Path

def remove_internal_navigation(file_path):
    """Remove the internal navigation block from an XHTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the navigation block and script
        nav_pattern = r'\s*<nav class="navigation".*?</nav>\s*<script type="text/javascript">.*?</script>'
        
        # Remove the navigation block
        updated_content = re.sub(nav_pattern, '', content, flags=re.DOTALL)
        
        # Clean up any extra whitespace before closing body tag
        updated_content = re.sub(r'\s+</body>', '\n</body>', updated_content)
        
        # Write back if content changed
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✓ Removed navigation from {file_path}")
            return True
        else:
            print(f"- No navigation found in {file_path}")
            return False
            
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    print("Removing internal navigation from XHTML files...")
    print("This will keep only the external 'Previous/Next/Contents' navigation.\n")
    
    oebps_dir = Path('epub/OEBPS')
    xhtml_files = list(oebps_dir.glob('*.xhtml'))
    
    if not xhtml_files:
        print("No XHTML files found in epub/OEBPS/")
        return
    
    print(f"Found {len(xhtml_files)} XHTML files to process:\n")
    
    updated_count = 0
    for file_path in sorted(xhtml_files):
        if remove_internal_navigation(file_path):
            updated_count += 1
    
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"Updated {updated_count} files")
    print(f"Total files processed: {len(xhtml_files)}")
    print(f"\nNow only the external 'Previous/Next/Contents' navigation")
    print(f"from preview.html will be visible.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
