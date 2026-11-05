# MegaProxy Identity

Graphic items for MegaProxy apps

Export all pages from `identity.svg` to `SVG/` (requires Python 3 and Inkscape 1.2+):

```sh
python3 export.py
```

File names follow the page labels in Inkscape. Existing matching files are
overwritten; other files are kept. To export elsewhere, use
`python3 export.py --output-dir /tmp/megaproxy-svg`.
