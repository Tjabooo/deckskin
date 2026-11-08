import os
import struct
import sys
import tempfile
import tomllib
import unittest
import unittest.mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import deckskin_cursor as cursor  # noqa: E402
import deckskin_firefox as firefox  # noqa: E402
import deckskin_spotify as spotify  # noqa: E402


def palette(name):
    with open(os.path.join(ROOT, "palettes", name + ".toml"), "rb") as fh:
        return tomllib.load(fh)


class Build(unittest.TestCase):
    def test_spotify_theme_uses_only_the_palette(self):
        for slug in ("ember", "neon"):
            pal = palette(slug)
            ini = spotify.render_colors(pal, slug)
            self.assertTrue(ini.startswith(f"[{slug}]"))
            for key in ("text", "subtext", "main", "sidebar", "player", "card", "button", "selected-row"):
                self.assertRegex(ini, rf"(?m)^{key}\s*= [0-9a-f]{{6}}$")
            css = spotify.render_css(pal, slug)
            self.assertNotIn("$", css)
            self.assertIn(pal["colors"]["accent"], css)
            self.assertNotIn("1ed760", css.lower())
            self.assertEqual(css.count("{"), css.count("}"))

    def test_spotify_equaliser_rotates_green_onto_the_accent(self):
        self.assertIn("hue-rotate(-111deg)", spotify.equaliser_filter({"colors": {"accent": "#ff8000"}}))

    def test_spotify_restart_drops_debug_flags(self):
        with unittest.mock.patch("builtins.open") as fake:
            fake.return_value.__enter__.return_value.read.return_value = (
                b"/opt/spotify/spotify\0--ozone-platform=wayland\0--remote-debugging-port=9333\0"
            )
            self.assertEqual(spotify.launch_args(1), ["/opt/spotify/spotify", "--ozone-platform=wayland"])

    def test_spotify_restart_handles_the_rewritten_process_title(self):
        with unittest.mock.patch("builtins.open") as fake:
            fake.return_value.__enter__.return_value.read.return_value = (
                b"/opt/spotify/spotify --enable-features=A,B --ozone-platform=wayland\0"
            )
            self.assertEqual(spotify.launch_args(1),
                             ["/opt/spotify/spotify", "--enable-features=A,B", "--ozone-platform=wayland"])

    def test_spotify_unpatched_means_the_spa_is_back(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "Apps"))
            self.assertFalse(spotify.is_unpatched(d))
            open(os.path.join(d, "Apps", "xpui.spa"), "w").close()
            self.assertTrue(spotify.is_unpatched(d))

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
