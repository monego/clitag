# clitag

A CLI audio tag editor and processor written in Python 3.x using the `mutagen` module, with support for regular expressions and autonumbering. It's more intended for batch processing tags.

# Install

It can be installed through `pip`:

```bash
$ pip install git+https://codeberg.org/monego/clitag.git
```

# Usage

Set some tags for all audio files in a folder:

```bash
$ clitag --artist "Someone" --album "Something" afolder/*.opus
```

Delete a tag:

```bash
$ clitag --delete "genre" afolder/*.opus
```

Use a regular expression to replace something in a tag:

```bash
$ clitag --re-title "regexp" "replacement" afolder/*.opus
```

Autonumber an album:

```bash
$ clitag --autonumber afolder/*.opus
```

Autotitle based on filename. Give it a start, end, and a separator. For e.g. "[tracknumber] - Title - [Date]" use:

```bash
$ clitag --autotitle 2 -2 --sep " " afolder/*.opus
```

or

```bash
$ clitag --autotitle 1 -1 --sep "-" afolder/*.opus
```

. The title has to have the same separator at both ends.

# Dependencies

The only external dependency is `mutagen`.
