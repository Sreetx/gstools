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

import os, time, sys, subprocess, re, glob, json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print

from dataclasses import dataclass

from color.warna import orange
from color.warna import putih
from color.warna import merah
from color.warna import hijau
from color.warna import banorange
from color.warna import biru
from color.warna import borange
from color.warna import bputih
from color.warna import bhijau
from color.warna import bmerah
from color.warna import bbiru
from color.warna import kelabu
from color.warna import borangekelip
from color.warna import banhijau
from color.warna import banmerah
from color.warna import banhijau
from color.warna import reset

console = Console()
@dataclass
class ESPInfo:
    device: str
    flags: str
    mountpoint: str
    fstype: str
    size: str
    uuid_efi: str
#Di bawah json nya bang :)

def esp_part_checker():
    try:
        output = subprocess.check_output(["lsblk", "-J", "-o", "NAME,MOUNTPOINT,FSTYPE,PARTFLAGS,SIZE,UUID"], text=True)
        devices = json.loads(output)['blockdevices']
        def find_esp(devices):
            for dev in devices:
                if 'children' in dev:
                    for child in dev['children']:
                        fstype = child.get('fstype', '')
                        partflags = child.get('partflags', '')
                        mountpoint = child.get('mountpoint', '')
                        size = child.get('size', '')
                        uuid_efi = child.get('uuid', '')

                        if (fstype == 'vfat' and '/boot/efi' and '/boot' in (mountpoint or '')):
                            return ESPInfo(
                                device=f"/dev/{child['name']}",
                                flags=partflags,
                                mountpoint=mountpoint,
                                fstype=fstype,
                                size=size,
                                uuid_efi=uuid_efi,
                            )
            return "Unknown"
        esp_info = find_esp(devices)
        if esp_info:
            return esp_info
        else:
            return None
    except Exception:
        print("[bold red] ! [/bold red]ESP Partition Not Found! Abort ..."); sys.exit()

def boot_part_dynamic():
    root_dir = subprocess.run(['findmnt', '-no', 'SOURCE', '/'], stdout=subprocess.PIPE, text=True)
    return root_dir.stdout.strip()

boot_part = boot_part_dynamic()

def dev_to_grub(dev):
    match = re.match(r'/dev/sd([a-z])(\d+)', dev)
    if match:
        disk_letter = match.group(1)
        part_number = int(match.group(2))
        disk_number = ord(disk_letter) - ord('a')
        return f"(hd{disk_number},{part_number})"

grub_part = dev_to_grub(boot_part)

def detect_grub_version():
    with os.popen("grub-install --version") as version:
        for grub_version in version:
            grub_version = grub_version.strip("grub-install").strip()
            grub_version = grub_version.strip("(GRUB)").strip()
            return grub_version

grub_version = detect_grub_version()

def check_grub_prefix():
    try:
        global path
        from core_tools.configures import path
    except ImportError:
        print("[bold red]![/bold red] Detect GRUB Installed path [bright_black]([/bright_black][green]core_tools/configures.py[/green] [orange1]>[/orange1] [bold green]path[/bold green][bright_black])[/bright_black] Not found!")
        path = ""
    if not path == "Unknown":
        path = "Unknown"
        prefix_final = "/boot/grub/grub.cfg"
        return prefix_final
    else:
        prefix_awal = path.strip()
        prefix_nanti = os.path.join(prefix_awal, "grub.cfg")
        try:
            if not os.path.exists(prefix_awal):
                print(f"\n [bold red![/bold red] File prefix_awal is missing or ESP partition not mounted! Create prefix with [bold white]--set-prefix[/bold white]"); sys.exit()
            with open (prefix_nanti) as prefix_nya:
            # Prefix
                for f in prefix_nya:
                    if f.startswith("set prefix=($root)"):
                        prefix1 = f.split("($root)")[1].strip().strip("'").strip()
                        break
                for f in prefix_nya:
                    if f.startswith('configfile $prefix'):
                        prefix2 = f.split("$prefix")[1].strip().strip()
                        break
                prefix_final = prefix1+prefix2
                return prefix_final
        except Exception:
            prefix_final = "/boot/grub/grub.cfg"
            return prefix_final

prefix_final = check_grub_prefix()


#pecahan
def check_model():
    try:
        result = subprocess.run(['sudo', 'dmidecode', '-t', 'system'], capture_output=True, text=True, check=True)

        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return lines
    except subprocess.CalledProcessError as e:
        print(f"Failed to get system model: {e}")
        return []

