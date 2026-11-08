"""Spotify theme: a Spicetify theme (color.ini + user.css) generated from a palette."""
import colorsys
import os
import shutil
import subprocess
import time
from string import Template

# Selectors stick to what survives Spotify updates: Root__* layout classes, data-testid, data-encore-id,
# and the stable names Spicetify's css-map provides. Hashed classes (e-10860-*, Q9sh9k...) change per release.
CSS = Template(r"""/* deckskin: $name deck for Spotify (generated from palettes/$slug.toml; edit that and re-run)
   Square panels, 3px accent bar on top, solid accent chips, hover = panel + 3px accent left edge. */

:root, .encore-dark-theme, .encore-dark-theme .encore-base-set, .encore-layout-themes {
  --deck-bg: $bg; --deck-panel: $panel; --deck-line: $line; --deck-fg: $fg; --deck-sub: $subtext;
  --deck-dim: $dim; --deck-accent: $accent; --deck-accent2: $accent2; --deck-deep: $deep; --deck-on: $on_accent;
  --deck-font: "$font", "Noto Color Emoji", "Noto Sans CJK JP", sans-serif;
  --text-bright-accent: $accent !important;
  --essential-bright-accent: $accent !important;
  --decorative-subdued: $line !important;
}

/* ── everything square, one font ── */
*, *::before, *::after { border-radius: 0 !important; }
body, body * { font-family: var(--deck-font) !important; letter-spacing: 0 !important; }
::selection { background: var(--deck-accent); color: var(--deck-on); }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--deck-line); }
::-webkit-scrollbar-thumb:hover { background: var(--deck-accent); }
.os-scrollbar-handle { background: var(--deck-line) !important; }
.os-scrollbar-handle:hover, .os-scrollbar-handle:active { background: var(--deck-accent) !important; }

/* ── window: panels on bg, each with a 1px line + 3px accent bar on top ── */
body, .Root__top-container { background: var(--deck-bg) !important; }
.Root__nav-bar, .Root__main-view, .Root__right-sidebar, .Root__now-playing-bar {
  position: relative; background: var(--deck-bg) !important; outline: 1px solid var(--deck-line); outline-offset: -1px;
}
.Root__nav-bar::before, .Root__main-view::before, .Root__right-sidebar::before, .Root__now-playing-bar::before {
  content: ""; position: absolute; inset: 0 0 auto 0; height: 3px; background: var(--deck-accent);
  z-index: 50; pointer-events: none;
}
.main-yourLibraryX-library, .main-yourLibraryX-libraryContainer, .main-view-container, .main-view-container__scroll-node,
.main-nowPlayingBar-container, .main-nowPlayingBar-nowPlayingBar, .main-nowPlayingView-container,
.Root__right-sidebar-peek, .Root__right-sidebar-peekContent, .Root__right-sidebar > * {
  background: transparent !important;
}

/* Art-coloured washes off: every page sits on the same flat bg. Spotify tints a page by setting these
   variables inline, and !important in a stylesheet beats inline. */
.Root__main-view [style*="--background-base"], .Root__main-view [style*="--background-tinted-base"] {
  --background-base: $bg !important; --background-highlight: $panel !important; --background-press: $line !important;
  --background-elevated-base: $panel !important; --background-elevated-highlight: $line !important;
  --background-elevated-press: $line !important; --background-tinted-base: $panel !important;
  --background-tinted-highlight: $line !important; --background-tinted-press: $line !important;
}
main > div > [style*="background-color"], [class*="actionBarBackground-background"], .main-entityHeader-backgroundColor,
.main-entityHeader-overlay, .main-view-container__scroll-node-child > [style*="background"] {
  background: none !important;
}
.main-topBar-background { background: var(--deck-bg) !important; box-shadow: inset 0 -1px 0 var(--deck-line); }
.main-topBar-container, .main-home-content { background: transparent !important; }

/* ── top bar ── */
.Root__globalNav { background: var(--deck-bg) !important; }
.main-globalNav-searchInputContainer, .main-globalNav-searchInputWrapper { background: transparent !important; }
.Root__globalNav input[data-encore-id="formInput"], .Root__globalNav form input {
  background: var(--deck-panel) !important; color: var(--deck-fg) !important; box-shadow: inset 0 0 0 1px var(--deck-line) !important;
}
.Root__globalNav input:focus { box-shadow: inset 0 0 0 1px var(--deck-accent) !important; }
.Root__globalNav input::placeholder { color: var(--deck-dim) !important; }
.main-globalNav-link-icon, .main-globalNav-navLink button, .main-globalNav-buddyFeed, .main-actionButtons button {
  background: var(--deck-panel) !important; box-shadow: inset 0 0 0 1px var(--deck-line);
}
.main-globalNav-link-icon:hover, .main-actionButtons button:hover { box-shadow: inset 0 0 0 1px var(--deck-accent); }
.main-globalNav-navLink button:disabled { background: transparent !important; box-shadow: none; }
.main-globalNav-navLinkActive, .main-globalNav-navLinkActive.main-globalNav-link-icon {
  background: var(--deck-accent) !important; color: var(--deck-on) !important; box-shadow: none;
}
.main-globalNav-navLinkActive svg { fill: var(--deck-on) !important; color: var(--deck-on) !important; }

/* ── tags: small bold uppercase ── */
.main-yourLibraryX-header h1, .main-yourLibraryX-header [data-encore-id="text"],
.main-trackList-trackListHeaderRow, .main-trackList-trackListHeaderRow *,
.main-nowPlayingView-sectionHeaderText, [data-testid="component-shelf"] [data-encore-id="listRowTitle"],
[data-testid="component-shelf"] [data-encore-id="listRowTitle"] * , .main-shelf-title, .main-shelf-title * {
  text-transform: uppercase; font-weight: 700 !important;
}
.main-yourLibraryX-header h1, .main-trackList-trackListHeaderRow, .main-trackList-trackListHeaderRow *,
.main-nowPlayingView-sectionHeaderText { font-size: 11px !important; color: var(--deck-dim) !important; }
[data-testid="component-shelf"] [data-encore-id="listRowTitle"], [data-testid="component-shelf"] [data-encore-id="listRowTitle"] *,
.main-shelf-title, .main-shelf-title * { font-size: 13px !important; color: var(--deck-fg) !important; }
.Root__main-view h2[data-encore-id], .Root__main-view h2[data-encore-id] a {
  text-transform: uppercase; font-size: 13px !important; font-weight: 700 !important; color: var(--deck-fg) !important;
}
[data-encore-id="verifiedBadge"] { color: var(--deck-accent) !important; fill: var(--deck-accent) !important; }

/* ── chips: dim outline, selected = solid accent ── */
[data-encore-id="chip"] > span, [data-encore-id="chip"] > a > span {
  background: var(--deck-panel) !important; color: var(--deck-sub) !important; box-shadow: inset 0 0 0 1px var(--deck-line);
  text-transform: uppercase; font-size: 11px !important; font-weight: 700 !important;
}
[data-encore-id="chip"]:hover > span { color: var(--deck-fg) !important; box-shadow: inset 0 0 0 1px var(--deck-accent); }
[data-encore-id="chip"][aria-checked="true"] > span, [data-encore-id="chip"][aria-checked="true"] > a > span {
  background: var(--deck-accent) !important; color: var(--deck-on) !important; box-shadow: none;
}
[data-encore-id="chip"][aria-checked="true"] svg { fill: var(--deck-on) !important; }

/* ── buttons: primary = solid accent chip; secondary = outlined ── */
[data-encore-id="buttonPrimary"] > span, [data-testid="control-button-playpause"], .main-playButton-PlayButton > button > span {
  background: var(--deck-accent) !important; color: var(--deck-on) !important; box-shadow: none !important; transform: none !important;
}
[data-encore-id="buttonPrimary"]:hover > span, [data-testid="control-button-playpause"]:hover {
  background: var(--deck-accent2) !important;
}
[data-encore-id="buttonPrimary"] svg, [data-testid="control-button-playpause"] svg { fill: var(--deck-on) !important; color: var(--deck-on) !important; }
/* A row of text buttons on a page (Add, Mix, Name & details) would out-shout the play chip: outline those. */
.Root__main-view [data-encore-id="buttonPrimary"]:not(.main-actionBar-ActionBarRow *):not(.main-playButton-PlayButton *):not(.main-playButton-PlayButton) > span {
  background: var(--deck-panel) !important; color: var(--deck-fg) !important; box-shadow: inset 0 0 0 1px var(--deck-line) !important;
}
.Root__main-view [data-encore-id="buttonPrimary"]:not(.main-actionBar-ActionBarRow *):not(.main-playButton-PlayButton *):not(.main-playButton-PlayButton):hover > span {
  background: var(--deck-panel) !important; box-shadow: inset 0 0 0 1px var(--deck-accent) !important;
}
.Root__main-view [data-encore-id="buttonPrimary"]:not(.main-actionBar-ActionBarRow *):not(.main-playButton-PlayButton *):not(.main-playButton-PlayButton) svg {
  fill: var(--deck-fg) !important; color: var(--deck-fg) !important;
}
[data-encore-id="buttonSecondary"] {
  background: var(--deck-panel) !important; color: var(--deck-fg) !important; border: 0 !important; box-shadow: inset 0 0 0 1px var(--deck-line) !important;
}
[data-encore-id="buttonSecondary"]:hover { box-shadow: inset 0 0 0 1px var(--deck-accent) !important; transform: none !important; }

/* ── hover = panel + 3px accent left edge ── */
.main-trackList-trackListRow:hover, .main-yourLibraryX-listItem:hover, .main-card-cardContainer:hover,
.view-homeShortcutsGrid-shortcut:hover, [role="menuitem"]:hover, .main-contextMenu-menuItemButton:hover {
  background: var(--deck-panel) !important; box-shadow: inset 3px 0 0 var(--deck-accent) !important;
}
.main-trackList-selected, .main-trackList-selected:hover { background: var(--deck-line) !important; box-shadow: inset 3px 0 0 var(--deck-accent) !important; }
.main-trackList-active { box-shadow: inset 3px 0 0 var(--deck-accent); }
.main-trackList-active .main-trackList-rowTitle, .main-trackList-active .main-trackList-rowTitle * { color: var(--deck-accent) !important; }
img[src*="equaliser"] { filter: $eq; }
.main-trackList-rowMainContent [style*="color: rgb"] { color: var(--deck-accent2) !important; }

/* The mono font runs wider than Spotify's, so rows step down a size to keep titles readable */
.main-trackList-rowTitle, .main-trackList-rowTitle *, .Root__nav-bar [data-encore-id="listRowTitle"], .Root__nav-bar [data-encore-id="listRowTitle"] * { font-size: 14px !important; }
.main-trackList-rowSubTitle, .main-trackList-rowSubTitle *, .main-trackList-rowSectionVariable, .main-trackList-rowSectionVariable *,
.main-trackList-rowSectionEnd, .main-trackList-rowDuration, .Root__nav-bar [data-encore-id="listRowSubtitle"], .Root__nav-bar [data-encore-id="listRowSubtitle"] * { font-size: 12px !important; }

/* ── cards ── */
.main-card-cardContainer { background: transparent !important; }
.main-card-cardContainer::before, .main-card-cardContainer::after { background: none !important; box-shadow: none !important; }
.view-homeShortcutsGrid-shortcut { background: var(--deck-panel) !important; box-shadow: inset 0 0 0 1px var(--deck-line); }
.view-homeShortcutsGrid-main, .view-homeShortcutsGrid-content { background: transparent !important; }
.main-cardImage-imageWrapper, .main-card-imageContainer { box-shadow: none !important; background: var(--deck-panel) !important; }

/* ── library sidebar ── */
.main-yourLibraryX-header, .main-yourLibraryX-filterArea, .main-yourLibraryX-rootListHeader { background: transparent !important; box-shadow: none !important; }
.x-filterBox-filterInput { background: var(--deck-panel) !important; }
.Root__nav-bar [class*="box--interactive"]:hover { background: var(--deck-panel) !important; box-shadow: inset 3px 0 0 var(--deck-accent) !important; }
.Root__nav-bar [class*="box--tinted"] { background: var(--deck-panel) !important; box-shadow: inset 3px 0 0 var(--deck-accent) !important; }

/* ── entity pages: title in the deck's weight, not a poster ── */
.main-entityHeader-title h1, .main-entityHeader-title [data-encore-id="text"] {
  font-size: clamp(26px, 4vw, 44px) !important; line-height: 1.1 !important; font-weight: 800 !important;
}
.main-entityHeader-image, .main-entityHeader-imagePlaceholder { box-shadow: none !important; outline: 1px solid var(--deck-line); }
.main-entityHeader-metaData *, .main-entityHeader-subtitle { color: var(--deck-sub) !important; }
/* Hero photos fade into the page, so the title stays readable on a bright image */
[data-testid="background-image"] + * {
  background-image: linear-gradient(to bottom, color-mix(in srgb, var(--deck-bg) 10%, transparent),
    color-mix(in srgb, var(--deck-bg) 70%, transparent) 60%, var(--deck-bg)) !important;
}
.main-entityHeader-headerText { text-shadow: 0 1px 10px color-mix(in srgb, var(--deck-bg) 80%, transparent); }

/* ── player ── */
.main-nowPlayingBar-container { padding-top: 3px; }
.cover-art { box-shadow: none !important; }
.x-progressBar-progressBarBg { background: var(--deck-line) !important; height: 4px !important; }
.x-progressBar-sliderArea { height: 4px !important; }
.x-progressBar-fillColor { background: linear-gradient(90deg, var(--deck-accent), var(--deck-deep)) !important; }
[data-testid="progress-bar-handle"] {
  background: var(--deck-fg) !important; box-shadow: none !important; width: 5px !important; height: 12px !important; margin-top: -2px;
}
.main-trackInfo-name a, .main-trackInfo-name { color: var(--deck-fg) !important; }
.main-trackInfo-artists a { color: var(--deck-sub) !important; }

/* ── right sidebar ── */
.Root__right-sidebar h2[data-encore-id], .Root__right-sidebar h2 {
  text-transform: uppercase; font-size: 11px !important; font-weight: 700 !important; color: var(--deck-dim) !important;
}
.main-nowPlayingView-section { background: var(--deck-panel) !important; box-shadow: inset 0 0 0 1px var(--deck-line); }

/* ── menus + tooltips: bg, 1px line, 3px accent bar ── */
#context-menu, .main-contextMenu-menu, [role="menu"], [data-placement] > [role="menu"], .main-contextMenu-tippy {
  background: var(--deck-bg) !important; color: var(--deck-fg) !important; box-shadow: 0 8px 24px rgba(0,0,0,.6) !important;
  border: 1px solid var(--deck-line); border-top: 3px solid var(--deck-accent);
}
.main-contextMenu-menuItem, [role="menu"] li { background: transparent !important; }
.main-contextMenu-menuItemButton { background: transparent; }
[data-encore-id="tooltip"], .hover-or-focus [role="tooltip"], [role="tooltip"] {
  background: var(--deck-panel) !important; color: var(--deck-fg) !important; box-shadow: inset 0 0 0 1px var(--deck-line) !important;
}

/* ── lyrics: Spotify sets these per track, inline ── */
[style*="--lyrics-color-background"] {
  --lyrics-color-background: $bg !important; --lyrics-color-active: $accent !important;
  --lyrics-color-inactive: $subtext !important; --lyrics-color-passed: $dim !important;
  --lyrics-color-messaging: $subtext !important;
}

/* ── browse tiles: keep the art, lose the loud per-genre colour ── */
.Root__main-view a > div[style*="background-color"] {
  background-color: var(--deck-panel) !important; box-shadow: inset 0 0 0 1px var(--deck-line);
}
.Root__main-view a:hover > div[style*="background-color"] { box-shadow: inset 3px 0 0 var(--deck-accent), inset 0 0 0 1px var(--deck-line); }

/* ── settings + dialogs ── */
.x-toggle-indicatorWrapper, .x-toggle-indicator { transition: none !important; }
[role="dialog"], .GenericModal > * { background-color: var(--deck-bg) !important; outline: 1px solid var(--deck-line); border-top: 3px solid var(--deck-accent); }
""")


