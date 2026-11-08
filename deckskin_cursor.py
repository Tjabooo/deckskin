"""Cursor theme: SVG shapes drawn on a 24-unit grid, built into Xcursor + hyprcursor."""
import os
import shutil
import struct
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

from PIL import Image

XCURSOR_SIZES = (24, 32, 36, 48, 64, 72, 96)
SPIN_FRAMES = 16
SPIN_DELAY = 50  # ms per frame

# canonical (CSS) name -> aliases (X11 names, Qt/GTK hash names, CSS synonyms)
ALIASES = {
    "default": ["left_ptr", "arrow", "top_left_arrow", "left_arrow"],
    "pointer": ["hand", "hand1", "hand2", "pointing_hand",
                "9d800788f1b08800ae810202380a0822", "e29285e634086352946a0e7090d73106"],
    "text": ["xterm", "ibeam"],
    "vertical-text": [],
    "wait": ["watch", "clock"],
    "progress": ["left_ptr_watch", "half-busy",
                 "08e8e1c95fe2fc01f976f1e063a24ccd", "3ecb610c1bf2410f44200f48c40d3599"],
    "crosshair": ["cross", "tcross", "cross_reverse", "diamond_cross", "color-picker", "target"],
    "cell": ["plus"],
    "move": ["fleur", "size_all", "all-scroll", "4498f0e0c1937ffe01fd06f973665830",
             "9081237383d90e509aa00f00170e968f"],
    "grab": ["openhand"],
    "grabbing": ["closedhand", "dnd-move", "dnd_move", "fcf21c00b30f7e3f83fe0dfd12e71cff"],
    "not-allowed": ["crossed_circle", "forbidden", "circle", "X_cursor", "pirate",
                    "03b6e0fcb3499374a867c041f52298f0"],
    "no-drop": ["dnd-none", "dnd_no_drop"],
    "help": ["question_arrow", "whats_this", "left_ptr_help", "dnd-ask",
             "5c6cd98b3f3ebcb1f9c7f1c204630408", "d9ce0ab605698f320427677b458ad60b"],
    "context-menu": [],
    "copy": ["dnd-copy", "1081e37283d90000800003c07f3ef6bf", "6407b0e94181790501fd1e167b474872"],
    "alias": ["link", "dnd-link", "3085a0e285430894940527032f8b26df",
              "640fb0e74195791501fd1ed57b41487f"],
    "zoom-in": ["zoom_in"],
    "zoom-out": ["zoom_out"],
    "ns-resize": ["n-resize", "s-resize", "top_side", "bottom_side", "sb_v_double_arrow",
                  "v_double_arrow", "size_ver", "double_arrow", "00008160000006810000408080010102"],
    "ew-resize": ["e-resize", "w-resize", "left_side", "right_side", "sb_h_double_arrow",
                  "h_double_arrow", "size_hor", "028006030e0e7ebffc7f7070c0600140"],
    "nwse-resize": ["nw-resize", "se-resize", "top_left_corner", "bottom_right_corner",
                    "bd_double_arrow", "size_fdiag", "c7088f0f3e6c8088236ef8e1e3e70000"],
    "nesw-resize": ["ne-resize", "sw-resize", "top_right_corner", "bottom_left_corner",
                    "fd_double_arrow", "size_bdiag", "fcf1c3c7cd4491d801f1e1c78f100000"],
    "col-resize": ["split_h", "14fef782d02440884392942c11205230"],
    "row-resize": ["split_v", "2870a09082c103050810ffdffffe0204"],
    "right_ptr": ["draft_large", "draft_small"],
}

# the pointer: a tailless wedge, tip on the hotspot
WEDGE = "M4 2 L4 19.5 L8.6 15.3 L15.6 15.3 Z"


