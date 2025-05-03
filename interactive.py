#!/usr/bin/env python3


import os
import glob
from datetime import datetime
import sys
import termios
import tty
import shutil

FONT_RESET = "\033[0m"
FONT_BOLD = "\033[1m"
FONT_INVERTED = "\033[30;47m"

clear = lambda: os.system("clear")
term_size = lambda: shutil.get_terminal_size((80, 20))
term_rows = term_size().lines - 5
files = []


def populate_files():
    global files

    home = os.path.expanduser("~")
    pattern = os.path.join(home, ".steam/steam/steamapps/common/Oblivion/Data/*.*")

    unsorted = []
    for ext in ["esm", "esp"]:
        unsorted.extend(glob.glob(pattern.replace("*.*", f"*.{ext}")))

    files = sorted(unsorted, key=lambda x: os.path.getmtime(x))


def display_files(selected_idx=None, offset=0, dragging=False):
    """Display files with optional selection highlighting and scrolling"""
    global term_rows
    clear()
    print("Use ENTER/UP/DOWN to move selection, press 'q' to finish")

    terminal_rows = term_rows  # Reserve space for header/footer
    visible_files = files[offset : offset + terminal_rows]

    print(
        f"{FONT_BOLD}↑↑↑ more files loaded earlier ↑↑↑{FONT_RESET}"
        if offset > 0
        else ""
    )

    for idx, file in enumerate(visible_files, start=offset):
        name = os.path.basename(file)
        drg = ">" if idx == selected_idx and dragging else " "
        hl_start = FONT_INVERTED if idx == selected_idx else ""
        hl_ends = FONT_RESET if idx == selected_idx else ""

        print(f"{hl_start}{drg} {name}{hl_ends}")

    print(
        f"{FONT_BOLD}↓↓↓ more files loaded later ↓↓↓{FONT_RESET}"
        if offset + terminal_rows < len(files)
        else ""
    )


def get_key():
    """Get a single key press"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        # Handle arrow keys (3-character sequence)
        if ch == "\x1b":
            ch = sys.stdin.read(2)
            if ch == "[A":
                return "up"
            elif ch == "[B":
                return "down"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def interactive_sort():
    """Interactive file sorting interface with scrolling support"""
    global term_rows

    def swap():
        if dragging:
            files[idx], files[idx + 1] = files[idx + 1], files[idx]

    idx = 0
    dragging = False
    scroll_offset = 0

    while True:
        # Adjust scroll offset to keep selection visible
        if idx < scroll_offset:
            scroll_offset = idx
        elif idx >= scroll_offset + term_rows:
            scroll_offset = idx - term_rows + 1

        display_files(idx, scroll_offset, dragging)
        key = get_key()

        if key == "up" and idx > 0:
            idx -= 1
            swap()
        elif key == "down" and idx < len(files) - 1:
            swap()
            idx += 1
        elif key == "\r":  # ENTER
            dragging = not dragging
        elif key == "q":
            clear()
            print("\n  are you ready? (Y/n)")
            if get_key() == "y":
                print
                break


def update_timestamps():
    """Update modification timestamps based on order (first = oldest)"""

    start_time = datetime.strptime("2001-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
    interval = 86400  # 1 day in seconds

    print("\n  new modification times:\n")

    for idx, file in enumerate(files):
        new_time = start_time.timestamp() + (idx * interval)
        os.utime(file, (new_time, new_time))
        mod_time_str = datetime.fromtimestamp(new_time).strftime("%Y-%m-%d")
        print(f"{mod_time_str}: {os.path.basename(file)}")


def main():
    print("Loading files...")
    populate_files()
    interactive_sort()
    update_timestamps()


if __name__ == "__main__":
    main()
