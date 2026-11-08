"""Firefox theme: userChrome.css + userContent.css + prefs, generated from a palette."""
import configparser
import glob
import json
import os
import re
import shutil
import time
from string import Template

CHROME = Template(r"""/* deckskin: $name deck for Firefox (generated from palettes/$slug.toml; edit that and re-run)
   Square panels, 3px accent bar on top, solid accent chips, hover = panel + 3px accent left edge. */

:root {
  --deck-bg: $bg; --deck-panel: $panel; --deck-line: $line; --deck-fg: $fg;
  --deck-sub: $subtext; --deck-dim: $dim; --deck-accent: $accent; --deck-accent2: $accent2;
  --deck-deep: $deep; --deck-on-accent: $on_accent;
  --deck-font: "$font", monospace;

  /* everything square */
  --border-radius-small: 0px !important; --border-radius-medium: 0px !important;
  --border-radius-large: 0px !important; --tab-border-radius: 0px !important;
  --toolbarbutton-border-radius: 0px !important; --arrowpanel-border-radius: 0px !important;
  --panel-border-radius: 0px !important; --menuitem-border-radius: 0px !important;
  --urlbar-icon-border-radius: 0px !important; --toolbarbutton-outer-padding: 2px !important;
  --button-border-radius: 0px !important; --popup-border-radius: 0px !important;
  --urlbar-border-radius: 0px !important; --urlbarview-border-radius: 0px !important;
  --urlbar-inner-border-radius: 0px !important; --urlbar-background-border-radius: 0px !important;

  /* toolbox + tabs */
  --toolbox-bgcolor: var(--deck-bg) !important; --toolbox-bgcolor-inactive: var(--deck-bg) !important;
  --toolbox-textcolor: var(--deck-fg) !important; --toolbox-textcolor-inactive: var(--deck-sub) !important;
  --lwt-accent-color: var(--deck-bg) !important; --lwt-accent-color-inactive: var(--deck-bg) !important;
  --lwt-text-color: var(--deck-fg) !important; --lwt-header-image: none !important;
  --lwt-additional-images: none !important;
  --toolbar-bgcolor: var(--deck-panel) !important; --toolbar-color: var(--deck-fg) !important;
  --tab-selected-bgcolor: var(--deck-panel) !important; --tab-selected-textcolor: var(--deck-fg) !important;
  --tab-hover-background-color: var(--deck-panel) !important;
  --tab-selected-shadow: none !important; --tab-selected-outline-color: transparent !important;
  --tab-outline-color: transparent !important; --tab-loading-fill: var(--deck-accent) !important;
  --tab-attention-icon-color: var(--deck-accent2) !important;
  --toolbarbutton-hover-background: var(--deck-line) !important;
  --toolbarbutton-active-background: var(--deck-accent) !important;
  --toolbarbutton-icon-fill-attention: var(--deck-accent) !important;
  --toolbarseparator-color: var(--deck-line) !important;
  --chrome-content-separator-color: var(--deck-line) !important;
  --focus-outline-color: var(--deck-accent) !important;
  --color-accent-primary: var(--deck-accent) !important;
  --color-accent-primary-hover: var(--deck-accent2) !important;
  --color-accent-primary-active: var(--deck-deep) !important;
  --button-text-color-primary: var(--deck-on-accent) !important;

  /* panels + menus: bg with a 1px line border */
  --arrowpanel-background: var(--deck-bg) !important; --arrowpanel-color: var(--deck-fg) !important;
  --arrowpanel-border-color: var(--deck-line) !important;
  --arrowpanel-dimmed: var(--deck-panel) !important; --arrowpanel-dimmed-further: var(--deck-line) !important;
  --panel-background: var(--deck-bg) !important; --panel-color: var(--deck-fg) !important;
  --panel-border-color: var(--deck-line) !important; --panel-separator-color: var(--deck-line) !important;
  --panel-item-hover-bgcolor: var(--deck-panel) !important; --panel-item-active-bgcolor: var(--deck-line) !important;
  --menu-background-color: var(--deck-bg) !important; --menu-color: var(--deck-fg) !important;
  --menu-border-color: var(--deck-line) !important;
  --menuitem-hover-background-color: var(--deck-panel) !important;
  --menu-disabled-color: var(--deck-dim) !important;

  /* URL bar */
  --toolbar-field-background-color: var(--deck-bg) !important;
  --toolbar-field-focus-background-color: var(--deck-bg) !important;
  --toolbar-field-color: var(--deck-fg) !important; --toolbar-field-focus-color: var(--deck-fg) !important;
  --toolbar-field-border-color: var(--deck-line) !important;
  --toolbar-field-focus-border-color: var(--deck-accent) !important;
  --urlbar-box-bgcolor: var(--deck-panel) !important; --urlbar-box-focus-bgcolor: var(--deck-panel) !important;
  --urlbar-box-hover-bgcolor: var(--deck-line) !important; --urlbar-box-active-bgcolor: var(--deck-line) !important;
  --urlbarView-background: var(--deck-bg) !important;
  --urlbarView-highlight-background: var(--deck-accent) !important;
  --urlbarView-highlight-color: var(--deck-on-accent) !important;
  --urlbarView-hover-background: var(--deck-panel) !important;
  --urlbarView-separator-color: var(--deck-line) !important;
  --urlbarView-action-color: var(--deck-accent2) !important;
  --urlbarView-url-color: var(--deck-accent2) !important;
  --urlbarview-background-color-selected: var(--deck-accent) !important;
  --urlbarview-text-color-selected: var(--deck-on-accent) !important;
  --urlbarview-result-button-selected-color: var(--deck-on-accent) !important;

  /* sidebar */
  --sidebar-background-color: var(--deck-bg) !important; --sidebar-text-color: var(--deck-fg) !important;
  --sidebar-border-color: var(--deck-line) !important;
}

/* ── toolbox: tab strip on bg, nav + bookmarks bars on panel (selected tab joins them) ── */
#navigator-toolbox, #titlebar, #TabsToolbar, #toolbar-menubar {
  background: var(--deck-bg) !important; background-image: none !important;
  color: var(--deck-fg) !important; border: none !important; box-shadow: none !important;
}
#navigator-toolbox { border-bottom: 1px solid var(--deck-line) !important; }
#nav-bar, #PersonalToolbar {
  background: var(--deck-panel) !important; background-image: none !important;
  border: none !important; box-shadow: none !important;
}
#nav-bar { border-top: none !important; }
/* window buttons: the compositor handles windows */
.titlebar-buttonbox-container, .titlebar-spacer[type="post-tabs"] { display: none !important; }

/* ── tabs ── */
.tabbrowser-tab { font-family: var(--deck-font) !important; font-size: 11.5px !important; }
.tabbrowser-tab:not([pinned]) { padding-inline: 1px !important; }
.tab-background {
  border-radius: 0 !important; margin-block: 4px 0 !important;
  background: transparent !important; box-shadow: none !important; outline: none !important;
}
.tabbrowser-tab:not([selected], [multiselected]):hover .tab-background {
  background: color-mix(in srgb, var(--deck-panel) 65%, transparent) !important;
  box-shadow: inset 0 2px 0 var(--deck-line) !important;
}
.tabbrowser-tab[selected] .tab-background {
  background: var(--deck-panel) !important;
  box-shadow: inset 0 3px 0 var(--deck-accent) !important;
}
.tabbrowser-tab[multiselected]:not([selected]) .tab-background {
  background: var(--deck-panel) !important;
  box-shadow: inset 0 3px 0 var(--deck-accent2) !important;
}
.tabbrowser-tab .tab-label { color: var(--deck-dim) !important; }
.tabbrowser-tab:hover .tab-label { color: var(--deck-sub) !important; }
.tabbrowser-tab[selected] .tab-label { color: var(--deck-fg) !important; font-weight: 700 !important; }
.tab-close-button { border-radius: 0 !important; }
.tab-close-button:hover { background: var(--deck-line) !important; }
.tab-icon-overlay, .tab-sharing-icon-overlay { border-radius: 0 !important; }
.tab-group-label, .tab-group-label-container { border-radius: 0 !important; font-family: var(--deck-font) !important; }
#tabbrowser-tabs { --tab-min-height: 30px !important; border-inline-start: none !important; }
#tabbrowser-tabs[haspinnedtabs]:not([positionpinnedtabs]) > #tabbrowser-arrowscrollbox > .tabbrowser-tab:nth-child(1 of :not([pinned], [hidden])) {
  margin-inline-start: 0 !important;
}

/* ── toolbar buttons: square; pressed/open = solid chip ── */
.toolbarbutton-1 > .toolbarbutton-icon, .toolbarbutton-1 > .toolbarbutton-badge-stack,
.toolbarbutton-1 > .toolbarbutton-text, #PersonalToolbar .toolbarbutton-1 { border-radius: 0 !important; }
.toolbarbutton-1:is([open], [checked], :hover:active) > :is(.toolbarbutton-icon, .toolbarbutton-badge-stack) {
  background: var(--deck-accent) !important; fill: var(--deck-on-accent) !important;
  color: var(--deck-on-accent) !important;
}
.toolbarbutton-badge { border-radius: 0 !important; background: var(--deck-accent2) !important;
  color: var(--deck-on-accent) !important; box-shadow: none !important; }

/* ── URL bar ── */
#urlbar, moz-urlbar, .urlbar, #searchbar {
  --toolbar-field-background-color: var(--deck-bg) !important;
  --toolbar-field-focus-background-color: var(--deck-bg) !important;
  --toolbar-field-color: var(--deck-fg) !important; --toolbar-field-focus-color: var(--deck-fg) !important;
  --toolbar-field-border-color: var(--deck-line) !important;
  --toolbar-field-focus-border-color: var(--deck-accent) !important;
  --urlbar-box-bgcolor: var(--deck-panel) !important; --urlbar-box-focus-bgcolor: var(--deck-panel) !important;
  --urlbar-box-hover-bgcolor: var(--deck-line) !important; --urlbar-box-active-bgcolor: var(--deck-line) !important;
  --urlbarView-background: var(--deck-bg) !important;
  --urlbarView-highlight-background: var(--deck-accent) !important;
  --urlbarView-highlight-color: var(--deck-on-accent) !important;
  --arrowpanel-background: var(--deck-bg) !important; --arrowpanel-color: var(--deck-fg) !important;
  --toolbarbutton-border-radius: 0px !important;
  --urlbar-border-radius: 0px !important; --urlbarview-border-radius: 0px !important;
  --urlbar-inner-border-radius: 0px !important; --urlbar-background-border-radius: 0px !important;
  --urlbarview-background-color-selected: var(--deck-accent) !important;
  --urlbarview-text-color-selected: var(--deck-on-accent) !important;
  --urlbar-input-container-outline-open-focused: 1px solid var(--deck-accent) !important;
}
#urlbar *, .urlbar *, #searchbar * { border-radius: 0 !important; }
#urlbar-background, .urlbar-background {
  background: var(--deck-bg) !important; border: 1px solid var(--deck-line) !important;
  border-radius: 0 !important; box-shadow: none !important; outline: none !important;
}
#urlbar:is([focused], [open], [breakout-extend]) :is(#urlbar-background, .urlbar-background),
#searchbar:focus-within {
  border-color: var(--deck-accent) !important;
  box-shadow: inset 0 3px 0 var(--deck-accent), 0 8px 24px rgba(0, 0, 0, 0.45) !important;
}
#urlbar .urlbar-input-container, #urlbar .urlbar-input-box, #urlbar-input, .urlbar-input {
  background: transparent !important; color: var(--deck-fg) !important;
}
#urlbar-input, .urlbar-input, #searchbar input {
  font-family: var(--deck-font) !important; font-size: 12.5px !important;
}
#urlbar-searchmode-switcher, #identity-box > box, #identity-icon-box, #tracking-protection-icon-container,
.urlbar-page-action, #urlbar-zoom-button, #star-button-box, .searchmode-switcher, #urlbar-label-box,
#urlbar .urlbar-go-button, #urlbar-go-button {
  border-radius: 0 !important;
}
#urlbar-searchmode-switcher, .searchmode-switcher { background: var(--deck-panel) !important; }
#urlbar-search-mode-indicator, .urlbar-search-mode-indicator {
  border-radius: 0 !important; background: var(--deck-accent) !important; color: var(--deck-on-accent) !important;
  outline: none !important;
}
#urlbar-zoom-button { background: var(--deck-accent2) !important; color: var(--deck-on-accent) !important; }

/* results dropdown */
.urlbarView, .urlbarView[popover], .urlbarView:popover-open,
.urlbarView-body-outer, .urlbarView-body-inner, .search-one-offs {
  background: var(--deck-bg) !important; color: var(--deck-fg) !important; border-radius: 0 !important;
}
.urlbarView-body-inner { border-top-color: var(--deck-line) !important; }
.urlbarView-row, .urlbarView-row-inner, .urlbarView-favicon, .urlbarView-button,
.urlbarView-dynamic-results, .urlbarView-row[type="tip"], .search-one-offs .searchbar-engine-one-off-item {
  border-radius: 0 !important;
}
.urlbarView-row:not([selected]):hover > .urlbarView-row-inner {
  background: var(--deck-panel) !important; box-shadow: inset 3px 0 0 var(--deck-accent) !important;
}
.urlbarView-row[selected] > .urlbarView-row-inner, .urlbarView-row-inner[selected] {
  background: var(--deck-accent) !important; color: var(--deck-on-accent) !important;
}
.urlbarView-row[selected] :is(.urlbarView-url, .urlbarView-action, .urlbarView-title-separator,
  .urlbarView-title, .urlbarView-tags) { color: var(--deck-on-accent) !important; }
.urlbarView-row[selected] .urlbarView-favicon { fill: var(--deck-on-accent) !important; }
.urlbarView-url, .urlbarView-action { font-family: var(--deck-font) !important; font-size: 11px !important; }
.urlbarView-title-separator { color: var(--deck-dim) !important; }
.urlbarView-row[label]::before { color: var(--deck-dim) !important; opacity: 1 !important;
  text-transform: uppercase !important; font-family: var(--deck-font) !important; font-weight: 700 !important; }
.urlbarView-group-aboveSuggestion { color: var(--deck-dim) !important; text-transform: uppercase !important;
  font-family: var(--deck-font) !important; font-size: 10px !important; font-weight: 700 !important; }

/* ── bookmarks bar ── */
#PersonalToolbar { padding-block: 1px 3px !important; }
#PersonalToolbar .bookmark-item {
  border-radius: 0 !important; color: var(--deck-sub) !important; margin-inline: 0 2px !important;
  font-family: var(--deck-font) !important; font-size: 11px !important;
}
#PersonalToolbar .bookmark-item:hover {
  background: var(--deck-bg) !important; color: var(--deck-fg) !important;
  box-shadow: inset 3px 0 0 var(--deck-accent) !important;
}
#PersonalToolbar .bookmark-item[open] { background: var(--deck-accent) !important; color: var(--deck-on-accent) !important; }

/* ── menus + panels: square, 3px accent bar on top, hover = panel + accent left edge ── */
menupopup, panel {
  --panel-border-radius: 0px !important; --panel-text-color: var(--deck-fg) !important;
  --panel-border-color: var(--deck-line) !important; --background-color-canvas: var(--deck-bg) !important;
}
menupopup, panel[type="arrow"] {
  --panel-background-color: linear-gradient(var(--deck-accent), var(--deck-accent)) top / 100% 3px no-repeat,
    var(--deck-bg) !important;
  --panel-padding-block: 6px !important;
}
menupopup menu, menupopup menuitem, panel .subviewbutton, .panel-header, menulist { font-family: var(--deck-font) !important; }
menupopup menu, menupopup menuitem { font-size: 12px !important; }
menupopup > :is(menu, menuitem)[_moz-menuactive]:not([disabled="true"]) {
  background: var(--deck-panel) !important; color: var(--deck-fg) !important;
  box-shadow: inset 3px 0 0 var(--deck-accent) !important;
}
menupopup > :is(menu, menuitem) { border-radius: 0 !important; }
menupopup > :is(menu, menuitem)[disabled="true"] { color: var(--deck-dim) !important; }
menuseparator::before { border-color: var(--deck-line) !important; }
.subviewbutton, .panel-subview-footer-button, .toolbaritem-combined-buttons > .subviewbutton {
  border-radius: 0 !important;
}
.subviewbutton:not([disabled="true"]):is(:hover, [open]),
.panel-subview-footer-button:not([disabled="true"]):hover {
  background: var(--deck-panel) !important; box-shadow: inset 3px 0 0 var(--deck-accent) !important;
}
.panel-header > h1, .panel-header { font-weight: 700 !important; }
#appMenu-fxa-label2, .unified-extensions-item-action-button, #unified-extensions-panel .unified-extensions-item,
#appMenu-popup .toolbaritem-combined-buttons > toolbarbutton { border-radius: 0 !important; }
button.footer-button, .panel-footer > button, moz-button, button { border-radius: 0 !important; }
button.footer-button[default], .panel-footer > button[default], .button-primary {
  background: var(--deck-accent) !important; color: var(--deck-on-accent) !important;
}

/* tooltips + link status */
tooltip {
  appearance: none !important; background: var(--deck-panel) !important; color: var(--deck-fg) !important;
  border: 1px solid var(--deck-line) !important; border-radius: 0 !important;
  font-family: var(--deck-font) !important; font-size: 11px !important;
}
#statuspanel-label {
  background: var(--deck-panel) !important; color: var(--deck-fg) !important;
  border: 1px solid var(--deck-line) !important; border-inline-start: 3px solid var(--deck-accent) !important;
  border-radius: 0 !important; font-family: var(--deck-font) !important; font-size: 11px !important;
}

/* find bar */
findbar {
  background: var(--deck-panel) !important; color: var(--deck-fg) !important;
  border-top: 1px solid var(--deck-line) !important; font-family: var(--deck-font) !important;
}
.findbar-textbox {
  background: var(--deck-bg) !important; color: var(--deck-fg) !important;
  border: 1px solid var(--deck-line) !important; border-radius: 0 !important; outline: none !important;
}
.findbar-textbox:focus { border-color: var(--deck-accent) !important; }
.findbar-textbox[status="notfound"] { border-color: var(--deck-deep) !important; }
.findbar-container > checkbox, .findbar-find-previous, .findbar-find-next { border-radius: 0 !important; }

/* sidebar */
#sidebar-main, #sidebar-box, #sidebar-header, #sidebar-launcher-splitter, sidebar-main {
  background: var(--deck-bg) !important; color: var(--deck-fg) !important;
  border-color: var(--deck-line) !important;
}
#sidebar-splitter { border-color: var(--deck-line) !important; background: var(--deck-line) !important; width: 1px !important; }

/* no white flash while a page loads */
#tabbrowser-tabpanels, #browser, .browserStack, browser[type="content"] { background-color: var(--deck-bg) !important; }

/* notification bars + dialogs */
notification-message, .notificationbox-stack notification-message {
  border-radius: 0 !important; --message-bar-background-color: var(--deck-panel) !important;
  --message-bar-text-color: var(--deck-fg) !important; border-inline-start: 3px solid var(--deck-accent) !important;
}
""")

