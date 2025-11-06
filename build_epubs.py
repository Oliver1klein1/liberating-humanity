import re
import shutil
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


PROJECT_ROOT = Path(__file__).parent
EPUB_ROOT = PROJECT_ROOT / "epub"
OUTPUT_LOCATIONS = [PROJECT_ROOT, PROJECT_ROOT / "dist"]
STANDARD_FILENAME = "Liberating-Humanity.epub"
KDP_FILENAME = "Liberating-Humanity-KDP.epub"


def ensure_output_dirs() -> None:
    for location in OUTPUT_LOCATIONS:
        if location == PROJECT_ROOT:
            continue
        location.mkdir(exist_ok=True)


def clone_epub_tree(destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(EPUB_ROOT, destination)


def add_kdp_mode_to_bodies(oebps_path: Path) -> None:
    body_tag_pattern = re.compile(r"<body([^>]*)>", re.IGNORECASE)

    def inject_kdp_mode(match: re.Match[str]) -> str:
        attributes = match.group(1)

        if re.search(r"class\s*=\s*\"[^\"]*kdp-mode[^\"]*\"", attributes, re.IGNORECASE) or \
           re.search(r"class\s*=\s*'[^']*kdp-mode[^']*'", attributes, re.IGNORECASE):
            return f"<body{attributes}>"

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

        prefix = "" if attributes.startswith((" ", "\n", "\t", "\r")) else " "
        return f"<body{prefix}class=\"kdp-mode\"{attributes}>"

    for xhtml_file in sorted(oebps_path.glob("*.xhtml")):
        text = xhtml_file.read_text(encoding="utf-8")
        updated_text, count = body_tag_pattern.subn(inject_kdp_mode, text, count=1)
        if count:
            xhtml_file.write_text(updated_text, encoding="utf-8")


def create_epub(source_dir: Path, output_file: Path) -> None:
    mimetype_path = source_dir / "mimetype"
    meta_inf_path = source_dir / "META-INF"
    oebps_path = source_dir / "OEBPS"

    with ZipFile(output_file, "w") as epub_zip:
        epub_zip.write(mimetype_path, "mimetype", compress_type=ZIP_STORED)

        for folder in (meta_inf_path, oebps_path):
            for path in sorted(folder.rglob("*")):
                if path.is_dir():
                    continue
                arcname = path.relative_to(source_dir)
                epub_zip.write(path, arcname.as_posix(), compress_type=ZIP_DEFLATED)


def build_epubs() -> None:
    ensure_output_dirs()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Standard edition
        standard_path = tmp_path / "standard"
        clone_epub_tree(standard_path)
        standard_epub = tmp_path / STANDARD_FILENAME
        create_epub(standard_path, standard_epub)
        for location in OUTPUT_LOCATIONS:
            shutil.copy2(standard_epub, location / STANDARD_FILENAME)

        # Kindle (KDP) edition
        kdp_path = tmp_path / "kdp"
        clone_epub_tree(kdp_path)
        add_kdp_mode_to_bodies(kdp_path / "OEBPS")
        kdp_epub = tmp_path / KDP_FILENAME
        create_epub(kdp_path, kdp_epub)
        for location in OUTPUT_LOCATIONS:
            shutil.copy2(kdp_epub, location / KDP_FILENAME)


if __name__ == "__main__":
    build_epubs()

