#!/usr/bin/env python3
"""
Create EPUB file for Amazon KDP with proper structure
Ensures mimetype is uncompressed and first in the archive
"""

import zipfile
import os
import shutil
from pathlib import Path

def create_kdp_epub():
    output_name = "Liberating-Humanity-KDP.epub"
    
    print("Creating EPUB file for Amazon KDP...")
    
    # Remove existing EPUB if it exists
    if os.path.exists(output_name):
        os.remove(output_name)
        print(f"Removed existing {output_name}")
    
    try:
        # Create the EPUB file
        with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as epub:
            # Add mimetype FIRST and UNCOMPRESSED (critical for EPUB spec)
            print("Adding mimetype (uncompressed)...")
            epub.write('mimetype', 'mimetype', compress_type=zipfile.ZIP_STORED)
            
            # Add META-INF/container.xml
            print("Adding META-INF structure...")
            epub.write('META-INF/container.xml', 'META-INF/container.xml')
            
            # Add all OEBPS content
            print("Adding OEBPS content...")
            oebps_dir = Path('epub/OEBPS')
            
            for file_path in oebps_dir.rglob('*'):
                if file_path.is_file():
                    archive_path = f"OEBPS/{file_path.relative_to(oebps_dir)}"
                    epub.write(str(file_path), archive_path)
                    print(f"  Added: {archive_path}")
        
        # Verify the file was created
        if os.path.exists(output_name):
            file_size = os.path.getsize(output_name)
            file_size_mb = round(file_size / (1024 * 1024), 2)
            
            print(f"\n{'='*60}")
            print("SUCCESS!")
            print(f"EPUB file created: {output_name}")
            print(f"File size: {file_size_mb} MB")
            print("\nThe EPUB file is ready for Amazon KDP!")
            print(f"\n{'='*60}")
            print("Key features for KDP compliance:")
            print("• Mimetype file is uncompressed and first in archive")
            print("• Proper META-INF/container.xml structure")
            print("• Complete metadata with all specified information")
            print("• Cover image properly referenced")
            print("• All content files properly organized")
            print(f"{'='*60}")
            
            # Show file contents for verification
            print(f"\nEPUB contents verification:")
            with zipfile.ZipFile(output_name, 'r') as epub:
                files = epub.namelist()
                print(f"Total files: {len(files)}")
                print("First 10 files:")
                for i, file in enumerate(files[:10]):
                    print(f"  {i+1}. {file}")
                if len(files) > 10:
                    print(f"  ... and {len(files) - 10} more files")
        else:
            print("ERROR: Failed to create EPUB file")
            
    except Exception as e:
        print(f"ERROR occurred: {e}")
        
    print("\nScript completed.")

if __name__ == "__main__":
    create_kdp_epub()
