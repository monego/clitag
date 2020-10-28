# clitag

A CLI audio tag editor and processor written in Python 3.x using the `mutagen` module, with support for regular expressions and autonumbering. It's more intended for batch processing tags.

# Usage

Set some tags for all audio files in a folder:

```bash
$ clitag --artist "Someone" --album "Something"  --files afolder/*.opus
```

Delete a tag:

```bash
$ clitag --delete "genre" --files afolder/*.opus
```

Use a regular expression to replace something in a tag:

```bash
$ clitag --re --title "s/pattern/sub/g" --files afolder/*.opus
```

Autonumber an album:

```bash
$ clitag --autonumber --files afolder/*.opus
```

Autotitle based on filename. Give it a start, end, and a separator. For e.g. "[tracknumber] - Title - [Date]" use:

```bash
$ clitag --autotitle 2 -2 --sep " " --files afolder/*.opus
```

or

```bash
$ clitag --autotitle 1 -1 --sep "-" --files afolder/*.opus
```

. The title has to have the same separator at both ends.

# Dependencies

The only external dependency is `mutagen`.
