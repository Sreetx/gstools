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

import os, sys, time, threading, subprocess, glob, webbrowser
from argparse import ArgumentParser

stop_event = threading.Event()
def loading_animation(teks):
    i = 0
    while not stop_event.is_set():
        dot = '.' * (i % 5)
        print(f"\r {teks}{dot:<5}", end='', flush=True)
        time.sleep(0.3)
        i += 1

def import_module():
    try:
        global banner
        global orange
        global putih
        global merah
        global hijau
        global biru
        global borange
        global bputih
        global bhijau
        global bmerah
        global banorange
        global bbiru
        global kelabu
        global borangekelip
        global banhijau
        global banmerah
        global banhijau
        global reset
        from color.warna import banner
        from color.warna import orange
        from color.warna import putih
        from color.warna import merah
        from color.warna import hijau
        from color.warna import biru
        from color.warna import banorange
        from color.warna import borange
        from color.warna import bputih
        from color.warna import bhijau
        from color.warna import bmerah
        from color.warna import bbiru
        from color.warna import kelabu
        from color.warna import borangekelip
        from color.warna import banhijau
        from color.warna import banmerah
        from color.warna import reset
    except ImportError:
        print(" [*] ImportError, Pelase reinstall this script from Github!");sys.exit()

def run_with_animation(func, teks):
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

run_with_animation(import_module, "[*] Importing Module")

# Check OS <
# Regenerate grub configfile via Subprocess <
# Check All OS <
# Preview Boot Entry
# Install GRUB EFI <
# Delete your system <
# Set Config /etc/default/grub
# Check All EFI Entry <
# Check OS Component <
# Burn ISO to disks <
def bantuan():
    banner()
    ini_bantuan_nya = """
python3 """+hijau+"""main.py"""+orange+""" [OPTIONS]"""+putih+"""

"""+biru+"""Options:
  """+orange+"""--check-os              """+putih+"""Check all information for your distro
  """+orange+"""--update-grub           """+putih+"""Regenerate grub configuration
  """+orange+"""--restore-config        """+putih+"""Restore the previous group configuration that was automatically backed up
  """+orange+"""--install-grub-efi      """+putih+"""Install GRUB to your esp partition by simply typing this option
  """+orange+"""--install-grub-portable """+putih+"""Install GRUB to your external drive (flashdisk, ssd, etc.)
  """+orange+"""--secret-tools          """+bmerah+"""Do Not Touch!"""+reset+"""
  """+orange+"""--detect-os             """+putih+"""Like the os-prober module, but simpler and lighter
  """+orange+"""--set-config            """+putih+"""Change GRUB settings from /etc/default/grub directly from this script
  """+orange+"""--set-prefix            """+putih+"""Change the location of the GRUB configuration file to be used
  """+orange+"""--burn-iso              """+putih+"""Create your own bootable disk in the simplest and easiest way (Even your grandmother can do it)
  """+orange+"""--preview-entry         """+putih+"""View your entries instantly without rebooting!
  """+orange+"""--update                """+putih+"""View your entries instantly without rebooting!
  """+orange+"""--dont-clear            """+putih+"""Do not clean the terminal (not standalone command)"""

    print(ini_bantuan_nya)

menu = ArgumentParser()
menu.add_argument('--check-os', dest='check_os', action='store_true', default=False, help="Check OS information")
menu.add_argument('--update-grub', dest='upgr', action='store_true', default=False, help="Update grub via mkconfig")
menu.add_argument('--restore-config', dest='reconf', action='store_true', default=False, help="Restore group config that was previously backed up")
menu.add_argument('--preview-entry', dest='preven', action='store_true', default=False, help="Preview Entry")
menu.add_argument('--install-grub-efi', dest='insgruf', action='store_true', default=False, help="Easiest to install GRUB EFI mode")
menu.add_argument('--install-grub-portable', dest='portabled', action='store_true', default=False, help="Install GRUB EFI to your external drives")
menu.add_argument('--secret-tools', dest='prank', action='store_true', default=False, help="Gk usah dipakek bang kalo gk mau nyesal ;)")
menu.add_argument('--set-config', dest='secon', action='store_true', default=False, help="Set config ini /etc/default/grub on TUI style")
menu.add_argument('--detect-os', dest='check_all_entry', action='store_true', default=False, help="Check all Entry from BIOS/UEFI")
menu.add_argument('--burn-iso', dest='flash', action='store_true', default=False, help="Easiest ISO Buring in TUI style!")
menu.add_argument('--set-prefix', dest='prefix', action='store_true', default=False, help="Set Default GRUB config file (/boot/grub/grub.cfg)")
menu.add_argument('--hh', dest='hh', action='store_true', default=False, help="Help Screen")
menu.add_argument('--dont-clear', dest='dclr', action='store_true', default=False, help="Dont Clear terminal")
menu.add_argument('--easy-mode', dest='easmod', action='store_true', default=False, help='Enter to easy mode, friendly TUI')
menu.add_argument('--update', dest='update', action='store_true', default=False, help='Update this tools')
option = menu.parse_args()

check_os = option.check_os
update_grubs = option.upgr
install_grubs = option.insgruf
pranks = option.prank
configs = option.secon
portable = option.portabled
reconf = option.reconf
detect_os = option.check_all_entry
dclr = option.dclr
iso_burner = option.flash
prefix = option.prefix
easy_mode = option.easmod
preven = option.preven
hh = option.hh
updates = option.update

