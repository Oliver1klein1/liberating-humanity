#!/usr/bin/env python3
"""
Analyze which images are used and which are unused in the EPUB
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def find_image_references(epub_dir):
    """Find all image references in XHTML files"""
    oebps = Path(epub_dir) / "OEBPS"
    references = set()
    
    # Find all image references in XHTML files
    for xhtml_file in oebps.glob("*.xhtml"):
        content = xhtml_file.read_text(encoding='utf-8')
        # Find img src attributes
        img_patterns = [
            r'src=["\']([^"\']+\.(jpg|jpeg|png))["\']',
            r'url\(["\']?([^"\']+\.(jpg|jpeg|png))["\']?\)',
        ]
        for pattern in img_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                img_path = match[0] if isinstance(match, tuple) else match
                # Handle relative paths like ../../filename.jpg
                if img_path.startswith('../'):
                    # Resolve relative to OEBPS
                    ref = Path(img_path).name
                else:
                    ref = img_path
                references.add(ref.lower())
    
    return references

def get_all_images(epub_dir):
    """Get all image files in OEBPS directory"""
    oebps = Path(epub_dir) / "OEBPS"
    images = {}
    for img_file in oebps.glob("*"):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            images[img_file.name.lower()] = img_file
    return images

def main():
    epub_dir = Path("epub")
    oebps = epub_dir / "OEBPS"
    
    # Get all images
    all_images = get_all_images(epub_dir)
    print(f"Total images found: {len(all_images)}")
    
    # Get references
    references = find_image_references(epub_dir)
    print(f"Images referenced in content: {len(references)}")
    
    # Find unused images
    unused = []
    used = []
    for img_name_lower, img_path in all_images.items():
        img_name = img_path.name
        if img_name_lower in references or img_name_lower in ['cover.jpg']:  # cover.jpg is in manifest
            used.append(img_name)
        else:
            unused.append(img_name)
    
    print(f"\nUsed images ({len(used)}):")
    for img in sorted(used):
        print(f"  - {img}")
    
    print(f"\nUnused images ({len(unused)}):")
    for img in sorted(unused):
        print(f"  - {img}")
    
    # Create unused_images directory
    unused_dir = oebps / "unused_images"
    unused_dir.mkdir(exist_ok=True)
    
    # Move unused images
    print(f"\nMoving {len(unused)} unused images to unused_images/...")
    for img_name in unused:
        src = oebps / img_name
        dst = unused_dir / img_name
        if src.exists():
            src.rename(dst)
            print(f"  Moved: {img_name}")

if __name__ == "__main__":
    main()

