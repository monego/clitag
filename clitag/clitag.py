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

import argparse
import re
import sys
import mutagen


parser = argparse.ArgumentParser(description='clitag')

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

parser.add_argument('--check', action='store_true',
                    help='List audio files and tags')
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


def print_change(name, afile, key, result):
    """ Print changes before applying. """
    if key in afile.keys():
        print(f"{name}: {afile[key][0]} => {result}")
    else:
        print(f"{name}:   => {result}")


def confirm(afile, confirm_all):
    """ Ask for user confirmation. """
    if confirm_all is False:
        user_confirm = input("Save these changes? (Y/n/!/q) ")
    else:
        user_confirm = '!'

    if user_confirm in ('', 'y', 'Y', '!') or confirm_all:
        afile.pprint()
        afile.save()
        if user_confirm == '!' and not confirm_all:
            confirm_all = True
        print("Saved change.")
    elif user_confirm in ('n', 'N'):
        print("Not saving this change.")
    elif user_confirm == 'q':
        print("Exiting.")
        sys.exit(0)
    else:
        print("Please answer y/n/!/q.")
        confirm(afile, confirm_all)
    return confirm_all

def main():

    confirm_all = False

    args = parser.parse_args()

    for n, f in enumerate(args.files):
        afile = mutagen.File(f)

        if args.check:
            for key, value in afile.items():
                print(key, ': ', value)
            print("")

        if args.autonumber:
            result = str(n+1)
            print_change("Tracknumber", afile, "tracknumber", result)
            afile["tracknumber"] = result

        if args.autotitle and args.sep:
            sep = args.sep[0]
            fname = f.split(sep=sep)
            start, end = args.autotitle[0], args.autotitle[1]
            result = " ".join(fname[start:end])
            afile["title"] = result
            print_change("Title", afile, "title", result)
        elif args.autotitle and not args.sep or not args.autotitle and args.sep:
            raise TypeError("Autotitling requires both --autotitle and --sep")

        if args.re_title:
            result = re.sub(r"{}".format(args.re_title[0]),
                            args.re_title[1], afile["title"][0])
            print_change("Title", afile, "title", result)
            afile["title"] = result

        if args.re_album:
            result = re.sub(r"{}".format(args.re_album[0]),
                            args.re_album[1], afile["album"][0])
            print_change("Album", afile, "album", result)
            afile["album"] = result

        if args.re_description:
            result = re.sub(r"{}".format(args.re_description[0]),
                            args.re_description[1],
                            afile["description"][0])
            print_change("Description", afile, "description", result)
            afile["description"] = result

        if args.title:
            result = args.title[0]
            print_change("Title", afile, "title", result)
            afile["title"] = result

        if args.artist:
            result = args.artist[0]
            print_change("Artist", afile, "artist", result)
            afile["artist"] = result

        if args.album:
            result = args.album[0]
            print_change("Album", afile, "album", result)
            afile["album"] = result

        if args.genre:
            result = args.genre[0]
            print_change("Genre", afile, "genre", result)
            afile["genre"] = result

        if args.date:
            result = args.date[0]
            print_change("Date", afile, "date", result)
            afile["date"] = str(result)

        if args.tracktotal:
            result = args.tracktotal[0]
            print_change("Tracktotal", afile, "tracktotal", result)
            afile["tracktotal"] = str(result)

        if args.description:
            result = args.description[0]
            print_change("Description", afile, "description", result)
            afile["description"] = result

        if args.delete:
            for kd in args.delete:
                print(f"Delete {kd}")
                afile.pop(kd, None)

        confirm_all = confirm(afile, confirm_all)

if __name__ == '__main__':
    sys.exit(main())
