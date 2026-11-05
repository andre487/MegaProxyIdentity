# MegaProxy Identity

Graphic items for MegaProxy apps

Export all pages from `identity.svg` to `SVG/` (requires Python 3 and Inkscape 1.2+):

```sh
python3 export.py
```

File names follow the page labels in Inkscape. Existing matching files are
overwritten; other files are kept. To export elsewhere, use
`python3 export.py --output-dir /tmp/megaproxy-svg`.

Group labels are preserved as plain SVG `data-name` attributes. Consumers can
select the `foreground` and `background` groups without depending on generated
IDs or the structure inside each group. The original `identity.svg` is unchanged.

Run the export regression check with `python3 -m unittest -v test_export`
(requires Inkscape).