def check_bios():
    try:
        result = subprocess.run(['sudo', 'dmidecode', '-t', 'bios'], capture_output=True, text=True, check=True)

        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return lines
    except subprocess.CalledProcessError as e:
        print(f"Failed to get bios model: {e}")
        return []

def cpu_model():
    try:
        with open ('/proc/cpuinfo', 'r') as f:
            for line in f:
                if "model name" in line:
                    cpu = line.split(":")[1].strip()
                    return cpu
            return "Unknown CPU Model"
    except FileNotFoundError:
        print("[bold red] ! [/bold red]CPU info file not found!")

#prime dev
def check_os():
    print("[bold orange1] * [/bold orange1]Checking OS part ..."); time.sleep(1.3)
    print("[bold green] # [/bold green]OS Part ..."); time.sleep(0.5)
    try:
        # For Rolling OS
        if os.path.exists(os.path.join("/", "etc", "os-release")):
            with open(os.path.join("/", "etc", "os-release")) as files:
                for c in files:
                    if c.startswith('PRETTY_NAME'):
                        distro = c.split('=')[1].strip().strip('"')
                        print (f"[bold green] > [/bold green][orange1]Distro:[/orange1] {distro}"); time.sleep(0.5)
                    if c.startswith('ID'):
                        os_id = c.split('=')[1].strip()
                        print (f"[bold green] > [/bold green][orange1]Distro ID:[/orange1] {os_id}"); time.sleep(0.5)
                    if c.startswith('ID_LIKE'):
                        os_id = c.split('=')[1].strip()
                        print (f"[bold green] > [/bold green][orange1]Distro ID:[/orange1] {os_id}"); time.sleep(0.5)
                    if c.startswith('VERSION_ID'):
                        os_id = c.split('=')[1].strip().strip('"')
                        print (f"[bold green] > [/bold green][orange1]Version ID:[/orange1] {os_id}"); time.sleep(0.5)
                    if c.startswith('BUILD_ID') or c.startswith("VERSION_CODENAME"):
                        build_id = c.split('=')[1].strip()
                        print (f"[bold green] > [/bold green][orange1]Build ID:[/orange1] {build_id}"); time.sleep(0.5)
                        break
        else:
            # For Old OS
            with open(os.path.join("/", "etc", "lsb-release")) as files:
                for d in files:
                    if d.startswith('NAME'):
                        distro = d.split('=')[1].strip().strip('"')
                        print (f"[bold green] > [/bold green][orange1]Distro:[/orange1] {distro}"); time.sleep(0.5)
                        break
        try:
            esp = esp_part_checker()
            device = esp.device
            flags = esp.flags
            fstype = esp.fstype
            mountpoint = esp.mountpoint
            size = esp.size
            uuid_efi = esp.uuid_efi
        except Exception:
            device = "Unknown"
            flags = "Unknown"
            fstype = "Unknown"
            mountpoint = "Unknown"
            size = "Unknown"
            uuid_efi = "Unknown"
            
        kernel = glob.glob("/boot/*vmlinuz*")
        initrd = glob.glob("/boot/*initrd*")

        if not flags:
            flags = "Unknown"
        if not initrd:
            initrd = glob.glob("/boot/*initramfs*")
            if not initrd:
                initrd = glob.glob("/boot/*initrfs*")
            if not initrd:
                initrd = "No Initramfs Found"
        if not kernel:
            kernel = "No Kernel Found"
        print("[bold orange1] > [/bold orange1]Kernel Found: \n[blue]=>[/blue] [orange1]" + f"[blue]\n=>[/blue] [orange1]".join(kernel)+"[/orange1]"); time.sleep(0.3)
        print('')
        print("[bold orange1] > [/bold orange1]Initramfs Found: \n[blue]=>[/blue] [orange1]" + f"[blue]\n=>[/blue] [orange1]".join(initrd)+"[/orange1]"); time.sleep(0.3)

        print("\n[bold green] # [/bold green]GRUB Information ..."); time.sleep(0.5)
        print ("[bold green] > [/bold green]GRUB Version: [orange1]"+grub_version+"[/orange1] [bright_black]([/bright_black][#3ff568]"+os_id+"[/#3ff568][bright_black])[/bright_black]"); time.sleep(0.5)
        print ("[bold green] > [/bold green]GRUB EFI Path: [#3ff568]"+path+"[/#3ff568]"); time.sleep(0.5)
        print ("[bold green] > [/bold green]GRUB configfile used: [orange1]"+str(prefix_final).strip()+"[/orange1]"); time.sleep(0.5)
        print(f"[bold green] * [/bold green]EFI partition: [white]{device}[/white] [bright_black]([/bright_black][green]{mountpoint}[/green][bright_black])[/bright_black]"); time.sleep(0.5)
        print(f"[bold green] * [/bold green]Size: [white]{size}[/white]"); time.sleep(0.5)
        print(f"[bold green] * [/bold green]UUID: [orange1]{uuid_efi}[/orange1]")
        print(f"[bold green] * [/bold green]Flags: [orange1]{flags}[/orange1]"); time.sleep(0.5)

        print("\n[bold green] # [/bold green]PC/System Model"); time.sleep(0.5)

        for line in check_model():
            if any(key in line for key in ["Manufacturer", "Product Name", "Version", "Serial Number", "UUID", "SKU Number", "Family"]):
                print(f"[bold orange1] > [/bold orange1]{line}"); time.sleep(0.5)

        print(f"[bold orange1] > [/bold orange1]CPU Information: {cpu_model()}"); time.sleep(0.5)

        print("\n[bold green] # [/bold green]BIOS Information"); time.sleep(0.5)

        for line in check_bios():
            if any(key in line for key in ["Vendor", "Version", "Release Date", "Runtime Size", "ROM Size"]):
                print(f"[bold orange1] > [/bold orange1]{line}"); time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[bold green]*[/bold green] Exit, have a nice day ...");sys.exit()
        exit()

