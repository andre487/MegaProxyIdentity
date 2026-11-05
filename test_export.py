"""Integration regression check; requires Inkscape."""

import pathlib
import shutil
import subprocess as sp
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


@unittest.skipUnless(shutil.which('inkscape'), 'Inkscape is required')
class ExportTest(unittest.TestCase):
    def test_export_preserves_group_labels_and_source(self):
        root = pathlib.Path(__file__).resolve().parent
        source = root / 'identity.svg'
        original = source.read_bytes()
        labels = {
            group.get('id'): group.get(
                '{http://www.inkscape.org/namespaces/inkscape}label'
            )
            for group in ET.fromstring(original).iter('{http://www.w3.org/2000/svg}g')
            if group.get('{http://www.inkscape.org/namespaces/inkscape}label')
        }
        with tempfile.TemporaryDirectory() as temporary:
            sp.run(
                [sys.executable, str(root / 'export.py'), '--output-dir', temporary],
                check=True,
                capture_output=True,
            )
            exports = list(pathlib.Path(temporary).glob('*.svg'))
            self.assertEqual(
                {path.name for path in (root / 'SVG').glob('*.svg')},
                {path.name for path in exports},
            )
            for path in exports:
                for group in ET.parse(path).iter('{http://www.w3.org/2000/svg}g'):
                    if group.get('id') in labels:
                        self.assertEqual(
                            labels[group.get('id')], group.get('data-name'), path.name
                        )
            for name in ('icon', 'icon-radius', 'icon-round', 'icon-toolbar'):
                tree = ET.parse(pathlib.Path(temporary) / f'{name}.svg').find(
                    f"./{{http://www.w3.org/2000/svg}}g[@data-name='{name}']"
                )
                self.assertIsNotNone(tree)
                for label in ('foreground', 'background'):
                    self.assertEqual(
                        1,
                        len(
                            tree.findall(
                                f".//{{http://www.w3.org/2000/svg}}g[@data-name='{label}']"
                            )
                        ),
                    )
        self.assertEqual(original, source.read_bytes())


if __name__ == '__main__':
    unittest.main()
