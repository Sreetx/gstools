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

import os, time, sys, glob, subprocess, re, signal, threading

from rich import print
from rich.live import Live
from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
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

console = Console()

stop_event = threading.Event()
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


def detect_grub_online():
    try:
        mountd = ["/boot", "/boot/efi"]
        with open("/proc/mounts", "r") as f:
            mounts = [line.split()[1] for line in f.readlines()]
        for mp in mountd:
            if mp in mounts:
                efi_path = mp
                break
        else:
            efi_path = "Unkwown"

        if efi_path == "Unkwown":
            return "Unknown"
        else:
            results = subprocess.run(["efibootmgr", "-v"], stdout=subprocess.PIPE, text=True)
            output = results.stdout
            current_boot = re.search(r'BootCurrent:\s*(\w+)', output)
            if not current_boot:
                return None
            current_id = current_boot.group(1)

            boot_line = None
            for line in output.splitlines():
                if line.startswith(f"Boot{current_id}"):
                    boot_line = line
                    break
            if not boot_line:
                return None

            file_path_match = re.search(r'/\\(EFI\\.*?grubx64\.efi)', boot_line, re.IGNORECASE)
            if not file_path_match:
                file_path_match = re.search(r'/\\(EFI\\.*?shimx64\.efi)', boot_line, re.IGNORECASE)
                if not file_path_match:
                    print("[bold red]![/bold red] EFI File path not found in efibootmgr entry")
                    return None

            file_path = file_path_match.group(1).replace('\\', '/')
            folder_path = os.path.dirname(file_path)

            path = os.path.join(efi_path, folder_path.lstrip('/'))
            os.makedirs(path, exist_ok=True)
            return path
    except KeyboardInterrupt:
        return None
path = detect_grub_online()

