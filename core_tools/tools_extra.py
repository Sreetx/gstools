# main.py
#
# Copyright 2025 Lingga Channel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os, time, sys, subprocess, re, threading, json
from rich import print
from rich.live import Live
from rich.console import Console, Group
from rich.text import Text
from rich.table import Table
from rich import box

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import ANSI
from datetime import datetime
from color.warna import orange
from color.warna import putih
from color.warna import merah
from color.warna import hijau
from color.warna import biru
from color.warna import borange
from color.warna import banorange
from color.warna import bputih
from color.warna import bhijau
from color.warna import bmerah
from color.warna import bbiru
from color.warna import kelabu
from color.warna import borangekelip
from color.warna import banhijau
from color.warna import banmerah
from color.warna import reset
waktu_log = time.strftime('%Y-%m-%d %H:%M:%S')

stop_event = threading.Event()
console = Console()

def loading_animation(teks):
    i = 0
    with Live(refresh_per_second=10, console=console, transient=True) as live:
        while not stop_event.is_set():
            dot = '.' * (i % 5)
            live.update(Text(f"\r {teks}{dot:<5}"))
            time.sleep(0.3)
            i += 1

def run_with_animation(func, teks):
    global loading_thread
    stop_event.clear()
    loading_thread = threading.Thread(target=loading_animation, args=(teks,))
    loading_thread.start()
    try:
        func()
    except ImportError:
        stop_event.set()
        sys.exit()
    finally:
        stop_event.set()
        loading_thread.join()
    stop_event.set()
    loading_thread.join()

from rich.console import Console
from rich.table import Table
from rich import box
import os

console = Console()

def iso_detector(gagal=False):
    global iso_files
    if gagal:
        search_root = ["/media", "/run/media", "/mnt", "/root"]
    else:
        search_root = ["/home"]

    excluded_dirs = {'/proc', '/sys', '/dev', '/run', '/snap', '/boot', '/var'}
    iso_files = []
    i = 1
    file_found_printed = False

    for root_dir in search_root:
        for root, dirs, files in os.walk(root_dir):
            if any(root.startswith(ex) for ex in excluded_dirs):
                continue
            for file in files:
                if file.lower().endswith(".iso"):
                    iso_path = os.path.join(root, file)
                    iso_files.append(iso_path)

                    if not file_found_printed:
                        console.print("\n[bold green] * [/bold green]File Found:")
                        file_found_printed = True
                    try:
                        size_bytes = os.path.getsize(iso_path)
                        size_mb = size_bytes / (1024 * 1024)
                        size_str = f"{size_mb:.1f} MB"
                    except Exception as e:
                        size_str = "Unknown"

                    hasil_cari_iso = Table(header_style="green", box=box.ROUNDED, border_style="green")
                    hasil_cari_iso.add_column("No", justify="center", style="bold white")
                    hasil_cari_iso.add_column("File Path", style="orange1")
                    hasil_cari_iso.add_column("Size", justify="center", style="bold white")

                    hasil_cari_iso.add_row(f"\r[bold white]{i}[/bold white]", f"[orange1]{iso_path}[/orange1]", f"[blue]{size_str}[/blue]")
                    console.print(hasil_cari_iso)
                    i += 1

    if not iso_files:
        console.print("\n[bold red] ! [/bold red]File Not Found in [#3ff568]/home[/#3ff568]")
        text = """[bright_black][[/bright_black][bold orange1]#[/bold orange1][bright_black]][/bright_black] Options:
[bright_black] ([/bright_black][bold green]1[/bold green][bright_black])[/bright_black] Scan on [#3ff568]/media[/#3ff568], [#3ff568]/run/media[/#3ff568], and [#3ff568]/mnt[/#3ff568] [bright_black](a little bit longer)[/bright_black]
[bright_black] ([/bright_black][bold green]2[/bold green][bright_black])[/bright_black] Continue without scanning files (As long as you remember where you saved your ISO file)"""
        console.print(text)

        stop_event.set()
        loading_thread.join()

        global pilihan
        pilihan = input(f" ({borange}>{reset}): ")
        if pilihan.lower() == "1":
            run_with_animation(lambda: iso_detector(gagal=True), f"{borange}~ {reset}Running an extended scan")
        else:
            pass


