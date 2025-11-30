#!/usr/bin/env python3
"""
EPUB Build Script for Liberating Humanity
Creates two EPUB files:
1. Standard EPUB for Gumroad
2. KDP EPUB with kdp-mode class for Amazon Kindle Direct Publishing

Ensures:
- mimetype file is first and uncompressed (EPUB spec requirement)
- All CSS styles are preserved
- KDP version has class="kdp-mode" on body elements
- Proper metadata and cover image
"""

import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


PROJECT_ROOT = Path(__file__).parent
EPUB_ROOT = PROJECT_ROOT / "epub"
OUTPUT_LOCATIONS = [PROJECT_ROOT, PROJECT_ROOT / "dist"]
STANDARD_FILENAME = "Liberating-Humanity.epub"
KDP_FILENAME = "Liberating-Humanity-KDP.epub"
EPUBCHECK_JAR = PROJECT_ROOT / "epubcheck-5.2.1" / "epubcheck.jar"


def ensure_output_dirs() -> None:
    """Create output directories if they don't exist."""
    for location in OUTPUT_LOCATIONS:
        if location == PROJECT_ROOT:
            continue
        location.mkdir(exist_ok=True)


def clone_epub_tree(destination: Path) -> None:
    """Clone the EPUB directory structure to a temporary location."""
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(EPUB_ROOT, destination)


def fix_image_paths(oebps_path: Path) -> None:
    """
    Convert absolute image paths (/cover.jpg) to relative paths (cover.jpg)
    in all XHTML and HTML files. EPUBs require relative paths.
    """
    for file_path in sorted(oebps_path.glob("*.xhtml")) + sorted(oebps_path.glob("*.html")):
        text = file_path.read_text(encoding="utf-8")
        original_text = text
        
        # Convert absolute image paths (/cover.jpg) to relative (cover.jpg)
        # Match src="/filename.jpg" or src='/filename.jpg'
        text = re.sub(
            r'src=["\']\/([^"\']+\.(jpg|jpeg|png|gif|svg|css|js))["\']',
            r'src="\1"',
            text,
            flags=re.IGNORECASE
        )
        
        # Also handle href attributes for links to other files
        text = re.sub(
            r'href=["\']\/([^"\']+\.(xhtml|html))["\']',
            r'href="\1"',
            text,
            flags=re.IGNORECASE
        )
        
        if text != original_text:
            file_path.write_text(text, encoding="utf-8")
            print(f"  Fixed image paths in {file_path.name}")


def add_kdp_mode_to_bodies(oebps_path: Path) -> None:
    """
    Add class="kdp-mode" to all <body> elements in XHTML files.
    This is used to hide navigation buttons in Kindle Previewer.
    """
    body_tag_pattern = re.compile(r"<body([^>]*)>", re.IGNORECASE)

    def inject_kdp_mode(match: re.Match[str]) -> str:
        attributes = match.group(1)

        # Check if kdp-mode already exists
        if re.search(r"class\s*=\s*\"[^\"]*kdp-mode[^\"]*\"", attributes, re.IGNORECASE) or \
           re.search(r"class\s*=\s*'[^']*kdp-mode[^']*'", attributes, re.IGNORECASE):
            return f"<body{attributes}>"

        # Handle double-quoted class attribute
        double_quote_match = re.search(r"class\s*=\s*\"([^\"]*)\"", attributes)
        if double_quote_match:
            existing = double_quote_match.group(1).strip()
            new_classes = "kdp-mode" if not existing else f"kdp-mode {existing}"
            new_attributes = attributes.replace(
                double_quote_match.group(0),
                f'class="{new_classes}"',
                1,
            )
            return f"<body{new_attributes}>"

        # Handle single-quoted class attribute
        single_quote_match = re.search(r"class\s*=\s*'([^']*)'", attributes)
        if single_quote_match:
            existing = single_quote_match.group(1).strip()
            new_classes = "kdp-mode" if not existing else f"kdp-mode {existing}"
            new_attributes = attributes.replace(
                single_quote_match.group(0),
                f"class='{new_classes}'",
                1,
            )
            return f"<body{new_attributes}>"

        # No existing class attribute, add one
        prefix = "" if attributes.startswith((" ", "\n", "\t", "\r")) else " "
        return f"<body{prefix}class=\"kdp-mode\"{attributes}>"

    # Process all XHTML files
    for xhtml_file in sorted(oebps_path.glob("*.xhtml")):
        text = xhtml_file.read_text(encoding="utf-8")
        updated_text, count = body_tag_pattern.subn(inject_kdp_mode, text, count=1)
        if count:
            xhtml_file.write_text(updated_text, encoding="utf-8")
            print(f"  Added kdp-mode to {xhtml_file.name}")


