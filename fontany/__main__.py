"""FontAny CLI entry point."""
import sys
from .core import process, color, OUT_DIR


BANNER = r"""
  ███████╗ ██████╗ ███╗   ██╗████████╗ █████╗ ███╗   ██╗██╗   ██╗
  ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗████╗  ██║╚██╗ ██╔╝
  █████╗  ██║   ██║██╔██╗ ██║   ██║   ███████║██╔██╗ ██║ ╚████╔╝
  ██╔══╝  ██║   ██║██║╚██╗██║   ██║   ██╔══██║██║╚██╗██║  ╚██╔╝
  ██║     ╚██████╔╝██║ ╚████║   ██║   ██║  ██║██║ ╚████║   ██║
  ╚═╝      ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝
"""


def print_banner():
    print(color(BANNER, "cyan"))
    print(color("      ⚡ FontAny - MT Manager Converter ⚡", "cyan"))
    print(color("      ─────────────────────────────────", "yellow"))
    print()


def print_help():
    print_banner()
    print("Usage:   fontany <fonts_folder>")
    print()
    print("Examples:")
    print("  fontany /sdcard/Download/MyFonts")
    print("  fontany /storage/emulated/0/webbox/sirius.menu/fonts/")
    print()
    print(f"Output:  {OUT_DIR}")
    print()
    print("Formats: .ttf  .otf  .ttc  .woff  .woff2")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)

    print_banner()
    process(sys.argv[1])


if __name__ == "__main__":
    main()