def render_colors(pal, slug):
    c = pal["colors"]
    table = {
        "text": c["fg"], "subtext": c["subtext"], "main": c["bg"], "main-elevated": c["panel"],
        "highlight": c["line"], "highlight-elevated": c["line"], "sidebar": c["bg"], "player": c["bg"],
        "card": c["panel"], "shadow": "#000000", "selected-row": c["fg"], "button": c["accent"],
        "button-active": c["accent2"], "button-disabled": c["dim"], "tab-active": c["line"],
        "notification": c["accent"], "notification-error": c["alert"], "misc": c["dim"],
    }
    return f"[{slug}]\n" + "".join(f"{k:<19}= {v.lstrip('#')}\n" for k, v in table.items())


def equaliser_filter(pal):
    """The 'now playing' bars are a green GIF, so rotate its hue onto the accent."""
    hexa = pal["colors"]["accent"].lstrip("#")
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hue = colorsys.rgb_to_hsv(r, g, b)[0] * 360
    return f"hue-rotate({round(hue - 141)}deg) saturate(1.2)"


def render_css(pal, slug):
    return CSS.substitute(
        name=pal["name"], slug=slug, font=pal["font"]["ui"], eq=equaliser_filter(pal), **pal["colors"]
    )


def theme_name(pal):
    return f"{pal['name']}-Deck"