def create_epub(source_dir: Path, output_file: Path) -> None:
    """
    Create an EPUB file from the source directory.
    CRITICAL: mimetype must be first and uncompressed (ZIP_STORED).
    """
    mimetype_path = source_dir / "mimetype"
    meta_inf_path = source_dir / "META-INF"
    oebps_path = source_dir / "OEBPS"

    if not mimetype_path.exists():
        raise FileNotFoundError(f"mimetype file not found at {mimetype_path}")

    with ZipFile(output_file, "w") as epub_zip:
        # CRITICAL: Add mimetype FIRST and UNCOMPRESSED (EPUB spec requirement)
        epub_zip.write(mimetype_path, "mimetype", compress_type=ZIP_STORED)
        
        # Add META-INF directory
        if meta_inf_path.exists():
            for path in sorted(meta_inf_path.rglob("*")):
                if path.is_dir():
                    continue
                arcname = path.relative_to(source_dir)
                epub_zip.write(path, arcname.as_posix(), compress_type=ZIP_DEFLATED)
        
        # Add OEBPS directory (all content files)
        if oebps_path.exists():
            for path in sorted(oebps_path.rglob("*")):
                if path.is_dir():
                    continue
                # Skip Python scripts and other non-book files
                if path.suffix in ('.py', '.pyc') or '__pycache__' in path.parts:
                    continue
                arcname = path.relative_to(source_dir)
                epub_zip.write(path, arcname.as_posix(), compress_type=ZIP_DEFLATED)


def run_epubcheck(epub_path: Path) -> bool:
    """Run epubcheck validation on the EPUB file."""
    if not EPUBCHECK_JAR.exists():
        print(f"  WARNING: epubcheck.jar not found at {EPUBCHECK_JAR}")
        print("  Skipping epubcheck validation.")
        return False
    
    try:
        result = subprocess.run(
            ["java", "-jar", str(EPUBCHECK_JAR), str(epub_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"  ✓ epubcheck passed for {epub_path.name}")
            return True
        else:
            print(f"  ✗ epubcheck found issues in {epub_path.name}:")
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"  WARNING: epubcheck timed out for {epub_path.name}")
        return False
    except Exception as e:
        print(f"  WARNING: Could not run epubcheck: {e}")
        return False


def build_epubs() -> None:
    """Build both standard and KDP EPUB files."""
    print("Building EPUB files for Liberating Humanity...")
    print(f"Source: {EPUB_ROOT}")
    print()
    
    ensure_output_dirs()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Standard EPUB for Gumroad
        print("Creating standard EPUB (Gumroad)...")
        standard_path = tmp_path / "standard"
        clone_epub_tree(standard_path)
        fix_image_paths(standard_path / "OEBPS")
        standard_epub = tmp_path / STANDARD_FILENAME
        create_epub(standard_path, standard_epub)
        
        # Copy to output locations
        for location in OUTPUT_LOCATIONS:
            output_path = location / STANDARD_FILENAME
            shutil.copy2(standard_epub, output_path)
            print(f"  Created: {output_path}")
            print(f"  Size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Run epubcheck on standard EPUB
        run_epubcheck(standard_epub)
        print()

        # KDP EPUB with kdp-mode class
        print("Creating KDP EPUB (Amazon Kindle)...")
        kdp_path = tmp_path / "kdp"
        clone_epub_tree(kdp_path)
        fix_image_paths(kdp_path / "OEBPS")
        add_kdp_mode_to_bodies(kdp_path / "OEBPS")
        kdp_epub = tmp_path / KDP_FILENAME
        create_epub(kdp_path, kdp_epub)
        
        # Copy to output locations
        for location in OUTPUT_LOCATIONS:
            output_path = location / KDP_FILENAME
            shutil.copy2(kdp_epub, output_path)
            print(f"  Created: {output_path}")
            print(f"  Size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Run epubcheck on KDP EPUB
        run_epubcheck(kdp_epub)
        print()

    print("✓ EPUB build complete!")
    print(f"\nOutput files:")
    for location in OUTPUT_LOCATIONS:
        print(f"  {location / STANDARD_FILENAME}")
        print(f"  {location / KDP_FILENAME}")


if __name__ == "__main__":
    build_epubs()

