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


import os, time, sys, glob, subprocess

from color.warna import borange
from color.warna import reset
from color.warna import banner

from rich import print
from rich.live import Live
from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import ANSI

console = Console()

def easy_mode():
    print("[bold orange1] # [/bold orange1]GRUB Sreetx Tools, easy mode!\n"); time.sleep(2)
    print("[bold orange1] > [/bold orange1] Options, [italic]select one[/italic]")

    tabel = Table(show_edge=False, pad_edge=False, box=None, show_header=False)
    tabel.add_row("[bright_black]([/bright_black][orange1]1[/orange1][bright_black])[/bright_black]", "Update grub.cfg config")
    tabel.add_row("[bright_black]([/bright_black][orange1]2[/orange1][bright_black])[/bright_black]", "Restore grub.cfg config")
    tabel.add_row("[bright_black]([/bright_black][orange1]3[/orange1][bright_black])[/bright_black]", "Set grub config default variabels (/etc/default/grub)")
    tabel.add_row("[bright_black]([/bright_black][orange1]4[/orange1][bright_black])[/bright_black]", "Check all component OS ini /boot")
    tabel.add_row("[bright_black]([/bright_black][orange1]5[/orange1][bright_black])[/bright_black]", "Check all installed OS (also functions to automatically insert detected entries into grub if the system os-prober is turned off)")
    tabel.add_row("[bright_black]([/bright_black][orange1]6[/orange1][bright_black])[/bright_black]", "Install GRUB EFI")
    tabel.add_row("[bright_black]([/bright_black][orange1]7[/orange1][bright_black])[/bright_black]", "Install GRUB EFI (portable)")
    tabel.add_row("[bright_black]([/bright_black][orange1]8/orange1][bright_black])[/bright_black]", "Preview GRUB ENTRY")
    tabel.add_row("[bright_black]([/bright_black][orange1]9[/orange1][bright_black])[/bright_black]", "Change default prefix")
    tabel.add_row("\n[bold orange1]ADD-ON[/bold orange1]")
    tabel.add_row("[bright_black]([/bright_black][orange1]10[/orange1][bright_black])[/bright_black]", "Create a Bootable disk !")
    tabel.add_row("[bright_black]([/bright_black][orange1]11[/orange1][bright_black])[/bright_black]", "Secret/Dark Tools, [bold red][italic]Do Not Touch![/italic][/bold red]")
    tabel.add_row("[bright_black]([/bright_black][bold green]12[/bold green][bright_black])[/bright_black]", "Update this tools")

    console.print(tabel)

    easy = input(f"{borange} => {reset}")

    #Update GRUB
    os.system("cls || clear")
    if easy.lower() == "1":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.configures import update_grub_config
            update_grub_config(reconf=False)
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB Config Updater (core_tools/configures > update_grub_config) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #Restore Backup
    if easy.lower() == "2":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.configures import update_grub_config
            update_grub_config(reconf=True)
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB Config Updater (core_tools/configures > update_grub_config) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #Set GRUB config default variables
    if easy.lower() == "3":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
           print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.configures import change_etc_default_grub
            change_etc_default_grub()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB default variabel config editor (core_tools/configures > change_etc_default_grub) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #Check all component os in /boot
    if easy.lower() == "4":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.os_prober import check_os
            check_os()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]OS information Finder (core_tools/os_prober > check_os) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #OS Prober by Sreetx
    if easy.lower() == "5":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.os_prober import os_prober
            check_os()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]OS Prober Sreetx (core_tools/os_prober > os_prober) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #Install GRUB EFI Mode
    if easy.lower() == "6":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.configures import install_grub_efi
            install_grub_efi()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB EFI Installer (core_tools/configures > install_grub_efi) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()
    
    #Install GRUB EFI Portable
    if easy.lower() == "7":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.configures import install_grub_portable
            install_grub_portable()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB EFI Protable Installer (core_tools/configures > install_grub_portable) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()
    
    #Preview GRUB ENTRY
    if easy.lower() == "8":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.configures import preview_grub_entry
            preview_grub_entry()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB EFI Protable Installer (core_tools/configures > preview_grub_entry) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #Set Prefix
    if easy.lower() == "9":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.configures import set_prefix
            set_prefix()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB Config prefix changer (core_tools/configures > set_prefix) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #Iso Burner
    if easy.lower() == "10":
        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red] Please run this script with SUDO/SU");sys.exit()
        try:
            from core_tools.tools_extra import burner_iso
            burner_iso()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB Config prefix changer (core_tools/tools_extra > burner_iso) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #SEcreetx!
    if easy.lower() == "11":
        banner()
        def root_id():
            return os.getuid() != 0
        if root_id():
            pass
        else:
            print("\n[bold red] ! [/bold red]using experimental secret features with sudo is dangerous!")
            print("[bld red] * [/bold red]But this feature can still make changes to your system!");sys.exit()
        try:
            from core_tools.configures import just_prank
            just_prank()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB Config prefix changer (core_tools/tools_extra > burner_iso) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()

    #UPDATEer
    if easy.lower() == "12":
        banner()
        def root_id():
            return os.getuid() != 0
        if root_id():
            pass
        else:
            print("[bold red] # [/bold red] This will just update all the tools")
            print("[bold red] # [/bold red] No need to use sudo/SU"); time.sleep(1.3)
            sys.exit()
        
        try:
            from core_tools.updater import updates
            updates()
            sys.exit()
        except ImportError:
            print("[bold red] ! [/bold red]GRUB Sreetx Tools Updater (core_tools/updater > updates) Not found!"); sys.exit()
        except KeyboardInterrupt:
            print("[bold green] * [/bold green]Exit, Have a nice day!");sys.exit()