CONTENT = Template(r"""/* deckskin: $name deck for Firefox pages (generated; edit palettes/$slug.toml and re-run) */

/* in-content pages (settings, add-ons, about:*): design tokens only, no forced backgrounds */
@-moz-document url-prefix("about:") {
  :root {
    --background-color-canvas: $bg !important; --background-color-box: $panel !important;
    --text-color: $fg !important; --text-color-deemphasized: $subtext !important;
    --border-color: $line !important; --border-color-deemphasized: $line !important;
    --border-color-card: $line !important; --border-color-interactive: $dim !important;
    --color-accent-primary: $accent !important; --color-accent-primary-hover: $accent2 !important;
    --color-accent-primary-active: $deep !important; --button-text-color-primary: $on_accent !important;
    --focus-outline-color: $accent !important; --link-color: $accent2 !important;
    --link-color-hover: $accent !important;
    --in-content-page-background: $bg !important; --in-content-box-background: $panel !important;
    --in-content-text-color: $fg !important; --in-content-accent-color: $accent !important;
    --in-content-primary-button-background: $accent !important;
    --in-content-primary-button-text-color: $on_accent !important;
    --border-radius-small: 0px !important; --border-radius-medium: 0px !important;
    --border-radius-large: 0px !important;
  }
}

/* new tab / home */
@-moz-document url("about:newtab"), url("about:home"), url("about:privatebrowsing") {
  :root {
    --newtab-background-color: $bg !important; --newtab-background-color-secondary: $panel !important;
    --newtab-text-primary-color: $fg !important; --newtab-text-secondary-color: $subtext !important;
    --newtab-element-hover-color: $panel !important; --newtab-element-active-color: $line !important;
    --newtab-element-secondary-color: $panel !important;
    --newtab-border-color: $line !important; --newtab-wordmark-color: $fg !important;
    --newtab-primary-action-background: $accent !important;
    --newtab-primary-element-text-color: $on_accent !important;
    --newtab-button-background: $panel !important; --newtab-button-text: $fg !important;
    --newtab-search-icon-color: $accent !important;
  }
  body { background-color: $bg !important; }
  body, input, button { font-family: "$font", monospace !important; }
  .search-handoff-button, .search-inner-wrapper input, #newtab-search-text, .fake-textbox,
  .search-wrapper input {
    border-radius: 0 !important; background-color: $panel !important; color: $fg !important;
    border: 1px solid $line !important; box-shadow: none !important; outline: none !important;
  }
  .search-handoff-button:is(:hover, .focused, :focus), .search-wrapper.fake-focus .search-handoff-button,
  .search-inner-wrapper input:focus {
    border-color: $accent !important; box-shadow: inset 0 3px 0 $accent !important;
  }
  .top-site-outer, .top-site-outer .tile, .top-site-outer .top-site-icon, .top-site-outer .icon-wrapper,
  .top-site-button, .context-menu, .context-menu-item button, .ds-card, .card-outer, .card,
  .customize-menu, .personalize-button, .discovery-stream .ds-section, .ds-highlights .card-outer,
  .wallpaper-input, .moz-toggle, .top-sites-list .top-site-outer .context-menu-button,
  .top-site-outer .default-icon {
    border-radius: 0 !important;
  }
  .top-site-outer .tile { background: $panel !important; box-shadow: none !important; border: 1px solid $line !important; }
  .top-site-outer:is(:hover, :focus-within) .tile { box-shadow: inset 0 3px 0 $accent !important; border-color: $line !important; }
  .top-site-outer:is(:hover, :focus-within) { background: transparent !important; }
  .top-site-outer .title { color: $subtext !important; font-size: 11px !important; }
  .top-site-outer .title.pinned .icon { fill: $accent2 !important; }
  .context-menu { background: $bg !important; border: 1px solid $line !important; border-top: 3px solid $accent !important; }
  .context-menu-item button:hover { background: $panel !important; box-shadow: inset 3px 0 0 $accent !important; }
}

/* reader view */
@-moz-document url-prefix("about:reader") {
  :root.dark, body.dark { --main-background: $bg !important; --main-foreground: $fg !important;
    --link-foreground: $accent2 !important; --toolbar-bgcolor: $panel !important; }
}
""")

