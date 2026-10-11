"""Core logic for FontAny."""
import os
import sys
import shutil
import zipfile
import tempfile
from pathlib import Path

OUT_DIR = Path("/sdcard/FontAny")
FONT_EXTS = {".ttf", ".otf", ".ttc", ".woff", ".woff2"}

MTZ_FONT_NAMES = [
    "Roboto-Regular.ttf",
    "Roboto-Bold.ttf",
    "Roboto-Italic.ttf",
    "Roboto-BoldItalic.ttf",
    "Roboto-Light.ttf",
    "Roboto-Medium.ttf",
]


def _c(text, color):
    colors = {"red": "\033[1;31m", "green": "\033[1;32m",
              "yellow": "\033[1;33m", "cyan": "\033[1;36m", "reset": "\033[0m"}
    return f"{colors.get(color, '')}{text}{colors['reset']}"


def to_ttf(src: Path, tmp_dir: Path) -> Path | None:
    """Convert any font file to TTF."""
    ext = src.suffix.lower()
    out = tmp_dir / (src.stem + ".ttf")

    if ext in (".ttf", ".otf", ".ttc"):
        shutil.copy(src, out)
        return out

    if ext == ".woff2":
        try:
            from fontTools.ttLib import TTFont
            font = TTFont(str(src))
            font.flavor = None
            font.save(str(out))
            return out
        except Exception:
            return None

    if ext == ".woff":
        try:
            from fontTools.ttLib import TTFont
            font = TTFont(str(src))
            font.flavor = None
            font.save(str(out))
            return out
        except Exception:
            return None

    return None


def build_mtz(ttf: Path, name: str) -> Path:
    """Build an MTZ file from a TTF."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mtz_path = OUT_DIR / f"{name}.mtz"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        fonts_dir = tmp / "fonts"
        meta_dir = tmp / "META-INF" / "com" / "mt"
        fonts_dir.mkdir(parents=True)
        meta_dir.mkdir(parents=True)

        for fname in MTZ_FONT_NAMES:
            shutil.copy(ttf, fonts_dir / fname)

        (meta_dir / "theme.info").write_text(
            f"name=FontAny - {name}\nauthor=FontAny\nversion=1.0\ntype=font\n",
            encoding="utf-8",
        )

        (tmp / "description.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<theme>\n"
            f"  <name>FontAny - {name}</name>\n"
            "  <author>FontAny</author>\n"
            "  <version>1.0</version>\n"
            "  <type>font</type>\n"
            "</theme>\n",
            encoding="utf-8",
        )

        with zipfile.ZipFile(mtz_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(tmp):
                for f in files:
                    full = Path(root) / f
                    z.write(full, full.relative_to(tmp))

    return mtz_path


def run(folder: str):
    """Main processing function."""
    src = Path(folder).expanduser()
    if not src.is_dir():
        print(_c(f"✗ Folder not found: {src}", "red"))
        sys.exit(1)

    files = [f for f in src.rglob("*")
             if f.is_file() and f.suffix.lower() in FONT_EXTS]

    if not files:
        print(_c("✗ No fonts found", "red"))
        sys.exit(1)

    print(_c(f"[*] Found {len(files)} font(s) in: {src}\n", "cyan"))

    ok, fail = 0, 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for i, f in enumerate(files, 1):
            name = f.stem
            print(f"[{i}/{len(files)}] {f.name} → ", end="", flush=True)
            ttf = to_ttf(f, tmp)
            if ttf:
                build_mtz(ttf, name)
                print(_c(f"✓ {name}.mtz", "green"))
                ok += 1
            else:
                print(_c("✗ failed", "red"))
                fail += 1

    print()
    print(_c(f"✓ Done: {ok} MTZ file(s) in {OUT_DIR}", "green"))
    if fail:
        print(_c(f"✗ Failed: {fail}", "red"))