def external_part_detector():
    output = subprocess.check_output(["lsblk", "-dno", "NAME,RM,SIZE"], text=True)
    lines = output.strip().split('\n')
    external_disk = []

    for line in lines:
        parts = line.split(None, 2)
        name = parts[0].strip()
        removable_status = parts[1].strip()
        size = parts[2].strip()

        if removable_status == '1':
            removable_status = " [bright_black]([/bright_black][bold green]>[/bold green][bright_black])[/bright_black] Removable (Flashdisk, SDCard, etc.)"
        else:
            removable_status = " [bright_black]([/bright_black][bold red]<[/bold red][bright_black])[/bright_black] Removable, NOT RECOMMENDED to flash (Protable HDD or SSD, SDCard, etc.)"

        if name.startswith('sd') and not name.startswith('sda') or name.startswith('mmcblk0'):
            external_disk.append((name, removable_status, size))
    if not external_disk:
        print("\n[bold red]*[/bold red] No external disk detected"); time.sleep(1.5)
        print("[bold red]*[/bold red] Exit, Have a nice day!");sys.exit()
    print("\n[bold green]#[/bold green] External disk detected:")
    for name, rs, size in external_disk:
        print(f"[bold orange1] • [/bold orange1][#3ff568]/dev/{name:<4} [/#3ff568]([blue]{size:^6}[/blue]) [orange1]>[/orange1][bold white]{rs}[/bold white]")

def list_iso_file():
    global iso_files
    while True:
        try:
            choise = int(input(f"{bputih}({reset}{borange}>{reset}{bputih}){reset} Select ISO File (number): "))
            index = choise - 1
            if 0 <= index < len(iso_files):
                return iso_files[index]
            else:
                print("[bold red] ! [/bold red] Not listed");sys.exit()
        except ValueError:
            print("[bold red] ! [/bold red] Not listed");sys.exit()
def burner_iso():
    try:
        print("\n[[bold orange1]#[/bold orange1]] Easy Iso Bruner, Create your bootable disk make easier!")
        print("[bold orange1] * [/bold orange1]Start searching for available ISO files.")
        run_with_animation(iso_detector, f"{borange}~ {reset}Searching ISO file")
        external_part_detector()

        if pilihan.lower() == "2":
            iso_file= input(f"{bputih}({reset}{borange}>{reset}{bputih}){reset} Select ISO File (path): ")
        else:
            iso_file = list_iso_file()

        if not os.path.exists(iso_file):
            print("[bold red] ! [/bold red] ISO File not found!"); sys.exit()

        target_disk_ansi = ANSI(f"{bputih}({reset}{borange}>{reset}{bputih}){reset} Target Disk (External Disk): ")
        target_disk = prompt(target_disk_ansi)
        target_disk = target_disk.strip()
        if not os.path.exists(target_disk):
            print("[bold red] ! [/bold red] External drive not found!"); sys.exit()

        #Detail
        iso_split = iso_file.split("/")[-1]
        print("\n[[bold green]INFO[/bold green]] ISO File: [#3ff568]"+iso_split+"[/#3ff568]")
        print("[[bold green]INFO[/bold green]] Target Device: [orange1]"+target_disk+"[/orange1]")
        print("[bold green] * [/bold green]This will format all contents of the inserted external disk (Target Device)")
        konfirmasi = ANSI(f"{bputih}({reset}{borange}?{reset}{bputih}){reset}{bputih} Do you want to continue? (y/n): {reset}")
        konfirmasi = prompt(konfirmasi)
        if konfirmasi.lower() == "y":
            print("\n[bold green] ~ [/bold green] Running DD (Disk Drive) ..."); time.sleep(2)
            subprocess.run(["sudo", "dd", f"if={iso_file}", f"of={target_disk}", "bs=6M", "status=progress"], check=True)
            print("[#3ff568][#] Done![/#3ff568]"); time.sleep(3); sys.exit()
        else:
            print("[bright_black][[/bright_black][bold green]*[/bold green][bright_black]][/bright_black] Exit, Have a nice day!");sys.exit()

    except KeyboardInterrupt:
        print("[bright_black][[/bright_black][bold green]*[/bold green][bright_black]][/bright_black] Exit, Have a nice day!");sys.exit()

def list_mountpoint_external():
    o = subprocess.run(['lsblk', '-rno', 'NAME,MOUNTPOINT,SIZE'], capture_output=True, text=True)
    lines = o.stdout.strip().split('\n')
    external_part = []
    for line in lines:
        parts = line.split(None, 2)
        if len(parts) != 3:
            continue
        name = parts[0].strip()
        mountpoint = parts[1].strip()
        size = parts[2].strip()
        if mountpoint in ("[SWAP]", "-") or not os.path.isdir(mountpoint):
            continue
        if (
            (name.startswith('sd') and name[-1].isdigit() and not name.startswith('sda')) or
            (name.startswith('mmcblk0'))
        ):
            external_part.append((name, mountpoint, size))

    return external_part
    if not external_part:
        print("\n[bold red]*[/bold red] No external part detected"); time.sleep(1.5)
        print("bold orange1]*[/bold orange1] Please insert and manually mount your external disk"); time.sleep(0.5)
        print("[bold red]*[/bold red] Exit, Have a nice day!");sys.exit()