PREFS_MARK = ("// >>> deckskin (managed block: deckskin rewrites this)", "// <<< deckskin")
BASE_THEME = "firefox-compact-dark@mozilla.org"


def context(palette, slug):
    c = dict(palette["colors"])
    c.update(name=palette["name"], slug=slug, font=palette["font"]["ui"])
    return c


def render(palette, slug):
    ctx = context(palette, slug)
    return CHROME.substitute(ctx), CONTENT.substitute(ctx)


def prefs_block(palette):
    c = palette["colors"]
    lines = [
        PREFS_MARK[0],
        'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);',
        f'user_pref("extensions.activeThemeID", "{BASE_THEME}");',
        'user_pref("ui.systemUsesDarkTheme", 1);',
        f'user_pref("ui.highlight", "{c["accent"]}");',
        f'user_pref("ui.highlighttext", "{c["on_accent"]}");',
        f'user_pref("browser.display.background_color.dark", "{c["bg"]}");',
        PREFS_MARK[1],
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- profiles

def firefox_roots():
    home = os.path.expanduser("~")
    return [p for p in (os.path.join(os.environ.get("XDG_CONFIG_HOME", home + "/.config"), "mozilla/firefox"),
                        home + "/.mozilla/firefox") if os.path.isfile(os.path.join(p, "profiles.ini"))]


def default_profile():
    """The profile Firefox actually opens: installs.ini/[Install*] Default, else Default=1."""
    for root in firefox_roots():
        ini = configparser.RawConfigParser()
        ini.optionxform = str
        ini.read(os.path.join(root, "profiles.ini"))
        for sec in ini.sections():
            if sec.startswith("Install") and ini.has_option(sec, "Default"):
                return os.path.join(root, ini.get(sec, "Default"))
        for sec in ini.sections():
            if ini.get(sec, "Default", fallback="") == "1":
                path = ini.get(sec, "Path")
                rel = ini.get(sec, "IsRelative", fallback="1") == "1"
                return os.path.join(root, path) if rel else path
    return None


def running_pid(profile):
    """PID holding the profile lock (symlink 'host:+pid'), if that process is alive."""
    try:
        target = os.readlink(os.path.join(profile, "lock"))
        pid = int(target.rsplit("+", 1)[1])
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError, IndexError):
        return None