if detect_os:
    try:
        if dclr:
            pass
        else:
            os.system("cls || clear")

        banner()
        from core_tools.os_prober import os_prober
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
        os_prober()
        exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] OS Prober (core_tools/os_prober.py > os_prober) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if check_os:
    if dclr:
        pass
    else:
        os.system("cls || clear")

    banner()
    def root_id():
        return os.getuid() == 0
    if root_id():
        pass
    else:
        print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
    try:
        from core_tools.os_prober import check_os
        check_os()
        sys.exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] OS information Finder (core_tools/os_prober > check_os) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if prefix:
    try:
        if dclr:
            pass
        else:
            os.system("cls || clear")

        banner()
        from core_tools.configures import set_prefix
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
        set_prefix()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] Set Prefix (core_tools/configures.py > set_prefix) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if pranks:
    try:
        if dclr:
            pass
        else:
            os.system("cls || clear")

        banner()
        from core_tools.configures import just_prank
        def user_uid():
            return os.getuid() !=0
        if user_uid():
            pass
        else:
            print(putih+"\n ["+merah+"!"+putih+"] using experimental secret features with sudo is dangerous!")
            print(putih+" ["+merah+"*"+putih+"] But this feature can still make changes to your system!");sys.exit()
        just_prank()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] Secreet Tools (core_tools/configures.py > ester_egg) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if iso_burner:
    try:
        if dclr:
            pass
        else:
            os.system("cls || clear")

        banner()
        def root_id():
            return os.getuid() == 0
        if root_id():
            pass
        else:
            print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
        from core_tools.tools_extra import burner_iso
        burner_iso()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] ISO Burner (core_tools/tools_extra.py > burner_iso) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if install_grubs:
    if dclr:
        pass
    else:
        os.system("cls || clear")

    banner()
    def root_id():
        return os.getuid() == 0
    if root_id():
        pass
    else:
        print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
    try:
        from core_tools.configures import install_grub_efi
        install_grub_efi()
        sys.exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] Install GRUB EFI (core_tools/configures > install_grub_efi) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if update_grubs:
    if dclr:
        pass
    else:
        os.system("cls || clear")

    banner()
    def root_id():
        return os.getuid() == 0
    if root_id():
        pass
    else:
        print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
    try:
        from core_tools.configures import update_grub_config
        update_grub_config(reconf=reconf)
        sys.exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] GRUB Config Updater (core_tools/configures > update_grub_config) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if reconf:
    if dclr:
        pass
    else:
        os.system("cls || clear")

    banner()
    def root_id():
        return os.getuid() == 0
    if root_id():
        pass
    else:
        print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
    try:
        from core_tools.configures import update_grub_config
        update_grub_config(reconf=True)
        sys.exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] GRUB Config Updater (core_tools/configures > update_grub_config) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if portable:
    if dclr:
        pass
    else:
        os.system("cls || clear")

    banner()
    def root_id():
        return os.getuid() == 0
    if root_id():
        pass
    else:
        print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
    try:
        from core_tools.configures import install_grub_portable
        install_grub_portable()
        sys.exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] GRUB EFI Portable Installer (core_tools/configures > install_grub_portable) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if configs:
    if dclr:
        pass
    else:
        os.system("cls || clear")

    banner()
    def root_id():
        return os.getuid() == 0
    if root_id():
        pass
    else:
        print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
    try:
        from core_tools.configures import change_etc_default_grub
        change_etc_default_grub()
        sys.exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] GRUB default variabel config editor (core_tools/configures > change_etc_default_grub) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if easy_mode:
    if dclr:
        pass
    else:
        os.system("cls || clear")

    banner()
    def root_id():
        return os.getuid() == 0
    if root_id():
        pass
    else:
        print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
    try:
        from core_tools.easy_mode import easy_mode
        easy_mode()
        sys.exit()
    except ImportError:
        print(f" [{merah}!{putih}] Easy Mode(core_tools/easy_mode > easy_mode) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if preven:
    if dclr:
        pass
    else:
        os.system("cls || clear")

    banner()
    def root_id():
        return os.getuid() == 0
    if root_id():
        pass
    else:
        print(putih+"\n ["+merah+"!"+putih+"] Please run this script with SUDO/SU"+reset);sys.exit()
    try:
        from core_tools.configures import preview_grub_entry
        preview_grub_entry()
        sys.exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] GRUB Entry Preview (core_tools/configures > preview_grub_entry) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if updates:
    try:
        if dclr:
            pass
        else:
            os.system("cls || clear")

        banner()
        def user_uid():
            return os.getuid() !=0
        if user_uid():
            pass
        else:
            print(f"{bmerah} # {reset}This will just update the tools")
            print(f"{bmerah} # {reset}No need to use sudo/SU"); time.sleep(1.3)
            sys.exit()
        from core_tools.updater import updates
        updates()
        sys.exit()
    except ImportError:
        print(putih+" ["+merah+"!"+putih+"] Secreet Tools (core_tools/updater > updates) Not found!"); sys.exit()
    except KeyboardInterrupt:
        print(f"{bmerah}*{reset} Exit, Have a nice day!");sys.exit()

if hh:
    bantuan()

else:
    os.system("cls || clear")
    banner()
    subscribe = input(borange+" > "+reset+merah+"Subscribe "+reset+"to my channel (y/n) ")
    if subscribe.lower() == 'y':
        print(bhijau+" # "+reset+"Thank's, buddy!")
        webbrowser.open("https://youtube.com/@linggachannel4781")
        with open("extras/cache", 'w') as cache:
            cache.write('')
        exit()
    else:
        print("OK")
        exit()
