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
            print(f"Tracknumber: {afile['tracknumber'][0]} => {result}")
            afile["tracknumber"] = result

        if args.autotitle and args.sep:
            sep = args.sep[0]
            fname = f.split(sep=sep)
            start, end = args.autotitle[0], args.autotitle[1]
            result = " ".join(fname[start:end])
            print(f"Title: {afile['title'][0]} => {result}")
            afile["title"] = result
        elif args.autotitle and not args.sep or not args.autotitle and args.sep:
            raise TypeError("Autotitling requires both --autotitle and --sep")

        if args.re_title:
            result = re.sub(r"{}".format(args.re_title[0]),
                            args.re_title[1], afile["title"][0])
            print(f"Title: {afile['title'][0]} => {result}")
            afile["title"] = result

        if args.re_album:
            result = re.sub(r"{}".format(args.re_album[0]),
                            args.re_album[1], afile["album"][0])
            print(f"Album: {afile['album'][0]} => {result}")
            afile["album"] = result

        if args.re_description:
            result = re.sub(r"{}".format(args.re_description[0]),
                            args.re_description[1],
                            afile["description"][0])
            print(f"Description: {afile['description'][0]} => {result}")
            afile["description"] = result

        if args.title:
            result = args.title[0]
            print(afile["title"])
            print(f"Title: {afile['title'][0]} => {result}")
            afile["title"] = result

        if args.artist:
            result = args.artist[0]
            print(f"Artist: {afile['artist'][0]} => {result}")
            afile["artist"] = result

        if args.album:
            result = args.album[0]
            print(f"Album: {afile['album'][0]} => {result}")
            afile["album"] = result

        if args.genre:
            result = args.genre[0]
            print(f"Genre: {afile['genre'][0]} => {result}")
            afile["genre"] = result

        if args.date:
            result = args.date[0]
            print(f"Date: {afile['date'][0]} => {result}")
            afile["date"] = str(result)

        if args.tracktotal:
            result = args.tracktotal[0]
            print(f"Tracktotal: {afile['tracktotal'][0]} => {result}")
            afile["tracktotal"] = str(result)

        if args.description:
            result = args.description[0]
            print(f"Description: {afile['description'][0]} => {result}")
            afile["description"] = result

        if args.delete:
            for kd in args.delete:
                print(f"Delete {kd}")
                afile.pop(kd, None)

        if confirm_all is False:
            confirmation = input("Save these changes? (Y/n/!/q) ")

        if confirmation in ("", 'y', '!') or confirm_all:
            afile.pprint()
            afile.save()
            if confirmation == '!' and not confirm_all:
                confirm_all = True
            print("")
        elif confirmation == 'q':
            print("Exiting.")
            sys.exit(0)
        else:
            print("Not saving further changes.")


if __name__ == '__main__':
    sys.exit(main())