def os_prober(output_file=None):
    print("[bold orange1] * [/bold orange1] Searching for Installed OS...")
    time.sleep(1.3)
    found = []
    with os.popen("lsblk -n -r -o NAME,MOUNTPOINT,UUID") as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        name = parts[0]
        mountpoint = parts[1]
        uuid = parts[2]
        if mountpoint in ("[SWAP]", "-") or not os.path.isdir(mountpoint):
            continue

        if not os.path.isfile(os.path.join(mountpoint, 'etc', 'os-release')):
            try:
                if os.path.isfile(os.path.join(mountpoint, 'etc', 'lsb-release')):
                    with open (os.path.join(mountpoint, 'etc', 'lsb-release')) as f1:
                        for l in f1:
                            if l.startswith('PRETTY_NAME'):
                                distro = l.split('=')[1].strip().strip('"')
                                break
                    found.append((distro, mountpoint, uuid))
            except:
                continue
        else:
            try:
                if os.path.isfile(os.path.join(mountpoint, 'etc', 'os-release')):
                    with open (os.path.join(mountpoint, 'etc', 'os-release')) as f1:
                        for l in f1:
                            if l.startswith('PRETTY_NAME'):
                                distro = l.split('=')[1].strip().strip('"')
                                break
                    found.append((distro, mountpoint, uuid))
            except:
                continue
        
    windows = "/boot/efi/EFI/Microsoft/Boot/bootmgfw.efi"
    if not os.path.exists(windows):
        windows = "/boot/EFI/Microsoft/Boot/bootmgfw.efi"
        if not os.path.exists(windows):
            pass
    else:
        pass
    if os.path.exists(windows):
        esp = esp_part_checker()
        device = esp.device
        flags = esp.flags
        fstype = esp.fstype
        mountpoint = esp.mountpoint
        size = esp.size
        uuid_efi = esp.uuid_efi
        found.append(("Windows", windows, uuid_efi))

    with open("extras/os-list.txt", "w") as f2:
        for distro, mp, uuid in found:
            f2.write(f"{distro} = {mp} {uuid}\n")
            print(f"[blue]==>[/blue] [bold white]{distro}[/bold white] = [#3ff568]{mp}[/#3ff568] [bright_black]([/bright_black][orange1]{uuid}[/orange1][bright_black])[/bright_black] (GRUB: {grub_part})")
    print("[bold green] > [/bold green] Done...")

    grub_file = "/etc/default/grub"
    pats = '/etc/grub.d/40_custom'
    processed_uuids = set()

    def is_os_prober_disabled():
        found_uncommented = False
        found_commented = False
        lines = []

        try:
            with open(grub_file, "r") as f:
                lines = f.readlines()

            for line in lines:
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                if line_stripped.startswith("#") and "GRUB_DISABLE_OS_PROBER" in line_stripped:
                    found_commented = True
                    continue

                if "GRUB_DISABLE_OS_PROBER" in line_stripped:
                    found_uncommented = True
                    key, value = line_stripped.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'").lower()

                    if key == "GRUB_DISABLE_OS_PROBER":
                        return value == "true"  # True = os-prober dimatikan

            if not found_uncommented and not found_commented:
                # Kalau gak ada sama sekali, tambahin default ke file
                lines.append("\nGRUB_DISABLE_OS_PROBER=false\n")
                with open(grub_file, "w") as f:
                    f.writelines(lines)
                print("[bold orange1] * [/bold orange1]Menambahkan GRUB_DISABLE_OS_PROBER=false ke /etc/default/grub")

            return False  # Default: os-prober aktif
        except Exception as e:
            print(f"[red]! Gagal membaca/mengubah GRUB config: {e}[/red]")
            return False

    status = is_os_prober_disabled()
    print('')
    if status is False:
        console.print(Panel.fit(
            "[bold orange1]! [/bold orange1]os-prober system is active, so detected entries will not be added to the grub configuration\n"
            "[bold orange1]# [/bold orange1]Turn off os-prober system to use this feature fully\n"
            "[bold orange1]# [/bold orange1]Turn it off with --set-config in this script and look for the GRUB_DISABLE_OS_PROBER key\n"
            "[bold orange1]# [/bold orange1]Make sure the value is true or the status is OFF",
            title="INFORMATION",border_style='orange1'
        ))

        tools = f"""
menuentry 'Reboot' --class restart $menuentry_id_option 'reboot' {{
    reboot
}}
menuentry 'Power OFF' --class shutdown $menuentry_id_option 'shutdown' {{
    halt
}}"""
        
        with open(pats, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if 'exec tail -n +3' in line:
                awal = i + 1
                break

        with open(pats, 'w') as f:
            f.writelines(lines[:awal])
            f.write("\n")

        with open(pats, 'a') as menus:
            menus.write(f"\n{tools}\n")

    else:
        print("[bold green] * [/bold green]The above output will be immediately entered into the grub entry..."); time.sleep(1.5)

        list_file = 'extras/os-list.txt'
        if not os.path.exists(list_file):
            print("[bold red] ! [/bold red]File Not Found"); sys.exit()

        with open(list_file, 'r') as ff:
            lines = ff.readlines()

        entry = []
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            distro, info = line.split('=', 1)
            distro = distro.strip()
            uuids = info.strip().split()
            if len (uuids) < 2:
                continue
            mountpoint, uuidd = uuids[0], uuids[1]

            if uuidd in processed_uuids:
                continue
            processed_uuids.add(uuidd)

            if mountpoint.lower() == "/":
                continue
            if distro.lower() == "windows":
                continue
            
            def cari_kernel_initrd():
                boot_path = os.path.join(mountpoint, "boot")

                def get_kernel_version_from_filename(filename):
                    match = re.search(r"\d+\.\d+\.\d+(?:-\d+)?", filename)
                    return match.group() if match else None

                kernel_candidates = glob.glob(os.path.join(boot_path, "vmlinuz*"))
                initrd_candidates = glob.glob(os.path.join(boot_path, "initrd*")) + glob.glob(os.path.join(boot_path, "initramfs*"))

                if not kernel_candidates:
                    print(f"[red]Gagal temukan kernel/initrd di {boot_path}[/red]")
                    return None, None
                for kernel_path in kernel_candidates:
                    kernel_name = os.path.basename(kernel_path)
                    kernel_ver = get_kernel_version_from_filename(kernel_name)
                    if not kernel_ver:
                        continue
                    for initrd_path in initrd_candidates:
                        initrd_name = os.path.basename(initrd_path)
                        initrd_ver = get_kernel_version_from_filename(initrd_name)

                        if initrd_ver == kernel_ver:
                            kernel = os.path.relpath(kernel_path, mountpoint)
                            initrd = os.path.relpath(initrd_path, mountpoint)
                            return kernel, initrd
                        
            kernel, initrd = cari_kernel_initrd()
            if not kernel or not initrd:
                continue
            
            def get_cmdline_linux(grub_file="/etc/default/grub"):
                with open(grub_file, "r") as f:
                    content = f.read()

                for line in content.splitlines():
                    if line.strip().startswith("#"):
                        continue

                    for key in ["GRUB_CMDLINE_LINUX_DEFAULT", "GRUB_CMDLINE_LINUX"]:
                        match = re.match(fr'^\s*{key}\s*=\s*[\'"](.*?)[\'"]', line)
                        if match:
                            return match.group(1)
                return ''

            if os.path.exists(os.path.join(mountpoint, "etc", "os-release")):
                with open(os.path.join(mountpoint, "etc", "os-release")) as files:
                    for c in files:
                        if c.startswith('ID'):
                            os_id = c.split('=')[1].strip().strip()
                            break
                        if c.startswith('ID_LIKE'):
                            os_id = c.split('=')[1].strip().strip('"')
                            break
                        
            
            cmdline_linux = get_cmdline_linux()
            if not cmdline_linux:
                print("gagal detect")

            template_entry = f"""
menuentry '{distro}' --class {os_id} --class os --class gnu --class gnulinux $menuentry_id_option 'gnulinux-simple-{uuidd}' {{
    load video
    set gfxpayload=keep
    insmod gzio
    insmod part_gpt
    insmod ext2
    insmod part_msdos
    search --no-floppy --fs-uuid --set=root {uuidd}
    linux /{kernel} root=UUID={uuidd} rw {cmdline_linux}
    initrd /{initrd}
}}"""
            
            entry.append(template_entry)

        if not os.path.exists(pats):
            print("/etc/grub.d/40_custom not found"); sys.exit()

        with open (pats, 'r') as h:
            clears = h.readlines()
        for i, line in enumerate(clears):                
            if 'exec tail -n +3' in line:
                awal = i + 1
                break

        with open(pats, 'w') as f:
            f.writelines(clears[:awal])
            f.write("\n")

        windows = "/boot/efi/EFI/Microsoft/Boot/bootmgfw.efi"
        if not os.path.exists(windows):
            windows = "/boot/EFI/Microsoft/Boot/bootmgfw.efi"
        else:
            pass
        if os.path.exists(windows):
            esp = esp_part_checker()
            device = esp.device
            flags = esp.flags
            fstype = esp.fstype
            mountpoint = esp.mountpoint
            size = esp.size
            uuid_efi = esp.uuid_efi
            
            windows = "/boot/efi/EFI/Microsoft/Boot"
            windows2 = "/boot/EFI/Microsoft/Boot"
            if os.path.exists(windows) or os.path.exists(windows2):
                windows_boot_path = '/EFI/Microsoft/Boot/bootmgfw.efi'
                windows_template = f"""
menuentry 'Windows' --class windows --class os $menuentry_id_option 'windows-{uuid_efi}' {{
    insmod part_gpt
    insmod fat
    search --no-floppy --fs-uuid --set=root {uuid_efi}
    chainloader {windows_boot_path}

}}"""

        tools = f"""
menuentry 'Reboot' --class restart $menuentry_id_option 'reboot' {{
    reboot
}}
menuentry 'Power OFF' --class shutdown $menuentry_id_option 'shutdown' {{
    halt
}}"""

        with open(pats, 'a') as ha:
            for e in entry:
                ha.write(f"{e}\n\n")
        if os.path.exists("/boot/EFI/Microsoft/Boot") or os.path.exists("/boot/efi/EFI/Microsoft/Boot"):
            with open(pats, 'a') as windows_entry:
                windows_entry.write(f"{windows_template}\n\n")
        else:
            pass
        with open(pats, 'a') as toolkit:
            toolkit.write(f"{tools}\n\n")

        print("[bold green] * [/bold green]Successfully added:")
        with open("extras/os-list.txt", 'r') as rs:
            list = rs.readlines()
        for i, line in enumerate(list):
            if i == 0:
                continue
            c = line.split("=")[0].strip()
            print(f"    {c}")
        
        tanya = input(f"{kelabu}({borange}?{reset}{kelabu}){putih} Update grub? (y/n) ")
        if tanya.lower() != 'n':
            from core_tools.configures import update_grub_config
            update_grub_config(reconf=False)
            sys.exit()

#For another module
def uuid_root_checker():
    #Single part UUID checker
    with os.popen("findmnt -nro UUID /") as f:
        lines = f.readlines()
    for line in lines:
        uuidc = line.strip().split()
        uuidc = ''.join(uuidc).strip()
        return uuidc
uuid_roots = uuid_root_checker()






