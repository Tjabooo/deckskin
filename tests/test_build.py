import os
import struct
import sys
import tempfile
import tomllib
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import deckskin_cursor as cursor  # noqa: E402
import deckskin_firefox as firefox  # noqa: E402


def palette(name):
    with open(os.path.join(ROOT, "palettes", name + ".toml"), "rb") as fh:
        return tomllib.load(fh)


class Build(unittest.TestCase):
    def test_every_shape_renders_valid_svg(self):
        c = palette("ember")["colors"]
        for name in cursor.ALIASES:
            for f in range(cursor.frames(name)):
                svg = cursor.build_shape(name, c, f)
                self.assertTrue(svg.startswith("<svg") and svg.endswith("</svg>"), name)

    def test_xcursor_files(self):
        with tempfile.TemporaryDirectory() as d:
            dest, _ = cursor.build(palette("neon"), d, hyprcursor=False)
            data = open(os.path.join(dest, "cursors", "wait"), "rb").read()
            magic, hdr, _, ntoc = struct.unpack("<4sIII", data[:16])
            self.assertEqual((magic, hdr), (b"Xcur", 16))
            self.assertEqual(ntoc, len(cursor.XCURSOR_SIZES) * cursor.SPIN_FRAMES)
            self.assertEqual(os.readlink(os.path.join(dest, "cursors", "left_ptr")), "default")

    def test_firefox_css_has_palette(self):
        pal = palette("ember")
        chrome, content = firefox.render(pal, "ember")
        self.assertIn(pal["colors"]["accent"], chrome)
        self.assertIn(pal["colors"]["bg"], content)
        self.assertNotIn("$", chrome.replace("$accent", ""))

    def test_prefs_block_replaces_itself(self):
        with tempfile.TemporaryDirectory() as d:
            ujs = os.path.join(d, "user.js")
            open(ujs, "w").write('user_pref("a", 1);\n')
            for _ in range(2):
                firefox.write_prefs_block(ujs, firefox.prefs_block(palette("neon")))
            s = open(ujs).read()
            self.assertEqual(s.count(firefox.PREFS_MARK[0]), 1)
            self.assertIn('user_pref("a", 1);', s)


if __name__ == "__main__":
    unittest.main()
