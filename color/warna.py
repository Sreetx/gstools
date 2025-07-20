# warna.py
#
# Copyright 2024-2025 Programmer
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

console = Console()

if sys.platform in ["linux", "linux2", "win32", "win64"]:
    orange = "\033[93m"
    putih = "\033[39m"
    merah = "\033[91m"
    hijau = "\033[92m"
    biru = "\033[94m"
    borange = "\033[1;93m"
    bputih = "\033[1;39m"
    bmerah = "\033[1;91m"
    bhijau = "\033[1;92m"
    bbiru = "\033[1;94m"
    banhijau = "\033[7;92m"
    kelabu = "\033[90m"
    borangekelip = "\033[5;93m"
    banmerah = "\033[7;91m"
    banorange = "\033[7;93m"
    reset = "\033[0m"
else:
    orange = ""
    putih = ""
    merah = ""
    hijau = ""
    biru = ""
    borange = ""
    bputih = ""
    bmerah = ""
    bhijau = ""
    bbiru = ""
    kelabu = ""
    borangekelip = ""
    banhijau = ""
    banmerah = ""
    reset = ""

try:
    import sys, os
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    print(f'{bmerah} ! {reset}Please Install "python-rich" or "python3-rich"'); sys.exit()

def banner():
    ss = os.path.join('color', 'tux-colored.txt')
    with open (ss, 'r', encoding='utf-8') as logo:
        logg = logo.read()
    version = os.path.join('extras', 'version.vers')
    with open (version, 'r') as versi:
        vers = versi.read()
        vers = vers.strip()

    header = Text.from_markup("[green]>[/green] [bold white]GRUB Sreetx Tools[/bold white], [italic white]Easy to Control Your GRUB in your Linux![/italic white]")
    print('')
    console.print(Panel(header, expand=False, border_style='green'))

    credits = Table(show_header=False, show_edge=False, pad_edge=False, box=None)
    credits.add_row("[bold green]*[/bold green]", "[orange1]Author[/orange1]", ": Lingga Channel")
    credits.add_row("[bold green]*[/bold green]", "[orange1]YouTube[/orange1]", ": https://youtube.com/@linggachannel4781")
    credits.add_row("[bold green]*[/bold green]", "[orange1]GitHub[/orange1]", ": https://github.com/Sreetx")
    credits.add_row("[bold green]*[/bold green]", "[orange1]Version[/orange1]", f": {vers}")
    credits.add_row("[bold green]*[/bold green]", "[orange1]License[/orange1]", ": GNU GPL v3")

    console.print(credits)

    #INFO, Subscribe lahh
    console.print(Panel.fit(
        "[bold orange1]#[/bold orange1] Let's Join to my Channel!\n"
        "[orange1]*[/orange1] Subscribe atau ku hitamkan kalian 😈\n"
        "[orange1]*[/orange1] python3 main.py --easy-mode\n"
        "[orange1]>[/orange1] You can use the special commands above for easier use!\n"
        "[bold orange1]HELP COMMAND[/bold orange1] python3 main.py --hh",
        title = "[bold green]INFO[/bold green]",
        border_style = "orange1"
    ))