def backup(path, root):
    if os.path.exists(path):
        dst = os.path.join(root, time.strftime("%Y%m%d-%H%M%S"), os.path.basename(path))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)


def write_prefs_block(path, block):
    old = open(path).read() if os.path.exists(path) else ""
    pat = re.compile(re.escape(PREFS_MARK[0]) + r".*?" + re.escape(PREFS_MARK[1]) + r"\n?", re.S)
    new = pat.sub(lambda _: block, old) if pat.search(old) else (old.rstrip("\n") + "\n\n" if old else "") + block
    with open(path, "w") as fh:
        fh.write(new)


def set_base_theme(profile):
    """Switch the active theme to built-in Dark (Firefox must be closed)."""
    ext = os.path.join(profile, "extensions.json")
    if os.path.exists(ext):
        data = json.load(open(ext))
        changed = False
        for a in data.get("addons", []):
            if a.get("type") != "theme":
                continue
            want = a["id"] == BASE_THEME
            if a.get("active") != want or a.get("userDisabled") != (not want):
                a["active"], a["userDisabled"] = want, not want
                changed = True
        if changed:
            with open(ext, "w") as fh:
                json.dump(data, fh)
            # startup cache gets rebuilt from extensions.json
            for f in glob.glob(os.path.join(profile, "addonStartup.json.lz4")):
                os.remove(f)
    prefs = os.path.join(profile, "prefs.js")
    if os.path.exists(prefs):
        s = open(prefs).read()
        s = re.sub(r'user_pref\("extensions\.activeThemeID", "[^"]*"\);',
                   f'user_pref("extensions.activeThemeID", "{BASE_THEME}");', s)
        with open(prefs, "w") as fh:
            fh.write(s)


def resume_once(profile):
    """Make the next start restore the session even if the user's startup page is the home page."""
    prefs = os.path.join(profile, "prefs.js")
    s = open(prefs).read() if os.path.exists(prefs) else ""
    s = re.sub(r'user_pref\("browser\.sessionstore\.resume_session_once", \w+\);\n?', "", s)
    s += 'user_pref("browser.sessionstore.resume_session_once", true);\n'
    with open(prefs, "w") as fh:
        fh.write(s)