class Painter:
    """Builds one SVG; every glyph sits on a translucent bg halo + soft shadow."""

    def __init__(self, c):
        self.c = c
        self.body = []
        self.defs = []
        self.n = 0

    def uid(self):
        self.n += 1
        return f"u{self.n}"

    def panel(self, d, stroke=None, width=1.5, transform=""):
        """Dark body, accent outline drawn inside the shape (keeps edges on the grid)."""
        c, cid = self.c, self.uid()
        t = f' transform="{transform}"' if transform else ""
        self.defs.append(f'<clipPath id="{cid}"><path d="{d}"{t}/></clipPath>')
        self.body.append(
            f'<path d="{d}"{t} fill="{c["bg"]}" stroke="{c["bg"]}" stroke-opacity="0.7" '
            f'stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="{d}"{t} fill="none" stroke="{stroke or "url(#acc)"}" '
            f'stroke-width="{width * 2}" clip-path="url(#{cid})"/>')
        return cid

    def chip(self, d, fill="url(#acc)", transform=""):
        """Solid accent body with a bg halo."""
        t = f' transform="{transform}"' if transform else ""
        self.body.append(
            f'<path d="{d}"{t} fill="{fill}" stroke="{self.c["bg"]}" stroke-opacity="0.75" '
            f'stroke-width="2.2" stroke-linejoin="round" paint-order="stroke"/>')

    def raw(self, s):
        self.body.append(s)

    def svg(self):
        c = self.c
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">'
            '<defs>'
            '<filter id="sh" x="-40%" y="-40%" width="180%" height="180%">'
            '<feGaussianBlur in="SourceAlpha" stdDeviation="0.55"/>'
            '<feOffset dx="0.45" dy="0.8"/>'
            '<feComponentTransfer><feFuncA type="linear" slope="0.45"/></feComponentTransfer>'
            '<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<linearGradient id="acc" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{c["accent"]}"/>'
            f'<stop offset="0.55" stop-color="{c["accent"]}"/>'
            f'<stop offset="1" stop-color="{c["deep"]}"/></linearGradient>'
            + "".join(self.defs) +
            '</defs><g filter="url(#sh)">' + "".join(self.body) + '</g></svg>')


# ---------------------------------------------------------------- shapes

def arrow(p, mirror=False):
    t = "translate(24 0) scale(-1 1)" if mirror else ""
    if t:
        p.raw(f'<g transform="{t}">')
    cid = p.panel(WEDGE, width=1.25)
    # deck motif: an accent bar down the straight edge (it fills the tip solid)
    p.raw(f'<rect x="4" y="2" width="2.25" height="17.5" fill="url(#acc)" clip-path="url(#{cid})"/>')
    if t:
        p.raw('</g>')


def badge(p, fill="url(#acc)"):
    p.chip("M13.5 13.5 H21.5 V21.5 H13.5 Z", fill=fill)


def spinner(p, x, y, s, w, frame, track):
    """Square track with a bright segment running round it (deck version of a throbber)."""
    c = p.c
    per = 4 * s
    seg = per / 3
    off = -per * frame / SPIN_FRAMES
    d = f"M{x} {y} H{x + s} V{y + s} H{x} Z"
    p.raw(f'<path d="{d}" fill="{c["bg"]}" stroke="{c["bg"]}" stroke-opacity="0.75" '
          f'stroke-width="{w + 2.2}"/>')
    p.raw(f'<path d="{d}" fill="none" stroke="{track}" stroke-width="{w}"/>')
    p.raw(f'<path d="{d}" fill="none" stroke="{c["accent"]}" stroke-width="{w}" '
          f'stroke-dasharray="{seg:.3f} {per - seg:.3f}" stroke-dashoffset="{off:.3f}"/>')
    # a dot in the middle that trades colour every half turn
    dot = c["accent2"] if frame < SPIN_FRAMES // 2 else c["deep"]
    m = s / 2 - 1
    p.raw(f'<rect x="{x + m}" y="{y + m}" width="2" height="2" fill="{dot}"/>')


DOUBLE = "M12 2 L16.5 7 H13 V17 H16.5 L12 22 L7.5 17 H11 V7 H7.5 Z"


