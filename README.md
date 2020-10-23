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

# Dependencies

The only external dependency is `mutagen`.