# ---------------------------------------------------------------- install

SPOTIFY_DIRS = (
    "/opt/spotify",
    "/usr/share/spotify",
    "/usr/libexec/spotify",
    os.path.expanduser("~/.local/share/spotify-launcher/install/usr/share/spotify"),
    os.path.expanduser("~/.local/share/flatpak/app/com.spotify.Client/current/active/files/extra/share/spotify"),
    "/var/lib/flatpak/app/com.spotify.Client/current/active/files/extra/share/spotify",
)
DEBUG_FLAGS = ("--remote-debugging-port", "--remote-allow-origins")
UNIT = "deckskin-spotify"


def spicetify_bin():
    found = shutil.which("spicetify")
    if found:
        return found
    home = os.path.expanduser("~/.spicetify/spicetify")
    return home if os.access(home, os.X_OK) else None


def spotify_dir():
    for path in SPOTIFY_DIRS:
        if os.path.isdir(os.path.join(path, "Apps")):
            return path
    return None


def spicetify(binary, *args):
    """Run spicetify without letting it restart Spotify. Raises with its own output on failure."""
    r = subprocess.run([binary, "-n", *args], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode != 0 or "error" in r.stdout.lower():
        tail = (r.stdout + r.stderr).replace("\r", "\n").splitlines()[-6:]
        raise RuntimeError(f"spicetify {' '.join(args)} failed:\n" + "\n".join(tail))
    return r.stdout


def config_dir(binary):
    """spicetify -c prints the config file path, and creates the file on first run."""
    r = subprocess.run([binary, "-c"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return os.path.dirname(r.stdout.strip().splitlines()[-1])


def write_theme(pal, slug, cfg):
    dest = os.path.join(cfg, "Themes", theme_name(pal))
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "color.ini"), "w") as fh:
        fh.write(render_colors(pal, slug))
    with open(os.path.join(dest, "user.css"), "w") as fh:
        fh.write(render_css(pal, slug))
    return dest


def is_unpatched(spotify):
    """Spicetify replaces Apps/xpui.spa with an extracted Apps/xpui, so a .spa means Spotify was (re)installed."""
    return os.path.exists(os.path.join(spotify, "Apps", "xpui.spa"))


def apply(binary, spotify):
    """Patch Spotify. After an update the old backup and extracted folders are stale, so rebuild them first."""
    apps = os.path.join(spotify, "Apps")
    if not os.access(apps, os.W_OK):
        raise RuntimeError(f"{apps} isn't writable. Spicetify patches it in place, so run once:\n"
                           f"  sudo chown -R $USER {spotify}")
    if is_unpatched(spotify):
        for stale in ("xpui", "login"):
            shutil.rmtree(os.path.join(apps, stale), ignore_errors=True)
        spicetify(binary, "clear")
        spicetify(binary, "backup")
    spicetify(binary, "apply")
    if is_unpatched(spotify) or not os.path.exists(os.path.join(apps, "xpui", "user.css")):
        raise RuntimeError("spicetify finished but the theme isn't in Spotify's files")


def write_units(command, spotify):
    """A user path unit: Spotify's xpui.spa only exists after an update removed the theme."""
    units = os.path.expanduser("~/.config/systemd/user")
    os.makedirs(units, exist_ok=True)
    with open(os.path.join(units, f"{UNIT}.path"), "w") as fh:
        fh.write(f"""[Unit]
Description=deckskin: watch for a Spotify update

[Path]
PathExists={spotify}/Apps/xpui.spa
Unit={UNIT}.service

[Install]
WantedBy=default.target
""")
    # The pause lets the package manager finish writing files. The limit stops a failing patch from looping.
    with open(os.path.join(units, f"{UNIT}.service"), "w") as fh:
        fh.write(f"""[Unit]
Description=deckskin: restore the Spotify theme after an update
StartLimitIntervalSec=3600
StartLimitBurst=3

[Service]
Type=oneshot
ExecStartPre=/usr/bin/sleep 20
ExecStart="{command}" spotify-reapply
""")


def main_pid():
    """The oldest process named spotify is the browser process; its children are helpers."""
    r = subprocess.run(["pgrep", "-o", "-x", "spotify"], capture_output=True, text=True)
    return int(r.stdout) if r.returncode == 0 and r.stdout.strip() else None


def launch_args(pid):
    """Reuse the running command line, so restarts keep flags like --ozone-platform=wayland."""
    with open(f"/proc/{pid}/cmdline", "rb") as fh:
        args = [a.decode() for a in fh.read().split(b"\0") if a]
    return [a for a in args if not a.startswith(DEBUG_FLAGS)]


def stop(timeout=20):
    """TERM every spotify process: the main one ignores it until its helpers are gone. Playback state survives."""
    subprocess.run(["pkill", "-x", "spotify"], capture_output=True)
    for _ in range(timeout * 5):
        if main_pid() is None:
            return True
        time.sleep(0.2)
    return False
