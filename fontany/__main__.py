"""CLI entry point."""
import sys
from .core import run


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print("FontAny - Convert fonts to MT Manager (MTZ) format")
        print()
        print("Usage:")
        print("  fontany <fonts_folder>")
        print()
        print("Example:")
        print("  fontany /sdcard/Download/MyFonts")
        print("  fontany /storage/emulated/0/webbox/sirius.menu/fonts/")
        print()
        print("Output: /sdcard/FontAny/")
        sys.exit(0)

    run(sys.argv[1])


if __name__ == "__main__":
    main()