def set_prefix():
    #rich experiment
    q = path.split()[0]
    os.makedirs(q, exist_ok=True)
    try:
        print ("[bold orange1] * [/bold orange1]GRUB config file prefix changer"); time.sleep(0.5)
        print ("[bold red] ![/bold red] [orange1]Don't proceed if you don't know what you're doing![/orange1]"); time.sleep(0.5)
        print("[bold orange1] *[/bold orange1] Set your custom grub config file, default [#464646]([/#464646][#3ff568]/boot/grub/grub.cfg[/#3ff568][#464646])[/#464646]"); time.sleep(0.5)
        lss = glob.glob("/boot/grub/*.cfg")
        lss1 = glob.glob("/boot/grub/*.bak")
        print(f"[bold orange1] >[/bold orange1] You config file found: \n[blue] => [/blue][orange1]" + f"[/orange1][blue]\n => [/blue][orange1]".join(lss+lss1)+"[/orange1]"); time.sleep(0.3)
        grub_directory = path.split()[0].strip()
        # Cari prefix configfile GRUB
        find_cfg = os.path.join(grub_directory, "grub.cfg")
        try:
            from core_tools.os_prober import grub_part
        except ImportError:
            print("[bold red]![/bold red] GRUB partition detector [bright_black]([/bright_black][green]core_tools/configures.py[/green] [orange1]>[/orange1] [bold green]grub_part[/bold green][bright_black])[/bright_black] Not found!")
            exit()
        roots = grub_part.strip("(").strip(")").strip()
        try:
            from core_tools.os_prober import uuid_roots
        except ImportError:
            print("[bold red]![/bold red] Find Root UUID [bright_black]([/bright_black][green]core_tools/os_prober.py[/green] [orange1]>[/orange1] [bold green]uuid_roots[/bold green][bright_black])[/bright_black] Not found!")
            exit()
        uuidd = uuid_roots
        if not os.path.exists(find_cfg):
            print("[bold red] ![/bold red] Prefix File Not Found ([orange1]"+find_cfg+"[/orange1])!"); time.sleep(1)
            print("[bold orange1] ~[/bold orange1] Creating file [#3ff568]"+find_cfg+"[/#3ff568]"); time.sleep(2)
            # Jika tidak ditemukan apapun
            # Write GRUB prefix disini
            # Kita mulai direktori build nya dari sini
            find_cfg2 = os.path.join(grub_directory, "grub.cfg")
            os.system("sudo touch "+find_cfg)
            grub_prefix_template = """search --no-floppy --fs-uuid --set=root """+uuidd+"""
set prefix=($root)/boot/grub
configfile $prefix/grub.cfg"""
            with open (find_cfg2, 'w', encoding='utf-8') as hasil_cfg:
                hasil_cfg.write(grub_prefix_template)
            print("[#3ff568][✅] Done ...[/#3ff568]"); time.sleep(3)
        else:
            pass

        try:
            from core_tools.os_prober import prefix_final
        except ImportError:
            print("[bold red]![/bold red] Find GRUB Prefix [bright_black]([/bright_black][green]core_tools/os_prober.py[/green] [orange1]>[/orange1] [bold green]prefix_final[/bold green][bright_black])[/bright_black] Not found!"); sys.exit()

        print("\n[bold green] >[/bold green] GRUB Configfile Used: [#3ff568]"+str(prefix_final)+"[/#3ff568]"); time.sleep(0.5)
        print("[bold green] >[/bold green] You GRUB EFI path: [#3ff568]"+path+"[/#3ff568]"); time.sleep(0.5)
        print("[bold red] *[/bold red] CTRL+C to exit ..."); time.sleep(0.5)
        new_prefix = input (bmerah+">"+reset+putih+" Configfile, default (/boot/grub/grub.cfg) or (grub.cfg): "+reset)
        new_prefix = new_prefix.strip()
        if not new_prefix:
            print("[bold red]! [/bold red] Content cannot be empty"); sys.exit()

        #Kita generate disini
        if not "/" in new_prefix:
            new_prefix = "/"+new_prefix
            nw_prefix = new_prefix.strip()
        print("[bold orange1] >[/bold orange1] Applying changes to [#3ff568]"+find_cfg+"[/#3ff568]"); time.sleep(1.3)
        if new_prefix == "":
            new_prefix = "/boot/grub/grub.cfg"
        print("[bold orange1] >[/bold orange1] Set default prefix [#3ff568]"+new_prefix+"[/#3ff568]"); time.sleep(2)
        path_part = new_prefix.strip().rsplit("/", 1)
        if len(path_part) == 2:
            pathss, grubs_cfg = path_part
            if pathss == '':
                pathss = "/boot/grub"
        else:
            pathss = "/boot/grub"
            grubs_cfg = "grub.cfg"
        if not os.path.exists(os.path.join(pathss, grubs_cfg)):
            #Rollback disini ya Sayori
            print("[bold red] ![/bold red] File [orange1]"+pathss+"/"+grubs_cfg+"[/orange1] Not Found!");time.sleep(3)
            print("[bold orange1] ![/bold orange1] Rollback to [#3ff568]/boot/grub/grub.cfg[/#3ff568]"); time.sleep(1.2)
            pathss = "/boot/grub"
            grubs_cfg = "grub.cfg"

        template_grub_prefix_2 = """search --no-floppy --fs-uuid --set=root """+uuidd+"""
set prefix=($root)"""+pathss+"""
configfile $prefix/"""+grubs_cfg
        print("[bold orange1] ~[/bold orange1] Re-create file [#3ff568]"+find_cfg+"[/#3ff568]"); time.sleep(2.3)
        with open (find_cfg, 'w', encoding='utf-8') as final_cfg:
            final_cfg.write(template_grub_prefix_2)
        print("[#3ff568][✅] Done ...[/#3ff568]"); time.sleep(2)

        #Unsigned distro standalone grub build
        with open("extras/grub-modules.txt") as f:
            modules = f.read().replace("\n", " ").strip()
        find_cfgg = os.path.dirname(find_cfg)
        grubg = os.path.join(find_cfgg, "grubx64.efi").strip()
        shimx = os.path.join(find_cfgg, "shimx64.efi").strip()
        if not os.path.exists(shimx):
            print("\n[bold red] ! [/bold red] shimx64.efi not detected, secure boot is not supported because of bootloader (GRUB)"); time.sleep(1.4)
            print("[bold orange1] # [/bold orange1]GRUB will be made standalone with the config file that was just created. Without GRUB signed support with shim, this config file will be useless at all"); time.sleep(1.4)
            print("[bold orange1] # [/bold orange1]That's why GRUB will be made standalone now"); time.sleep(1.5)
            tes = input(f"{bmerah}(?) {reset}{bputih}Continue? [y/n] {reset}")
            if tes.lower() == "y":
                time.sleep(2)
                subprocess.run(["sudo", "grub-mkstandalone", "-O", "x86_64-efi", f'--modules={modules}', "--locales=id", "--locale-directory=/usr/share/locale", "--fonts=unicode", f"--output={grubg}", f"boot/grub/grub.cfg={find_cfg}"], check=True)
                print("[[bold green]INFO[/bold green]] GRUB standalone successfully created"); time.sleep(1)
        print("[bold green] *[/bold green] Enjoy your new configuration ...");sys.exit()

    except (KeyboardInterrupt):
        print("\n[bold green]*[/bold green] Exit, have a nice day ...");sys.exit()