def build_shape(name, c, frame=0):
    p = Painter(c)
    if name == "default":
        arrow(p)
    elif name == "right_ptr":
        arrow(p, mirror=True)
    elif name == "pointer":
        p.chip(WEDGE)
        # a dark notch along the straight edge: reads as a pressed key
        p.raw(f'<path d="M5.6 6.2 V15.4" stroke="{c["bg"]}" stroke-width="1.1" stroke-opacity="0.55"/>')
    elif name == "text":
        p.chip("M8.5 3 H15.5 V5 H13 V19 H15.5 V21 H8.5 V19 H11 V5 H8.5 Z")
    elif name == "vertical-text":
        p.chip("M8.5 3 H15.5 V5 H13 V19 H15.5 V21 H8.5 V19 H11 V5 H8.5 Z",
               transform="rotate(90 12 12)")
    elif name == "crosshair":
        p.chip("M11 2 H13 V9 H11 Z M11 15 H13 V22 H11 Z M2 11 H9 V13 H2 Z M15 11 H22 V13 H15 Z")
        p.raw(f'<rect x="11" y="11" width="2" height="2" fill="{c["accent2"]}"/>')
    elif name == "cell":
        p.panel("M9 3 H15 V9 H21 V15 H15 V21 H9 V15 H3 V9 H9 Z")
    elif name == "move":
        p.chip("M12 2 L16 6.5 H13 V11 H17.5 V8 L22 12 L17.5 16 V13 H13 V17.5 H16 L12 22 "
               "L8 17.5 H11 V13 H6.5 V16 L2 12 L6.5 8 V11 H11 V6.5 H8 Z")
        p.raw(f'<rect x="10.5" y="10.5" width="3" height="3" fill="{c["bg"]}"/>')
    elif name in ("grab", "grabbing"):
        if name == "grab":
            p.panel("M6 6 H18 V18 H6 Z")
            dot = c["accent2"]
        else:
            p.chip("M7 7 H17 V17 H7 Z")
            dot = c["bg"]
        for x in (9.5, 12.5):
            for y in (8.5, 11, 13.5):
                p.raw(f'<rect x="{x}" y="{y}" width="2" height="2" fill="{dot}"/>')
    elif name == "not-allowed":
        p.raw(f'<circle cx="12" cy="12" r="9.2" fill="{c["bg"]}" fill-opacity="0.75"/>')
        p.raw(f'<circle cx="12" cy="12" r="7" fill="{c["bg"]}" stroke="{c["alert"]}" stroke-width="2.4"/>')
        p.raw(f'<path d="M7 7 L17 17" stroke="{c["alert"]}" stroke-width="2.4"/>')
    elif name == "wait":
        spinner(p, 6, 6, 12, 2.5, frame, c["line"])
    elif name == "progress":
        arrow(p)
        spinner(p, 14.5, 14.5, 6.5, 2, frame, c["line"])
    elif name in ("help", "context-menu", "copy", "alias", "no-drop"):
        arrow(p)
        b = c["bg"]
        if name == "no-drop":
            badge(p, fill=c["alert"])
            p.raw(f'<path d="M15.5 15.5 L19.5 19.5 M19.5 15.5 L15.5 19.5" stroke="{b}" stroke-width="1.6"/>')
        else:
            badge(p)
            if name == "copy":
                p.raw(f'<path d="M14.8 16.75 H20.2 V18.25 H14.8 Z M16.75 14.8 H18.25 V20.2 H16.75 Z" fill="{b}"/>')
            elif name == "alias":
                p.raw(f'<path d="M15.3 19.7 L19.4 15.6 M16.3 15.4 H19.6 V18.7" fill="none" stroke="{b}" stroke-width="1.5"/>')
            elif name == "context-menu":
                p.raw(f'<path d="M15 15 H20 V16.3 H15 Z M15 16.85 H20 V18.15 H15 Z M15 18.7 H20 V20 H15 Z" fill="{b}"/>')
            elif name == "help":
                p.raw(f'<path d="M15.6 16.4 V15.2 H19.4 V17.6 H17.5 V18.6" fill="none" stroke="{b}" stroke-width="1.5"/>'
                      f'<rect x="16.75" y="19.3" width="1.5" height="1.5" fill="{b}"/>')
    elif name in ("zoom-in", "zoom-out"):
        p.raw(f'<path d="M14.3 14.3 L20.5 20.5" stroke="{c["bg"]}" stroke-opacity="0.75" stroke-width="5.2"/>')
        p.raw(f'<path d="M14.3 14.3 L20.5 20.5" stroke="url(#acc)" stroke-width="3"/>')
        p.raw(f'<circle cx="10" cy="10" r="7.6" fill="{c["bg"]}" fill-opacity="0.75"/>')
        p.raw(f'<circle cx="10" cy="10" r="5.6" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2"/>')
        p.raw(f'<rect x="7" y="9.25" width="6" height="1.5" fill="{c["accent2"]}"/>')
        if name == "zoom-in":
            p.raw(f'<rect x="9.25" y="7" width="1.5" height="6" fill="{c["accent2"]}"/>')
    elif name in ("ns-resize", "ew-resize", "nwse-resize", "nesw-resize"):
        rot = {"ns-resize": 0, "ew-resize": 90, "nwse-resize": -45, "nesw-resize": 45}[name]
        p.chip(DOUBLE, transform=f"rotate({rot} 12 12)" if rot else "")
    elif name in ("col-resize", "row-resize"):
        t = "" if name == "col-resize" else "rotate(90 12 12)"
        p.chip("M2 12 L6.5 7.5 V10.8 H9.5 V13.2 H6.5 V16.5 Z M22 12 L17.5 7.5 V10.8 H14.5 V13.2 H17.5 V16.5 Z",
               transform=t)
        p.chip("M11 4 H13 V20 H11 Z", fill=c["accent2"], transform=t)
    else:
        raise KeyError(name)
    return p.svg()


