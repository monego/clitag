#!@PYTHON@

# clitag.py
#
# Copyright (C) 2020, 2021 Vinicius Monego
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table
import argparse
import re
import sys
import mutagen


parser = argparse.ArgumentParser(description='clitag')
console = Console()

at_group = parser.add_argument_group('autotitle')
at_group.add_argument('--autotitle', type=int, nargs=2,
                      metavar=('START', 'END'),
                      help="Autotitle based on filename. Requires --sep")
at_group.add_argument('--sep', type=str, nargs=1,
                      help="Separator for autotitle")

tgroup = parser.add_mutually_exclusive_group()
tgroup.add_argument('--title', type=str, nargs=1,
                    help='Set audio title')
tgroup.add_argument('--re-title', type=str, nargs=2,
                    metavar=('REGEXP', 'REPLACEMENT'),
                    help='Change audio title using regular expressions')

agroup = parser.add_mutually_exclusive_group()
agroup.add_argument('--album', type=str, nargs=1,
                    help='Set audio album')
agroup.add_argument('--re-album', type=str, nargs=2,
                    metavar=('REGEXP', 'REPLACEMENT'),
                    help='Change audio album using regular expressions')

dgroup = parser.add_mutually_exclusive_group()
dgroup.add_argument('--description', type=str, nargs=1,
                    help='Set audio description')
dgroup.add_argument('--re-description', type=str, nargs=2,
                    metavar=('REGEXP', 'REPLACEMENT'),
                    help='Change audio description using regular expressions')

parser.add_argument('--interactive', action='store_true',
                    help='Approve each change manually')
parser.add_argument('--artist', type=str, nargs=1,
                    help='Set audio artist')
parser.add_argument('--genre', type=str, nargs=1,
                    help='Set audio genre')
parser.add_argument('--date', type=int, nargs=1,
                    help='Set audio date')
parser.add_argument('--tracktotal', type=int, nargs=1,
                    help='Number of tracks in the album')
parser.add_argument('--autonumber', action='store_true',
                    help="Autonumber the track files")
parser.add_argument('--delete', type=str, nargs='+',
                    help="Delete some keys")
parser.add_argument('files', type=str, nargs='+',
                    help="The files to change")


def tag_exists(f, tag):
    try:
        return f[tag][0]
    except KeyError:
        return ""

def main():

    args = parser.parse_args()

    afile_list = []

    for n, f in enumerate(args.files):
        afile = mutagen.File(f)
        afile_list.append(afile)

        console.rule(f)

        table = Table(title=f.split('/')[-1])

        table.add_column("Tag", justify="center", style="cyan", no_wrap=True)
        table.add_column("Before", style="strike on red")
        table.add_column("After", justify="center", style="green")

        if args.autonumber:
            result = str(n+1)
            table.add_row("Tracknumber", tag_exists(afile, "tracknumber"), result)
            afile["tracknumber"] = result

        if args.autotitle and args.sep:
            sep = args.sep[0]
            fname = f.split(sep=sep)
            start, end = args.autotitle[0], args.autotitle[1]
            result = " ".join(fname[start:end])
            afile["title"] = result
            table.add_row("Title", tag_exists(afile, "title"), result)
        elif args.autotitle and not args.sep or not args.autotitle and args.sep:
            raise TypeError("Autotitling requires both --autotitle and --sep")

        if args.re_title:
            result = re.sub(r"{}".format(args.re_title[0]),
                            args.re_title[1], afile["title"][0])
            table.add_row("Title", tag_exists(afile, "title"), result)
            afile["title"] = result

        if args.re_album:
            result = re.sub(r"{}".format(args.re_album[0]),
                            args.re_album[1], afile["album"][0])
            table.add_row("Album", tag_exists(afile, "album"), result)
            afile["album"] = result

        if args.re_description:
            result = re.sub(r"{}".format(args.re_description[0]),
                            args.re_description[1],
                            afile["description"][0])
            table.add_row("Description", tag_exists(afile, "description"), result)
            afile["description"] = result

        if args.title:
            result = args.title[0]
            table.add_row("Title", tag_exists(afile, "title"), result)
            afile["title"] = result

        if args.artist:
            result = args.artist[0]
            table.add_row("Artist", tag_exists(afile, "artist"), result)
            afile["artist"] = result

        if args.album:
            result = args.album[0]
            table.add_row("Album", tag_exists(afile, "album"), result)
            afile["album"] = result

        if args.genre:
            result = args.genre[0]
            table.add_row("Genre", tag_exists(afile, "genre"), result)
            afile["genre"] = result

        if args.date:
            result = args.date[0]
            table.add_row("Date", tag_exists(afile, "date"), str(result))
            afile["date"] = str(result)

        if args.tracktotal:
            result = args.tracktotal[0]
            table.add_row("Tracktotal", tag_exists(afile, "tracktotal"), result)
            afile["tracktotal"] = str(result)

        if args.description:
            result = args.description[0]
            table.add_row("Description", tag_exists(afile, "description"), result)
            afile["description"] = result

        if args.delete:
            for kd in args.delete:
                print(f"Delete {kd}")
                afile.pop(kd, None)

        console.print(table)

        if args.interactive:
            if Confirm.ask("Save these changes?"):
                afile.pprint()
                afile.save()

    if not args.interactive:
        if Confirm.ask("Save these changes?"):
            for afile in afile_list:
                afile.pprint()
                afile.save()

if __name__ == '__main__':
    sys.exit(main())
