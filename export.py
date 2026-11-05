#!/usr/bin/env python3
"""Export identity.svg pages as plain SVG files using Inkscape."""

import argparse
import pathlib
import re
import shutil
import subprocess as sp
import tempfile
import xml.etree.ElementTree as ET


def main():
    root = pathlib.Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--output-dir',
        type=pathlib.Path,
        default=root / 'SVG',
        help='Destination directory (default: SVG next to this script)',
    )
    args = parser.parse_args()
    inkscape = shutil.which('inkscape')
    if inkscape is None:
        parser.error('Inkscape must be installed and available in PATH')

    source = root / 'identity.svg'
    document = ET.parse(source)
    svg_namespace = '{http://www.w3.org/2000/svg}'
    for clip in document.iter(f'{svg_namespace}clipPath'):
        if clip.find(f'{svg_namespace}g') is not None:
            parser.error(
                f'Clip path {clip.get("id")!r} contains a group; '
                'ungroup its shapes before exporting for browser compatibility'
            )
    pages = document.findall('.//{http://www.inkscape.org/namespaces/inkscape}page')
    if not pages:
        parser.error('No Inkscape pages found in identity.svg')

    names = []
    for page in pages:
        name = page.get('{http://www.inkscape.org/namespaces/inkscape}label', '')
        if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
            parser.error(f'Invalid or missing page label: {name!r}')
        if name in names:
            parser.error(f'Duplicate page label: {name!r}')
        names.append(name)

    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    # Finish all exports before replacing any existing files.
    with tempfile.TemporaryDirectory(prefix='.export-', dir=output) as temporary:
        temporary = pathlib.Path(temporary)
        for number, name in enumerate(names, start=1):
            sp.run(
                [
                    inkscape,
                    str(source),
                    f'--export-page={number}',
                    '--export-area-page',
                    '--export-type=svg',
                    '--export-plain-svg',
                    f'--export-filename={temporary / (name + ".svg")}',
                ],
                check=True,
            )
            ET.parse(temporary / f'{name}.svg')

        for name in names:
            destination = output / f'{name}.svg'
            (temporary / destination.name).replace(destination)
            print(f'Exported {destination}')


if __name__ == '__main__':
    main()
