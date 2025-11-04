#!/usr/bin/env python3
"""
EPUB Creation Script for KDP
Creates properly formatted EPUB files with mimetype first (uncompressed)
"""

import zipfile
import os
import sys
from pathlib import Path

def create_epub(epub_dir, output_file, epub_version="kdp"):
    """
    Create EPUB file from directory structure
    
    Args:
        epub_dir: Path to EPUB directory (containing mimetype, META-INF, OEBPS)
        output_file: Output EPUB file path
        epub_version: "kdp" for standard KDP, "kindle" for Kindle-specific
    """
    epub_path = Path(epub_dir)
    output_path = Path(output_file)
    
    # Remove existing file if it exists
    if output_path.exists():
        output_path.unlink()
    
    # Create ZIP file with correct compression
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as epub:
        # CRITICAL: Add mimetype first, uncompressed (EPUB spec requirement)
        mimetype_path = epub_path / "mimetype"
        if not mimetype_path.exists():
            raise FileNotFoundError(f"mimetype file not found at {mimetype_path}")
        
        # Add mimetype with no compression (store only)
        epub.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF directory
        meta_inf = epub_path / "META-INF"
        if meta_inf.exists():
            for root, dirs, files in os.walk(meta_inf):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(epub_path)
                    epub.write(file_path, arcname)
        
        # Add OEBPS directory
        oebps = epub_path / "OEBPS"
        if oebps.exists():
            # Sort files for consistent ordering
            all_files = []
            for root, dirs, files in os.walk(oebps):
                for file in files:
                    # Skip Python scripts and other non-book files
                    if file.endswith(('.py', '.pyc', '__pycache__')):
                        continue
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(epub_path)
                    all_files.append((file_path, arcname))
            
            # Sort for consistent output
            all_files.sort(key=lambda x: str(x[1]))
            
            for file_path, arcname in all_files:
                epub.write(file_path, arcname)
    
    print(f"Created EPUB: {output_path}")
    print(f"  Size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
    return output_path

def main():
    base_dir = Path(__file__).parent
    epub_dir = base_dir / "epub"
    
    # Create standard KDP EPUB
    print("Creating standard KDP EPUB...")
    kdp_epub = create_epub(epub_dir, base_dir / "Liberating-Humanity-KDP.epub", "kdp")
    
    # Create Kindle-specific EPUB (same structure but may have different optimizations)
    print("\nCreating Kindle-specific EPUB...")
    kindle_epub = create_epub(epub_dir, base_dir / "Liberating-Humanity-Kindle.epub", "kindle")
    
    print("\nEPUB files created successfully!")
    print(f"  KDP: {kdp_epub}")
    print(f"  Kindle: {kindle_epub}")

if __name__ == "__main__":
    main()