HOTSPOTS = {  # in grid units (0-24)
    "default": (4, 2), "pointer": (4, 2), "progress": (4, 2), "help": (4, 2),
    "context-menu": (4, 2), "copy": (4, 2), "alias": (4, 2), "no-drop": (4, 2),
    "right_ptr": (20, 2), "zoom-in": (10, 10), "zoom-out": (10, 10),
}
ANIMATED = ("wait", "progress")


def frames(name):
    return SPIN_FRAMES if name in ANIMATED else 1


# ---------------------------------------------------------------- build

def render_png(svg_path, size):
    out = subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), svg_path],
                         check=True, capture_output=True).stdout
    return Image.open(BytesIO(out)).convert("RGBA")


def xcursor_bytes(images):
    """images: [(nominal, PIL RGBA, xhot, yhot, delay)] -> Xcursor file bytes."""
    head = struct.pack("<4sIII", b"Xcur", 16, 0x10000, len(images))
    toc, chunks = b"", b""
    pos = 16 + 12 * len(images)
    for nominal, im, xh, yh, delay in images:
        r, g, b, a = im.convert("RGBa").split()  # premultiplied
        pix = Image.merge("RGBA", (b, g, r, a)).tobytes()  # little-endian ARGB
        chunk = struct.pack("<9I", 36, 0xFFFD0002, nominal, 1, im.width, im.height, xh, yh, delay) + pix
        toc += struct.pack("<III", 0xFFFD0002, nominal, pos)
        chunks += chunk
        pos += len(chunk)
    return head + toc + chunks


