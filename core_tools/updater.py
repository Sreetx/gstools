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

import os, time, sys, requests

from color.warna import borange
from color.warna import reset
from color.warna import banner
from color.warna import bhijau

from rich import print
from rich.live import Live
from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box

def updates():
    #setiap pembaruan akan menambahkan fitur ini

    print("[bold orange1] ~ [/bold orange1]Checking Update..."); time.sleep(0.2)

    found = False
    version = ["v2.2.12-#Beta", "v2.2.11-#Beta", "v2.2.13-#Beta"]
    for versin in version:
        encoded_version = versin.replace("#", "%23")
        url = f"https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/extras/{encoded_version}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"[bold green] * [/bold green]Found Version: {versin}"); time.sleep(1.3)
                cs = input(f"{bhijau} ? {reset}Continue Update to {versin} (y/n) ")
                if cs.strip().lower() != "n":
                    #run update
                    print("[bold green] ~ [/bold green]Downloading Update...")
                    
                    #true update
                    main = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/main.py")
                    color = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/color/warna.py")
                    configures = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/core_tools/configures.py")
                    easy_mode = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/core_tools/easy_mode.py")
                    loading_bar = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/core_tools/loading_bar.py")
                    os_prober = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/core_tools/os_prober.py")
                    tools_extra = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/core_tools/tools_extra.py")
                    updater = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/core_tools/updater.py")
                    grub_modules = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/extras/grub-modules.txt")
                    sans = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/extras/sans.txt")
                    versiond = requests.get("https://raw.githubusercontent.com/Sreetx/gstools/refs/heads/master/extras/version.vers")

                    print("\n[bold orange1] > [/bold orange1]Installing main"); time.sleep(0.5)
                    with open ("main.py", 'wb') as a:
                        a.write(main.content)

                    print("[bold orange1] > [/bold orange1]Installing warna/color"); time.sleep(0.5)
                    with open("color/warna.py", 'wb') as b:
                        b.write(color.content)
                    
                    print("[bold orange1] > [/bold orange1]Installing core_tools/configures"); time.sleep(0.5)
                    with open("core_tools/configures.py", 'wb') as c:
                        c.write(configures.content)

                    print("[bold orange1] > [/bold orange1]Installing core_tools/easy_mode"); time.sleep(0.5)
                    with open("core_tools/easy_mode.py", 'wb') as d:
                        d.write(easy_mode.content)

                    print("[bold orange1] > [/bold orange1]Installing core_tools/loading_bar"); time.sleep(0.5)
                    with open("core_tools/loading_bar.py", 'wb') as e:
                        e.write(loading_bar.content)

                    print("[bold orange1] > [/bold orange1]Installing core_tools/os_prober"); time.sleep(0.5)
                    with open("core_tools/os_prober.py", 'wb') as f:
                        f.write(os_prober.content)
                    
                    print("[bold orange1] > [/bold orange1]Installing core_tools/tools_extra"); time.sleep(0.5)
                    with open("core_tools/tools_extra.py", 'wb') as g:
                        g.write(tools_extra.content)

                    print("[bold orange1] > [/bold orange1]Installing Extras"); time.sleep(0.5)
                    with open("extras/sans.txt", 'wb') as h:
                        h.write(sans.content)
                    with open("extras/grub_modules.txt", 'wb') as i:
                        i.write(grub_modules.content)
                    with open("extras/version.vers", 'wb') as j:
                        j.write(versiond.content)
                    
                    print("[bold orange1] > [/bold orange1]Installing core_tools/updater"); time.sleep(0.5)
                    with open("core_tools/updater.py", 'wb') as k:
                        k.write(updater.content)
                    
                    print("\n[bold green] # [/bold green] Done")

                    found = True
                    break
                    
        except KeyboardInterrupt: print("Exit"); sys.exit()
    
    if not found:
        print("[bold orange1] # [/bold orange1]This tools is up to date!"); sys.exit()