def install_grub_efi():
    print("[bold orange1] # [/bold orange1]GRUB EFI Installer, [italic]make your job easier![/italic]"); time.sleep(1)
    print("[bold orange1] ~ [/bold orange1]Searching ESP (EFI System Partition) Partition"); time.sleep(2)
    try:
        from core_tools.os_prober import esp_part_checker
        esp = esp_part_checker()
        global device, flags, fstype, mountpoint, size
        device = esp.device
        flags = esp.flags
        fstype = esp.fstype
        mountpoint = esp.mountpoint
        size = esp.size
        uuid_efi = esp.uuid_efi
    except ImportError:
        print("[bold red]![/bold red] Find Root UUID [bright_black]([/bright_black][green]core_tools/os_prober.py[/green] [orange1]>[/orange1] [bold green]esp_part_checker[/bold green][bright_black])[/bright_black] Not found!"); sys.exit()

    header = Text.from_markup("\n[orange1] > [/orange1][bold white italic]EFI Partition Information[/bold white italic]")
    console.print(header)
    esp_infos = Table(show_header=False, box=box.ROUNDED, border_style="green")
    esp_infos.add_row("[green]>[/green]", "[bold white]Devices[/bold white]", device)
    esp_infos.add_row("[green]>[/green]", "[bold white]Mountpoint[/bold white]", mountpoint)
    esp_infos.add_row("[green]>[/green]", "[bold white]Partiton Type[/bold white]", fstype)
    esp_infos.add_row("[green]>[/green]", "[bold white]Flags[/bold white]", "esp, boot")
    esp_infos.add_row("[green]>[/green]", "[bold white]Size[/bold white]", size)
    esp_infos.add_row("[green]>[/green]", "[bold white]UUID[/bold white]", uuid_efi)
    console.print(esp_infos); time.sleep(1)

    linux = '/etc/os-release'
    if os.path.exists(linux):
        if os.path.exists(os.path.join("/", "etc", "os-release")):
            with open(os.path.join("/", "etc", "os-release")) as files:
                for c in files:
                    if c.startswith('PRETTY_NAME'):
                        distro = c.split('=')[1].strip().strip('"')
                    if c.startswith('ID'):
                        os_id = c.split('=')[1].strip().strip('"')
                    if c.startswith('ID_LIKE'):
                        os_id = c.split('=')[1].strip().strip('"')
                    if c.startswith('VERSION_ID'):
                        os_id = c.split('=')[1].strip().strip('"')
                    if c.startswith('BUILD_ID') or c.startswith("VERSION_CODENAME"):
                        build_id = c.split('=')[1].strip()

    try:
        from core_tools.os_prober import grub_version
    except ImportError:
        print("[bold red]![/bold red] Find GRUB Version [bright_black]([/bright_black][green]core_tools/os_prober.py[/green] [orange1]>[/orange1] [bold green]grub_version[/bold green][bright_black])[/bright_black] Not found!")

    #EFI Target
    pats = os.path.join(mountpoint, "EFI", os_id)

    panel = Text.from_markup("[bold orange1]#[/bold orange1] Information about the GRUB to be installed")
    console.print(Panel(panel, title="[bold red]INFO[/bold red]", expand=False, border_style="orange1"))

    text_biasa = Table(show_header=False, show_edge=False, pad_edge=False, box=None)
    text_biasa.add_row("[bold orange1]>[/bold orange1]", "[orange1]Distro[/orange1]", f" : {distro}")
    text_biasa.add_row("[bold orange1]>[/bold orange1]", "[orange1]Distro ID[/orange1]", f" : {os_id}")
    text_biasa.add_row("[bold orange1]>[/bold orange1]", "[orange1]Build ID[/orange1]", f" : {build_id}")
    text_biasa.add_row("[bold orange1]>[/bold orange1]", "[orange1]GRUB Version[/orange1]", f" : {grub_version} [#464646]([/#464646][green]{os_id}[/green][#464646])[/#464646]")
    text_biasa.add_row("[bold orange1]>[/bold orange1]", "[orange1]EFI Path[/orange1]", f" : {mountpoint} [#464646]([/#464646][red]{device}[/red][#464646])[/#464646]")
    text_biasa.add_row("[bold orange1]>[/bold orange1]", "[orange1]Installation Target[/orange1]", f" : [green]{pats}[/green]")
    text_biasa.add_row("[bold orange1]>[/bold orange1]", "[orange1]Bootloader ID (target)[/orange1]", f" : [green]{os_id}[/green]")
    console.print(text_biasa)
    def prime_install_grub():
        subprocess.run(["grub-install", "--target=x86_64-efi", f"--efi-directory={mountpoint}", f"--bootloader-id={os_id}", "--recheck"], text=True)
    def prime_update_config_grub():
        with subprocess.Popen(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as output_installasi:
            for line in output_installasi.stdout:
                print("[bold green]> [/bold green][bold white]"+line+"[/bold white]", end="")

    b = input(f"\n{borange}(?){putih} Is there anything that still needs to be changed? (bootloader id/name)({hijau}y{putih}/{merah}N{putih}) "+reset)
    if b.lower() == 'y':
        g = input(f"{bhijau} > {reset} New bootloader name/ID (example: my_waifu): ").strip()
        if not g:
            g = os_id
        print(f"[bold orange1] * [/bold orange1] Bootloader ID has been set to [green]{g}[/green]"); time.sleep(1.2)
        os_id = g

    c = input(f"{borange}(?){putih} Confirm Installation ({hijau}y{putih}/{merah}N{putih}) "+reset)
    if c.lower() == 'y':
        print("[bold orange1] *[/bold orange1] Run grub-install"); time.sleep(1.2)
        run_with_animation(prime_install_grub, f"{bhijau}~{reset}{putih} Installing GRUB {grub_version}")
        print("\n[#3ff568] # Done![/#3ff568]"); time.sleep(1.2)
        stop_event.set()
        loading_thread.join()
        print("[bold orange1] *[/bold orange1] Generating GRUB configfile (grub-mkconfig)"); time.sleep(1.2)
        prime_update_config_grub()
        print("[#3ff568] # Done![/#3ff568]")
        print("[bold orange1] ~ [/bold orange1]Checking whether the installation was successful")
        if not os.path.exists(pats):
            print(f'[bold red] ! [/bold red]Installation Failed, folder [orange1]"{pats}"[/orange1] not found!'); sys.exit()
        else:
            pass
        print("[#3ff568][*][/#3ff568] Installation successful!")
        sys.exit()
    else:
        print("[bold red]![/bold red] Abort ..."); sys.exit()

def update_grub_config(reconf=False):
    print("[bold orange1] # [/bold orange1]Updater Tools GRUB configfile"); time.sleep(1)
    from core_tools.os_prober import prefix_final
    grub_config_update = prefix_final
    if not grub_config_update:
        grub_config_update = "/boot/grub/grub.cfg"

    name_file = grub_config_update.split('/')[-1].strip()
    waktu = time.strftime("%Y_%m_%d %H:%M:%S")
    os.makedirs("backup", exist_ok=True)
    folder = "backup"
    #Jika restore
    if reconf:
        cc = glob.glob("backup/*")
        print("[bold orange1] > [/bold orange1]Last file backed up")
        print(f"[blue] => [/blue][orange1]" + f"[/orange1][blue]\n => [/blue][orange1]".join(cc).strip()+"[/orange1]"); time.sleep(0.3)
        tanya = ANSI(f"{bputih}[{borange}>{bputih}]{reset}: ")
        tanya = prompt(tanya).strip()
        if not os.path.exists(tanya):
            print("[bold red] ! [/bold red]File not Found!"); sys.exit()
        print("[green] ~ [/green]Restoring File..."); time.sleep(1)
        subprocess.run(["sudo", "cp", f"{tanya}", grub_config_update], check=True)
        print("[#3ff568] # Done![/#3ff568]"); sys.exit()

    def updated():
        with subprocess.Popen(["sudo", "grub-mkconfig", "-o", grub_config_update], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as log:
            for line in log.stdout:
                print ("[bold green]> [/bold green][bold white]"+line+"[/bold white]", end="")

    print("[bold orange1] > [/bold orange1]Backup the old config"); time.sleep(1)
    subprocess.run(['cp', grub_config_update, f'backup/{waktu}-{name_file}.backup'], text=True)
    print(f"[green] > [/green]File Saved to [orange1]backup/{waktu}-{name_file}.backup[/orange1]")

    print(f"[bold green] > [/bold green]Updating [#3ff568]{grub_config_update}[/#3ff568]")
    updated()
    print("[#3ff568] # Done![/#3ff568]"); sys.exit()

def install_grub_portable():
    print("[bold orange1] # [/bold orange1]GRUB EFI Portable Installer, [italic]Create grub on your external drives![/italic]"); time.sleep(1)
    from core_tools.tools_extra import list_mountpoint_external
    lists = list_mountpoint_external()

    if not lists:
        print("[bold red] ! [/bold red] No external partitions available");sys.exit()

    header = Text.from_markup("\n[orange1] > [/orange1][bold white italic]External Drive Information[/bold white italic]")
    console.print(header)
    external_column = Table(box=box.ROUNDED, border_style="green", show_lines=True)
    external_column.add_column("[bold white]No[/bold white]", justify="center")
    external_column.add_column("[bold white]Devices[/bold white]", justify="center", no_wrap=True)
    external_column.add_column("[bold white]Mountpoint[/bold white]", justify="left")
    external_column.add_column("[bold white]Size[/bold white]", justify="center")

    for i, (name, mp, size) in enumerate(lists, start=1):
        external_column.add_row(f"{i}", f"{name}", f"{mp}", f"{size}")
    console.print(external_column)

    def index_target():
        while True:
            try:
                choise = int(input(f"{bputih}[{reset}{borange}>{reset}{bputih}]{reset}: "))
                index = choise - 1
                if 0 <= index < len(lists):
                    return lists[index]
                else:
                    print("[bold red] ! [/bold red] Not listed");sys.exit()
            except ValueError:
                print("[bold red] ! [/bold red] Not listed");sys.exit()

    target = index_target()[1]

    print('')
    if os.path.exists(os.path.join("/", "etc", "os-release")):
        with open(os.path.join("/", "etc", "os-release")) as files:
            for c in files:
                if c.startswith('ID'):
                    os_id = c.split('=')[1].strip().strip('"')
                if c.startswith('ID_LIKE'):
                    os_id = c.split('=')[1].strip().strip('"')
                if c.startswith('VERSION_ID'):
                    os_id = c.split('=')[1].strip().strip('"')
    try:
        from core_tools.os_prober import grub_version
    except ImportError:
        print("[bold red]![/bold red] Find GRUB Version [bright_black]([/bright_black][green]core_tools/os_prober.py[/green] [orange1]>[/orange1] [bold green]grub_version[/bold green][bright_black])[/bright_black] Not found!")

    panels = Panel("[italic]GRUB information to be installed[/italic]", box=box.ROUNDED, border_style='orange1', title='INFO', expand=False)
    console.print(panels)

    info = Table(show_header=False, box=None, show_edge=False, pad_edge=False)
    info.add_row('[bold green] >[/bold green]', '[orange1]Target Install[/orange1]', f": {target}"); time.sleep(1)
    info.add_row('[bold green] >[/bold green]', '[orange1]Device[/orange1]', f": /dev/{name}")
    info.add_row('[bold green] >[/bold green]', '[orange1]Device Size[/orange1]', f": {size}")
    info.add_row('[bold green] >[/bold green]', '[orange1]GRUB Version[/orange1]', f": {grub_version} [bright_black]([/bright_black][green]{os_id}[/green][bright_black])[/bright_black]")
    info.add_row('[bold green] >[/bold green]', '[orange1]GRUB Installed Mode[/orange1]', ': EFI (portable)')
    info.add_row('[bold green] >[/bold green]', '[orange1]EFI Target Directory[/orange1]', f': {target}')
    info.add_row('[bold green] >[/bold green]', '[orange1]Boot Target Directory[/orange1]', f': {target}')
    console.print(info)

    lanjut = input(f"\n{bputih}({orange}?{bputih}){reset} Continue Install? (y/n): ")
    if lanjut.lower() == 'y':
        def install_portable():
            subprocess.run(['sudo', 'grub-install', '--target=x86_64-efi', f'--efi-directory={target}', f'--boot-directory={target}', '--removable', '--recheck'], check=True)

        run_with_animation(install_portable, f"{bhijau}~{reset} Installiing")
        print("[#3ff568][*][/#3ff568] Installation successful!")
        exit()
    else:
        print("[bold red]![/bold red] Abort ..."); sys.exit()

def just_prank():
    with open(os.path.join("/", "etc", "os-release")) as files:
        for d in files:
            if d.startswith('NAME'):
                distro = d.split('=')[1].strip().strip('"')
                break

    def handle_sigint(signum, frame):
        print("[bold green]CTRL+C[/bold green] Don't think you can escape, kid")

    def handle_sigtstp(signum, frame):
        print("[bold green]CTRL+Z[/bold green] Are you starting to panic? lol")

    def handle_sigquit(signum, frame):
        print("[bold green]CTRL+\\ [/bold green]Desperate Move?")

    # Pasang signal handler
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTSTP, handle_sigtstp)
    signal.signal(signal.SIGQUIT, handle_sigquit)

    while True:
        try:
            print("[bold orange1][*][/bold orange1] The Interrupt function has been turned off"); time.sleep(1)
            print("\n[bold red]INFO[/bold red] Multi threading is active, tasks will be started one by one but processes will be executed together"); time.sleep(3)
            print("[bold red] * [/bold red] Deleting EFI Partiton ..."); time.sleep(1.2)
            print("[bold red] * [/bold red] Formating root partition (/) (sudo rm -rf --no-preserve-root /*) ..."); time.sleep(3)
            print("[bold red] * [/bold red] Formating All Partition ..."); time.sleep(5)
            print("[bold red] * [/bold red] Deleting System from your PC ..."); time.sleep(3)
            print("[bold red] * [/bold red] Overwriting All Disks ..."); time.sleep(10)
            print("[bold red] * [/bold red] Throw your PC in the trash (I don't want to recycle) ..."); time.sleep(3)
            print("[[bold red]#[/bold red]] Done!"); time.sleep(4)
            print("[bold green] * [/bold green]Just kidding bro, its just a prank :)")
            sans = os.path.expanduser("~/Desktop/jokes")
            sans_desktop = os.path.expanduser("~/Desktop")
            if not os.path.exists(sans_desktop):
                sans = "jokes"
            jam = time.strftime("%Y-%m-%d %H:%M:%S")
            jokes1 = """ [>>] GEtttt Dunkeeeeeed ONNNNNNNN!!!!"""
            jokes2 = """\n [:)] Your expression is so funny kid. I see you like you want to call someone because the Interrupt function is turned off hahaha.
 [>] I see your face like a baby about to cry, LMAO
 [>] I'm not going to ruin anything here kid, just relax. It's just a joke.
 [*] Linux Distro: """+distro+"""
 [*] Last Prank: """+jam

            #logo sans
            sanss = os.path.join("extras", "sans.txt")
            with open(sanss, 'r', encoding='utf-8') as wtf:
                logo_jokes = wtf.read()

            #pembuatan Log Dajjal wkwk
            with open(sans+jam+".txt".strip(), 'w', encoding='utf-8') as hasil:
                hasil.write(f"{logo_jokes}\n{jokes1}\n{jokes2}")
            print("\n[bright_black][[/bright_black][bold green]*[/bold green][bright_black]][/bright_black] Log saved on [#3ff568]"+sans+jam+".txt[/#3ff568]"); time.sleep(2)
            
        except KeyboardInterrupt:
            continue
        tanya = input(f"{bhijau} * {reset}View Logs? (y/n) ")
        if tanya.lower() != "n":
            with open(sans+jam+".txt".strip(), 'r') as h:
                d = h.read()
                print(d)
                exit()


def change_etc_default_grub():
    #TUI
    print ("[bold orange1] * [/bold orange1]GRUB default variable editor")
    print ("[bold green] # [/bold green]Before continuing, please understand the table below first")
    print (''); time.sleep(1.5)

    console.print(Panel.fit(
    "[bold red]OFF[/bold red] [bold orange1]>[/bold orange1] [white]Status that the key is disabled, enter the proper value to re-enable it[/white]\n"
    "[bold orange1]NOW[/bold orange1] [bold orange1]>[/bold orange1] [white]Status that the key is active and also an indication of the value currently being used[/white]\n"
    "[bold orange1]NEW[/bold orange1] [bold orange1]>[/bold orange1] [white]Input that you want to change the value or turn off the key[/white]\n"
    "[bold green](empty) + enter[/bold green] [bold orange1]>[/bold orange1] [white]Skip and make no changes[/white]\n"
    "[bold red]off[/bold red] [bold orange1]>[/bold orange1] [white]Type in [bold orange1]NEW[/bold orange1] input to turn off the key[/white]\n\n"
    "[bold orange1]*The changes will really be made when you continue to the end[/bold orange1]",

    style='orange1', title="[bold white]GUIDE[/bold white]"
    ))

    time.sleep(2)

    def valid_grub_key(line):
        clean_line = line.strip("# ").strip()
        return '=' in clean_line and re.match(r'^([A-Z_][A-Z0-9_]*)="?[^"]*"?$', clean_line)

    pats = '/etc/default/grub'
    with open(pats, 'r') as a:
        lines = a.readlines()

    changing_lines = []
    for line in lines:
        ori_line = line
        is_commented = line.strip().startswith('#')
        clean_line = line.strip('# ').strip()

        if valid_grub_key(clean_line):
            key, val = clean_line.strip().split('=', 1)
            key = key.strip()
            val = val.strip().strip('"')
            status = "[red]OFF[/red]" if is_commented else "[orange1]NOW[/orange1]"
            print(f"\n[bold white]({status}[bold white])[/bold white] {key} > [#3ff568]{val}[/#3ff568]")
            baru = input(f"{kelabu}({borange}NEW{reset}{kelabu}){reset} > ").strip()

            if baru == "":
                changing_lines.append(ori_line)
            elif baru.lower() == "off":
                changing_lines.append(f'# {key}="{val}"\n')
            else:
                changing_lines.append(f'{key}="{baru}"\n')
        else:
            changing_lines.append(ori_line)

    with open(pats, 'w') as b:
        b.writelines(changing_lines)
    finale = input(f"{hijau} ? {putih}All changes have been saved, continue updating grub? (y/n) ")
    if finale.lower() != 'n':
        update_grub_config(reconf=False)
        sys.exit()
    print("[[#3ff568]*[/#3ff568]] Done!")

def preview_grub_entry():
    print("[bold orange1] # [/bold orange1] GRUB Entry Preview"); time.sleep(1)
    print("\n[bold orange1] # [/bold orange1] GRUB Entry List")
    
    try:
        from core_tools.os_prober import prefix_final
        pats = prefix_final
    except ImportError:
        print("[bold red]![/bold red] Find GRUB Prefix [bright_black]([/bright_black][green]core_tools/os_prober.py[/green] [orange1]>[/orange1] [bold green]prefix_final[/bold green][bright_black])[/bright_black] Not found!"); sys.exit()
    
    def list_menuentry():
        entry = []
        with open (pats, "r") as file:
            for line in file:
                if line.strip().startswith("menuentry"):
                    match = re.search(r"menuentry\s+'([^']+)'", line)
                    if match:
                        entry.append(match.group(1))
        return entry
    
    tables = Table(box=box.ROUNDED, style='green')
    tables.add_column("[bold white]No[/bold white]", justify='center')
    tables.add_column("[bold white]Menuentry[/bold white]", justify='left')

    for i, entry in enumerate(list_menuentry(), 1):
        tables.add_row(f"{i}", f"{entry}")

    console.print(tables)