def build(palette, outdir, hyprcursor=True):
    """Write a complete theme dir (index.theme + cursors/ [+ manifest.hl + hyprcursors/])."""
    c = palette["colors"]
    theme = f'{palette["name"]}-Deck'
    dest = os.path.join(outdir, theme)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(os.path.join(dest, "cursors"))
    src = tempfile.mkdtemp(prefix="deckskin-")
    try:
        hc_src = os.path.join(src, "hc")
        os.makedirs(os.path.join(hc_src, "hyprcursors"))
        jobs = []
        for name in ALIASES:
            d = os.path.join(hc_src, "hyprcursors", name)
            os.makedirs(d)
            for f in range(frames(name)):
                svg = os.path.join(d, f"{name}-{f:02d}.svg")
                with open(svg, "w") as fh:
                    fh.write(build_shape(name, c, f))
                jobs += [(name, f, svg, s) for s in XCURSOR_SIZES]
        with ThreadPoolExecutor(os.cpu_count() or 4) as ex:
            pngs = dict(zip([(n, f, s) for n, f, _, s in jobs],
                            ex.map(lambda j: render_png(j[2], j[3]), jobs)))
        for name, aliases in ALIASES.items():
            hx, hy = HOTSPOTS.get(name, (12, 12))
            n = frames(name)
            imgs = []
            for s in XCURSOR_SIZES:
                for f in range(n):
                    imgs.append((s, pngs[(name, f, s)], round(hx * s / 24), round(hy * s / 24),
                                 SPIN_DELAY if n > 1 else 0))
            with open(os.path.join(dest, "cursors", name), "wb") as fh:
                fh.write(xcursor_bytes(imgs))
            for a in aliases:
                os.symlink(name, os.path.join(dest, "cursors", a))
            # hyprcursor source meta
            lines = ["resize_algorithm = bilinear", f"hotspot_x = {hx / 24:.4f}",
                     f"hotspot_y = {hy / 24:.4f}"]
            lines += [f"define_override = {a}" for a in aliases]
            lines += [f"define_size = 0, {name}-{f:02d}.svg" + (f", {SPIN_DELAY}" if n > 1 else "")
                      for f in range(n)]
            with open(os.path.join(hc_src, "hyprcursors", name, "meta.hl"), "w") as fh:
                fh.write("\n".join(lines) + "\n")
        desc = f'{palette["name"]} deck cursors (deckskin)'
        with open(os.path.join(dest, "index.theme"), "w") as fh:
            fh.write(f"[Icon Theme]\nName={theme}\nComment={desc}\nInherits=Adwaita\n")
        with open(os.path.join(hc_src, "manifest.hl"), "w") as fh:
            fh.write(f"name = {theme}\ndescription = {desc}\nversion = 1\ncursors_directory = hyprcursors\n")
        if hyprcursor and shutil.which("hyprcursor-util"):
            out = os.path.join(src, "out")
            os.makedirs(out)
            r = subprocess.run(["hyprcursor-util", "--create", hc_src, "--output", out],
                               capture_output=True, text=True)
            built = [os.path.join(out, x) for x in os.listdir(out)]
            if r.returncode or not built:
                raise RuntimeError("hyprcursor-util failed:\n" + r.stdout + r.stderr)
            shutil.copy(os.path.join(built[0], "manifest.hl"), dest)
            shutil.copytree(os.path.join(built[0], "hyprcursors"), os.path.join(dest, "hyprcursors"))
        return dest, pngs
    finally:
        shutil.rmtree(src, ignore_errors=True)


def preview(palette, pngs, path, size=48):
    """Contact sheet: every shape on the palette bg and on white, frame 0."""
    from PIL import ImageDraw, ImageFont
    c = palette["colors"]
    names = list(ALIASES)
    cols, cell, pad = 9, size + 28, 18
    rows = -(-len(names) // cols)
    w = pad * 2 + cols * cell
    h = pad * 2 + rows * 2 * cell + 8
    im = Image.new("RGBA", (w, h), c["bg"])
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, w, 3], fill=c["accent"])
    font = None
    try:
        fp = subprocess.run(["fc-match", "-f", "%{file}", palette["font"]["ui"] + ":bold"],
                            capture_output=True, text=True).stdout
        font = ImageFont.truetype(fp, 9)
    except Exception:
        font = ImageFont.load_default()
    light_top = pad + rows * cell + 8
    dr.rectangle([0, light_top - 4, w, h], fill="#f2efe9")
    for i, n in enumerate(names):
        x = pad + (i % cols) * cell
        for top, col in ((pad, c["dim"]), (light_top, "#6b6b6b")):
            y = top + (i // cols) * cell
            im.alpha_composite(pngs[(n, 0, size)], (x + 14, y + 4))
            label = n.upper()[:12]
            tw = dr.textlength(label, font=font)
            dr.text((x + cell / 2 - tw / 2, y + size + 6), label, fill=col, font=font)
    im.save(path)
