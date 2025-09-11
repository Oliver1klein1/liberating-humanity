#!/usr/bin/env python3
"""
Create a properly formatted EPUB file for Amazon KDP
Ensures mimetype is first file and uncompressed
"""

import zipfile
import os
import shutil
from pathlib import Path

def create_epub():
    epub_name = "LiberatingHumanity.epub"
    
    # Remove existing EPUB
    if os.path.exists(epub_name):
        os.remove(epub_name)
    
    # Create EPUB with proper structure
    with zipfile.ZipFile(epub_name, 'w', zipfile.ZIP_DEFLATED) as epub:
        # Add mimetype first (uncompressed, no extra field)
        epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF files
        meta_inf_dir = Path('epub/META-INF')
        for file_path in meta_inf_dir.rglob('*'):
            if file_path.is_file():
                arcname = f"META-INF/{file_path.relative_to(meta_inf_dir)}"
                epub.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)
        
        # Add OEBPS files
        oebps_dir = Path('epub/OEBPS')
        for file_path in oebps_dir.rglob('*'):
            if file_path.is_file():
                arcname = f"OEBPS/{file_path.relative_to(oebps_dir)}"
                epub.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)
    
    # Verify file was created
    if os.path.exists(epub_name):
        file_size = os.path.getsize(epub_name)
        print(f"EPUB created successfully: {epub_name}")
        print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        
        # Verify mimetype is first
        with zipfile.ZipFile(epub_name, 'r') as epub:
            file_list = epub.namelist()
            if file_list[0] == 'mimetype':
                print("✓ Mimetype file is correctly positioned as first file")
            else:
                print(f"✗ Warning: First file is '{file_list[0]}', not 'mimetype'")
                
            # Check mimetype content
            mimetype_content = epub.read('mimetype').decode('utf-8')
            if mimetype_content == 'application/epub+zip':
                print("✓ Mimetype content is correct")
            else:
                print(f"✗ Warning: Mimetype content is '{mimetype_content}'")
        
        return True
    else:
        print("✗ Failed to create EPUB file")
        return False

if __name__ == "__main__":
    create_epub()
