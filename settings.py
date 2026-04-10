# settings.py

import os
import sys
import json
import math
import pygame

# =====================
# Screen defaults
# =====================
DEFAULT_WIDTH, DEFAULT_HEIGHT = 1920, 1080
CONFIG_FILE = "config.txt"

# =====================
# Palette (dark slate / teal accent) — from design
# =====================
BG             = (12,  14,  20 )
PANEL          = (20,  24,  34 )
PANEL2         = (26,  30,  42 )
BORDER         = (38,  46,  64 )
BORDER_HI      = (60,  80, 120 )
CARD_BG        = (30,  36,  50 )
CARD_HOV       = (44,  54,  76 )
CARD_GREY      = (18,  20,  26 )
WHITE          = (225, 232, 245)
MUTED          = (95,  108, 132)
DIM            = (55,  65,  85 )
RED            = (210,  65,  65)
AMBER          = (215, 155,  45)
BLUE           = (75,  145, 255)
TEAL           = (45,  195, 165)
GREEN          = (65,  190,  95)
PURPLE         = (145,  90, 220)
GOLD           = (255, 215,   0)
OVERLAY        = (8,   10,  16, 225)
PINK           = (220, 120, 160)
SALMON         = (230, 140, 110)

# =====================
# Resolution options
# =====================
RESOLUTIONS = [
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    (3840, 2160),
]

# FPS options
FPS_OPTIONS = [30, 60, 120, 144, 240]

# Theme options
THEMES = ["Dark Slate", "Midnight Blue", "Deep Purple", "Forest Green"]
THEME_PALETTES = {
    "Dark Slate":    {"bg": (12, 14, 20),  "panel": (20, 24, 34),  "accent": (75, 145, 255)},
    "Midnight Blue": {"bg": (10, 12, 28),  "panel": (18, 22, 44),  "accent": (60, 130, 240)},
    "Deep Purple":   {"bg": (16, 10, 24),  "panel": (28, 18, 38),  "accent": (145, 90, 220)},
    "Forest Green":  {"bg": (8, 16, 12),   "panel": (16, 28, 22),  "accent": (45, 195, 165)},
}

# =====================
# Default config
# =====================
DEFAULT_CONFIG = {
    "display": {
        "resolution": [1920, 1080],
        "fullscreen": False,
        "vsync": True,
        "fps_limit": 60,
        "theme": "Dark Slate",
    },
    "audio": {
        "master_volume": 80,
        "music_volume": 70,
        "sfx_volume": 90,
        "muted": False,
    },
    "gameplay": {
        "player_name": "Player",
        "starting_balance": 1000,
        "auto_save": True,
        "show_hints": True,
        "card_animation_speed": 2,  # 1=slow, 2=normal, 3=fast
        "confirm_bets": True,
        "show_hand_value": True,
    },
    "controls": {
        "hit_key": "H",
        "stand_key": "S",
        "double_key": "D",
        "split_key": "P",
        "surrender_key": "R",
    },
    "accessibility": {
        "colorblind_mode": False,
        "large_text": False,
        "high_contrast": False,
        "screen_shake": True,
    },
    "about": {
        "game_name": "Casino Suite",
        "studio": "219 Studios",
        "website": "www.219Studios.com/game/cardgame",
        "game_version": "0.3",
        "python_version": "",
        "pygame_version": "",
    },
}


# =====================
# Helpers
# =====================
def rrect(surf, color, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)


def panel_box(surf, rect, r=10):
    rrect(surf, PANEL, rect, r)
    rrect(surf, BORDER, rect, r, 1)


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


# =====================
# Config I/O
# =====================
def load_config():
    """Load config from JSON file, merging with defaults."""
    config = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                saved = json.load(f)
            # Merge saved into config (preserving defaults for missing keys)
            for section, values in saved.items():
                if section in config and isinstance(values, dict):
                    for k, v in values.items():
                        config[section][k] = v
                else:
                    config[section] = values
        except Exception as e:
            print(f"Config load error: {e}")
    # Fill runtime info
    config["about"]["python_version"] = f"Python {sys.version.split()[0]}"
    config["about"]["pygame_version"] = f"pygame {pygame.version.ver} (SDL {'.'.join(str(x) for x in pygame.version.SDL)})"
    return config


def save_config(config):
    """Save config to JSON file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Config save error: {e}")
        return False


# =====================
# UI Components
# =====================
class Slider:
    """Horizontal slider widget."""
    def __init__(self, x, y, w, h, min_val=0, max_val=100, value=50, label="", suffix="%"):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.label = label
        self.suffix = suffix
        self.dragging = False
        self.track_rect = pygame.Rect(x, y + h // 2 - 3, w, 6)
        self.thumb_radius = 10

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            tx = self._thumb_x()
            ty = self.rect.y + self.rect.height // 2
            dist = ((e.pos[0] - tx)**2 + (e.pos[1] - ty)**2) ** 0.5
            if dist < self.thumb_radius + 5 or self.track_rect.collidepoint(e.pos):
                self.dragging = True
                self._update_from_pos(e.pos[0])
                return True
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            self.dragging = False
        elif e.type == pygame.MOUSEMOTION and self.dragging:
            self._update_from_pos(e.pos[0])
            return True
        return False

    def _update_from_pos(self, mx):
        frac = (mx - self.rect.x) / max(1, self.rect.width)
        frac = clamp(frac, 0, 1)
        self.value = int(self.min_val + frac * (self.max_val - self.min_val))

    def _thumb_x(self):
        frac = (self.value - self.min_val) / max(1, self.max_val - self.min_val)
        return self.rect.x + int(frac * self.rect.width)

    def draw(self, surf, fonts):
        mx, my = pygame.mouse.get_pos()
        tx = self._thumb_x()
        ty = self.rect.y + self.rect.height // 2

        # Label
        ls = fonts["small"].render(self.label, True, MUTED)
        surf.blit(ls, (self.rect.x, self.rect.y - 18))

        # Value
        vs = fonts["small"].render(f"{self.value}{self.suffix}", True, TEAL)
        surf.blit(vs, (self.rect.right - vs.get_width(), self.rect.y - 18))

        # Track background
        rrect(surf, (35, 42, 58), self.track_rect, r=3)

        # Filled portion
        filled = pygame.Rect(self.rect.x, self.track_rect.y, tx - self.rect.x, 6)
        if filled.width > 0:
            rrect(surf, TEAL, filled, r=3)

        # Thumb
        hov = ((mx - tx)**2 + (my - ty)**2) ** 0.5 < self.thumb_radius + 5
        thumb_col = WHITE if (hov or self.dragging) else TEAL
        pygame.draw.circle(surf, thumb_col, (tx, ty), self.thumb_radius)
        pygame.draw.circle(surf, (20, 20, 30), (tx, ty), self.thumb_radius - 3)
        pygame.draw.circle(surf, thumb_col, (tx, ty), 4)


class Toggle:
    """Toggle switch widget."""
    def __init__(self, x, y, value=False, label=""):
        self.x = x
        self.y = y
        self.value = value
        self.label = label
        self.w = 48
        self.h = 24
        self.rect = pygame.Rect(x, y, self.w, self.h)

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos):
                self.value = not self.value
                return True
        return False

    def draw(self, surf, fonts):
        mx, my = pygame.mouse.get_pos()
        hov = self.rect.collidepoint(mx, my)

        # Label
        ls = fonts["small"].render(self.label, True, MUTED)
        surf.blit(ls, (self.x - ls.get_width() - 12, self.y + 3))

        # Track
        track_col = GREEN if self.value else (50, 55, 70)
        if hov:
            track_col = tuple(min(255, c + 20) for c in track_col)
        rrect(surf, track_col, self.rect, r=12)

        # Thumb
        thumb_x = self.x + self.w - 12 if self.value else self.x + 12
        thumb_y = self.y + self.h // 2
        pygame.draw.circle(surf, WHITE, (thumb_x, thumb_y), 9)

        # Status text
        st = fonts["small"].render("ON" if self.value else "OFF", True, GREEN if self.value else DIM)
        surf.blit(st, (self.x + self.w + 8, self.y + 3))


class Dropdown:
    """Dropdown selector widget."""
    def __init__(self, x, y, w, options, selected=0, label=""):
        self.x = x
        self.y = y
        self.w = w
        self.h = 32
        self.options = options
        self.selected = selected
        self.label = label
        self.open = False
        self.rect = pygame.Rect(x, y, w, self.h)

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.open:
                for i, opt in enumerate(self.options):
                    opt_r = pygame.Rect(self.x, self.y + self.h + i * 30, self.w, 30)
                    if opt_r.collidepoint(e.pos):
                        self.selected = i
                        self.open = False
                        return True
                self.open = False
                return False
            elif self.rect.collidepoint(e.pos):
                self.open = True
                return True
        return False

    def draw(self, surf, fonts):
        mx, my = pygame.mouse.get_pos()
        hov = self.rect.collidepoint(mx, my)

        # Label
        ls = fonts["small"].render(self.label, True, MUTED)
        surf.blit(ls, (self.x, self.y - 18))

        # Main box
        bg = CARD_HOV if hov else CARD_BG
        rrect(surf, bg, self.rect, r=6)
        rrect(surf, BLUE if self.open else BORDER, self.rect, r=6, bw=1)

        # Selected text
        txt = str(self.options[self.selected]) if self.selected < len(self.options) else ""
        ts = fonts["normal"].render(txt, True, WHITE)
        surf.blit(ts, (self.x + 10, self.y + 6))

        # Arrow
        arrow = "▼" if not self.open else "▲"
        ar = fonts["normal"].render(arrow, True, MUTED)
        surf.blit(ar, (self.x + self.w - 24, self.y + 6))

        # Dropdown list
        if self.open:
            for i, opt in enumerate(self.options):
                opt_r = pygame.Rect(self.x, self.y + self.h + i * 30, self.w, 30)
                opt_hov = opt_r.collidepoint(mx, my)
                bg = CARD_HOV if opt_hov else PANEL2
                if i == self.selected:
                    bg = (30, 50, 70)
                rrect(surf, bg, opt_r, r=0 if i < len(self.options) - 1 else 6)
                rrect(surf, BORDER, opt_r, r=0 if i < len(self.options) - 1 else 6, bw=1)
                os_txt = fonts["normal"].render(str(opt), True, WHITE if i == self.selected else MUTED)
                surf.blit(os_txt, (self.x + 10, opt_r.y + 5))

    def selected_value(self):
        if 0 <= self.selected < len(self.options):
            return self.options[self.selected]
        return None


class TextInput:
    """Simple text input widget."""
    def __init__(self, x, y, w, text="", label="", max_len=20):
        self.x = x
        self.y = y
        self.w = w
        self.h = 32
        self.text = text
        self.label = label
        self.max_len = max_len
        self.active = False
        self.rect = pygame.Rect(x, y, w, self.h)
        self.cursor_timer = 0

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.active = self.rect.collidepoint(e.pos)
            return self.active
        if e.type == pygame.KEYDOWN and self.active:
            if e.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return True
            elif e.key == pygame.K_RETURN:
                self.active = False
                return True
            elif e.key == pygame.K_ESCAPE:
                self.active = False
                return True
            elif len(self.text) < self.max_len and e.unicode.isprintable() and e.unicode:
                self.text += e.unicode
                return True
        return False

    def draw(self, surf, fonts):
        self.cursor_timer = (self.cursor_timer + 1) % 60

        # Label
        ls = fonts["small"].render(self.label, True, MUTED)
        surf.blit(ls, (self.x, self.y - 18))

        # Box
        bg = (35, 42, 58) if self.active else CARD_BG
        bord = BLUE if self.active else BORDER
        rrect(surf, bg, self.rect, r=6)
        rrect(surf, bord, self.rect, r=6, bw=2 if self.active else 1)

        # Text
        ts = fonts["normal"].render(self.text, True, WHITE)
        surf.blit(ts, (self.x + 8, self.y + 6))

        # Cursor
        if self.active and self.cursor_timer < 30:
            cx = self.x + 8 + ts.get_width() + 2
            pygame.draw.line(surf, WHITE, (cx, self.y + 6), (cx, self.y + self.h - 6), 2)


# =====================
# Settings Screen
# =====================
class SettingsScreen:
    # Tab definitions
    TABS = ["Display", "Audio", "Gameplay", "Controls", "Accessibility", "About"]
    TAB_ICONS = ["🖥", "🔊", "", "⌨", "♿", "ℹ"]

    def __init__(self, display):
        self.display = display
        self.width, self.height = display.get_size()
        self.fonts = {
            "normal":  pygame.font.Font(None, 24),
            "small":   pygame.font.Font(None, 20),
            "large":   pygame.font.Font(None, 40),
            "title":   pygame.font.Font(None, 48),
            "huge":    pygame.font.Font(None, 64),
            "section": pygame.font.Font(None, 28),
            "key":     pygame.font.Font(None, 22),
        }

        self.config = load_config()
        self.active_tab = 0
        self.scroll_y = 0
        self.max_scroll = 0

        self.status = ""
        self.status_timer = 0
        self.unsaved = False

        # Build widgets
        self._build_widgets()

    def _build_widgets(self):
        """Create all interactive widgets from config."""
        cfg = self.config
        wx = 380  # widget x start (right of labels)
        content_x = 300

        # --- Display ---
        res_strs = [f"{w}×{h}" for w, h in RESOLUTIONS]
        current_res = cfg["display"]["resolution"]
        res_idx = 0
        for i, (w, h) in enumerate(RESOLUTIONS):
            if w == current_res[0] and h == current_res[1]:
                res_idx = i
                break
        self.dd_resolution = Dropdown(content_x + 200, 0, 200, res_strs, res_idx, "Resolution")

        fps_idx = FPS_OPTIONS.index(cfg["display"]["fps_limit"]) if cfg["display"]["fps_limit"] in FPS_OPTIONS else 1
        self.dd_fps = Dropdown(content_x + 200, 0, 140, [str(f) + " FPS" for f in FPS_OPTIONS], fps_idx, "FPS Limit")

        self.tg_fullscreen = Toggle(content_x + 300, 0, cfg["display"]["fullscreen"], "Fullscreen")
        self.tg_vsync = Toggle(content_x + 300, 0, cfg["display"]["vsync"], "VSync")

        theme_idx = THEMES.index(cfg["display"]["theme"]) if cfg["display"]["theme"] in THEMES else 0
        self.dd_theme = Dropdown(content_x + 200, 0, 200, THEMES, theme_idx, "Theme")

        # --- Audio ---
        self.sl_master = Slider(content_x + 160, 0, 280, 30, 0, 100, cfg["audio"]["master_volume"], "Master Volume")
        self.sl_music = Slider(content_x + 160, 0, 280, 30, 0, 100, cfg["audio"]["music_volume"], "Music Volume")
        self.sl_sfx = Slider(content_x + 160, 0, 280, 30, 0, 100, cfg["audio"]["sfx_volume"], "SFX Volume")
        self.tg_muted = Toggle(content_x + 300, 0, cfg["audio"]["muted"], "Mute All")

        # --- Gameplay ---
        self.ti_name = TextInput(content_x + 160, 0, 220, cfg["gameplay"]["player_name"], "Player Name")
        self.sl_balance = Slider(content_x + 160, 0, 280, 30, 100, 10000, cfg["gameplay"]["starting_balance"], "Starting Balance", suffix="$")

        anim_speeds = ["Slow", "Normal", "Fast"]
        anim_idx = clamp(cfg["gameplay"]["card_animation_speed"] - 1, 0, 2)
        self.dd_anim_speed = Dropdown(content_x + 200, 0, 160, anim_speeds, anim_idx, "Card Animation")

        self.tg_auto_save = Toggle(content_x + 300, 0, cfg["gameplay"]["auto_save"], "Auto Save")
        self.tg_show_hints = Toggle(content_x + 300, 0, cfg["gameplay"]["show_hints"], "Show Hints")
        self.tg_confirm_bets = Toggle(content_x + 300, 0, cfg["gameplay"]["confirm_bets"], "Confirm Bets")
        self.tg_show_hand_value = Toggle(content_x + 300, 0, cfg["gameplay"]["show_hand_value"], "Show Hand Value")

        # --- Controls ---
        self.ti_hit = TextInput(content_x + 200, 0, 80, cfg["controls"]["hit_key"], "Hit Key", max_len=1)
        self.ti_stand = TextInput(content_x + 200, 0, 80, cfg["controls"]["stand_key"], "Stand Key", max_len=1)
        self.ti_double = TextInput(content_x + 200, 0, 80, cfg["controls"]["double_key"], "Double Key", max_len=1)
        self.ti_split = TextInput(content_x + 200, 0, 80, cfg["controls"]["split_key"], "Split Key", max_len=1)
        self.ti_surrender = TextInput(content_x + 200, 0, 80, cfg["controls"]["surrender_key"], "Surrender Key", max_len=1)

        # --- Accessibility ---
        self.tg_colorblind = Toggle(content_x + 300, 0, cfg["accessibility"]["colorblind_mode"], "Colorblind Mode")
        self.tg_large_text = Toggle(content_x + 300, 0, cfg["accessibility"]["large_text"], "Large Text")
        self.tg_high_contrast = Toggle(content_x + 300, 0, cfg["accessibility"]["high_contrast"], "High Contrast")
        self.tg_screen_shake = Toggle(content_x + 300, 0, cfg["accessibility"]["screen_shake"], "Screen Shake")

    def _collect_config(self):
        """Collect current widget values into config dict."""
        cfg = self.config

        # Display
        res_val = self.dd_resolution.selected_value()
        if res_val:
            parts = res_val.replace("×", "x").split("x")
            cfg["display"]["resolution"] = [int(parts[0]), int(parts[1])]
        cfg["display"]["fullscreen"] = self.tg_fullscreen.value
        cfg["display"]["vsync"] = self.tg_vsync.value
        fps_val = self.dd_fps.selected_value()
        if fps_val:
            cfg["display"]["fps_limit"] = int(fps_val.replace(" FPS", ""))
        theme_val = self.dd_theme.selected_value()
        if theme_val:
            cfg["display"]["theme"] = theme_val

        # Audio
        cfg["audio"]["master_volume"] = self.sl_master.value
        cfg["audio"]["music_volume"] = self.sl_music.value
        cfg["audio"]["sfx_volume"] = self.sl_sfx.value
        cfg["audio"]["muted"] = self.tg_muted.value

        # Gameplay
        cfg["gameplay"]["player_name"] = self.ti_name.text or "Player"
        cfg["gameplay"]["starting_balance"] = self.sl_balance.value
        cfg["gameplay"]["card_animation_speed"] = self.dd_anim_speed.selected + 1
        cfg["gameplay"]["auto_save"] = self.tg_auto_save.value
        cfg["gameplay"]["show_hints"] = self.tg_show_hints.value
        cfg["gameplay"]["confirm_bets"] = self.tg_confirm_bets.value
        cfg["gameplay"]["show_hand_value"] = self.tg_show_hand_value.value

        # Controls
        cfg["controls"]["hit_key"] = self.ti_hit.text.upper() or "H"
        cfg["controls"]["stand_key"] = self.ti_stand.text.upper() or "S"
        cfg["controls"]["double_key"] = self.ti_double.text.upper() or "D"
        cfg["controls"]["split_key"] = self.ti_split.text.upper() or "P"
        cfg["controls"]["surrender_key"] = self.ti_surrender.text.upper() or "R"

        # Accessibility
        cfg["accessibility"]["colorblind_mode"] = self.tg_colorblind.value
        cfg["accessibility"]["large_text"] = self.tg_large_text.value
        cfg["accessibility"]["high_contrast"] = self.tg_high_contrast.value
        cfg["accessibility"]["screen_shake"] = self.tg_screen_shake.value

        return cfg

    def save(self):
        self.config = self._collect_config()
        if save_config(self.config):
            self.set_status("Settings saved to config.txt!")
            self.unsaved = False
        else:
            self.set_status("Error saving settings!")

    def reset_defaults(self):
        self.config = json.loads(json.dumps(DEFAULT_CONFIG))
        self.config["about"]["python_version"] = f"Python {sys.version.split()[0]}"
        self.config["about"]["pygame_version"] = f"pygame {pygame.version.ver} (SDL {'.'.join(str(x) for x in pygame.version.SDL)})"
        self._build_widgets()
        self.unsaved = True
        self.set_status("Reset to defaults (unsaved)")

    def set_status(self, msg, dur=120):
        self.status = msg
        self.status_timer = dur

    def tick_status(self):
        if self.status_timer > 0:
            self.status_timer -= 1
            if self.status_timer == 0:
                self.status = ""

    def txt(self, text, x, y, color=WHITE, fk="normal", center=False):
        s = self.fonts[fk].render(str(text), True, color)
        if center:
            self.display.blit(s, (x - s.get_width() // 2, y - s.get_height() // 2))
        else:
            self.display.blit(s, (x, y))

    # ===================================================================
    # DRAWING
    # ===================================================================
    def draw(self):
        self.tick_status()
        self.display.fill(BG)
        W, H = self.width, self.height

        # ---- Header ----
        header_r = pygame.Rect(0, 0, W, 70)
        rrect(self.display, PANEL, header_r, r=0)
        pygame.draw.line(self.display, BORDER, (0, 70), (W, 70), 1)

        self.txt("⚙  SETTINGS", 30, 18, WHITE, "title")

        if self.unsaved:
            self.txt("● UNSAVED CHANGES", 320, 30, AMBER, "small")

        # Save button (header)
        mx, my = pygame.mouse.get_pos()
        save_r = pygame.Rect(W - 260, 16, 110, 38)
        hov_save = save_r.collidepoint(mx, my)
        rrect(self.display, GREEN if not hov_save else (95, 220, 125), save_r, r=8)
        rrect(self.display, (100, 220, 130), save_r, r=8, bw=2 if hov_save else 1)
        self.txt("SAVE", save_r.centerx, save_r.centery, WHITE, "normal", center=True)

        # Reset button
        reset_r = pygame.Rect(W - 140, 16, 120, 38)
        hov_reset = reset_r.collidepoint(mx, my)
        rrect(self.display, RED if hov_reset else (80, 30, 30), reset_r, r=8)
        self.txt("RESET", reset_r.centerx, reset_r.centery, WHITE, "normal", center=True)

        # ESC hint
        self.txt("ESC to return", W - 400, 30, DIM, "small")

        # ---- Tabs (left sidebar) ----
        tab_w = 200
        tab_h = 50
        tab_x = 15
        tab_y_start = 90

        sidebar_r = pygame.Rect(0, 70, tab_w + 30, H - 70)
        rrect(self.display, PANEL2, sidebar_r, r=0)
        pygame.draw.line(self.display, BORDER, (tab_w + 30, 70), (tab_w + 30, H), 1)

        for i, (tab_name, icon) in enumerate(zip(self.TABS, self.TAB_ICONS)):
            tr = pygame.Rect(tab_x, tab_y_start + i * (tab_h + 6), tab_w, tab_h)
            active = i == self.active_tab
            hov = tr.collidepoint(mx, my)

            if active:
                bg = (28, 40, 60)
                bord = BLUE
                tc = WHITE
                # Active indicator bar
                pygame.draw.rect(self.display, BLUE,
                                 pygame.Rect(tr.x, tr.y, 4, tr.height),
                                 border_top_left_radius=4, border_bottom_left_radius=4)
            elif hov:
                bg = (24, 30, 44)
                bord = BORDER_HI
                tc = WHITE
            else:
                bg = PANEL2
                bord = PANEL2
                tc = MUTED

            rrect(self.display, bg, tr, r=8)
            if active or hov:
                rrect(self.display, bord, tr, r=8, bw=1)

            self.txt(f"{icon}  {tab_name}", tr.x + 16, tr.centery, tc, "normal", center=False)
            # Adjust vertical centering
            ts = self.fonts["normal"].render(f"{icon}  {tab_name}", True, tc)
            self.display.blit(ts, (tr.x + 16, tr.centery - ts.get_height() // 2))

        # ---- Content area ----
        content_x = tab_w + 50
        content_y = 90
        content_w = W - content_x - 30
        content_h = H - content_y - 20

        # Clip content
        content_rect = pygame.Rect(content_x - 10, content_y, content_w + 20, content_h)

        tab = self.TABS[self.active_tab]

        if tab == "Display":
            self._draw_display_tab(content_x, content_y, content_w)
        elif tab == "Audio":
            self._draw_audio_tab(content_x, content_y, content_w)
        elif tab == "Gameplay":
            self._draw_gameplay_tab(content_x, content_y, content_w)
        elif tab == "Controls":
            self._draw_controls_tab(content_x, content_y, content_w)
        elif tab == "Accessibility":
            self._draw_accessibility_tab(content_x, content_y, content_w)
        elif tab == "About":
            self._draw_about_tab(content_x, content_y, content_w)

        # ---- Status bar ----
        if self.status:
            sr = pygame.Rect(W // 2 - 200, H - 45, 400, 30)
            rrect(self.display, PANEL, sr, r=8)
            rrect(self.display, BORDER, sr, r=8, bw=1)
            col = GREEN if "saved" in self.status.lower() else \
                  AMBER if "unsaved" in self.status.lower() or "Reset" in self.status else \
                  RED if "Error" in self.status else WHITE
            self.txt(self.status, sr.centerx, sr.centery, col, "small", center=True)

        # ---- Footer ----
        self.txt("S = Save  •  R = Reset Defaults  •  TAB = Next Tab  •  ESC = Back",
                 W // 2, H - 12, DIM, "small", center=True)

    def _section_header(self, text, x, y, w):
        """Draw a section header with line."""
        self.txt(text, x, y, WHITE, "section")
        pygame.draw.line(self.display, BORDER, (x, y + 28), (x + w - 40, y + 28), 1)
        return y + 40

    def _setting_row(self, label, x, y, desc=None):
        """Draw a setting label and optional description. Returns next y."""
        self.txt(label, x, y + 4, WHITE, "normal")
        if desc:
            self.txt(desc, x, y + 24, DIM, "small")
            return y + 48
        return y + 36

    # --- DISPLAY TAB ---
    def _draw_display_tab(self, cx, cy, cw):
        y = cy
        y = self._section_header("Display Settings", cx, y, cw)

        # Resolution
        self.dd_resolution.x = cx + 240
        self.dd_resolution.y = y + 4
        self.dd_resolution.label = ""
        self.txt("Resolution", cx, y + 10, WHITE, "normal")
        self.dd_resolution.draw(self.display, self.fonts)
        y += 50

        # FPS
        self.dd_fps.x = cx + 240
        self.dd_fps.y = y + 4
        self.dd_fps.label = ""
        self.txt("FPS Limit", cx, y + 10, WHITE, "normal")
        self.dd_fps.draw(self.display, self.fonts)
        y += 50

        # Fullscreen
        self.tg_fullscreen.x = cx + 240
        self.tg_fullscreen.y = y + 4
        self.tg_fullscreen.rect = pygame.Rect(cx + 240, y + 4, self.tg_fullscreen.w, self.tg_fullscreen.h)
        self.tg_fullscreen.label = ""
        self.txt("Fullscreen", cx, y + 8, WHITE, "normal")
        self.tg_fullscreen.draw(self.display, self.fonts)
        self.txt("Press F11 to toggle", cx + 340, y + 8, DIM, "small")
        y += 44

        # VSync
        self.tg_vsync.x = cx + 240
        self.tg_vsync.y = y + 4
        self.tg_vsync.rect = pygame.Rect(cx + 240, y + 4, self.tg_vsync.w, self.tg_vsync.h)
        self.tg_vsync.label = ""
        self.txt("VSync", cx, y + 8, WHITE, "normal")
        self.tg_vsync.draw(self.display, self.fonts)
        y += 44

        # Theme
        y += 10
        y = self._section_header("Appearance", cx, y, cw)
        self.dd_theme.x = cx + 240
        self.dd_theme.y = y + 4
        self.dd_theme.label = ""
        self.txt("Color Theme", cx, y + 10, WHITE, "normal")
        self.dd_theme.draw(self.display, self.fonts)
        y += 50

        # Theme preview
        theme_name = self.dd_theme.selected_value() or "Dark Slate"
        if theme_name in THEME_PALETTES:
            tp = THEME_PALETTES[theme_name]
            preview_r = pygame.Rect(cx, y + 5, cw - 40, 60)
            rrect(self.display, tp["bg"], preview_r, r=8)
            inner = pygame.Rect(cx + 10, y + 15, 120, 40)
            rrect(self.display, tp["panel"], inner, r=6)
            rrect(self.display, tp["accent"], inner, r=6, bw=2)
            self.txt("Preview", inner.centerx, inner.centery, WHITE, "small", center=True)

            accent_r = pygame.Rect(cx + 150, y + 20, 80, 30)
            rrect(self.display, tp["accent"], accent_r, r=6)
            self.txt("Accent", accent_r.centerx, accent_r.centery, WHITE, "small", center=True)

    # --- AUDIO TAB ---
    def _draw_audio_tab(self, cx, cy, cw):
        y = cy
        y = self._section_header("Audio Settings", cx, y, cw)

        # Master
        self.sl_master.rect.x = cx + 180
        self.sl_master.rect.y = y
        self.sl_master.track_rect = pygame.Rect(cx + 180, y + 15, 280, 6)
        self.sl_master.label = "Master Volume"
        self.txt("Master Volume", cx, y + 8, WHITE, "normal")
        self.sl_master.draw(self.display, self.fonts)
        # Visual bar
        bar_x = cx + 480
        bar_w = 120
        bar_h = 14
        rrect(self.display, (35, 42, 58), pygame.Rect(bar_x, y + 8, bar_w, bar_h), r=4)
        fill_w = int(bar_w * self.sl_master.value / 100)
        if fill_w > 0:
            rrect(self.display, TEAL, pygame.Rect(bar_x, y + 8, fill_w, bar_h), r=4)
        y += 60

        # Music
        self.sl_music.rect.x = cx + 180
        self.sl_music.rect.y = y
        self.sl_music.track_rect = pygame.Rect(cx + 180, y + 15, 280, 6)
        self.sl_music.label = "Music Volume"
        self.txt("Music Volume", cx, y + 8, WHITE, "normal")
        self.sl_music.draw(self.display, self.fonts)
        y += 60

        # SFX
        self.sl_sfx.rect.x = cx + 180
        self.sl_sfx.rect.y = y
        self.sl_sfx.track_rect = pygame.Rect(cx + 180, y + 15, 280, 6)
        self.sl_sfx.label = "SFX Volume"
        self.txt("SFX Volume", cx, y + 8, WHITE, "normal")
        self.sl_sfx.draw(self.display, self.fonts)
        y += 60

        # Mute
        self.tg_muted.x = cx + 240
        self.tg_muted.y = y + 4
        self.tg_muted.rect = pygame.Rect(cx + 240, y + 4, self.tg_muted.w, self.tg_muted.h)
        self.tg_muted.label = ""
        self.txt("Mute All Audio", cx, y + 8, WHITE, "normal")
        self.tg_muted.draw(self.display, self.fonts)
        y += 50

        # Volume visualization
        y += 10
        y = self._section_header("Volume Preview", cx, y, cw)
        # Animated bars
        effective_master = 0 if self.tg_muted.value else self.sl_master.value / 100
        channels = [
            ("Master", self.sl_master.value, TEAL),
            ("Music", self.sl_music.value, BLUE),
            ("SFX", self.sl_sfx.value, GREEN),
        ]
        for i, (name, vol, col) in enumerate(channels):
            by = y + i * 35
            self.txt(name, cx, by + 4, MUTED, "small")
            bar_bg = pygame.Rect(cx + 80, by + 4, 300, 18)
            rrect(self.display, (35, 42, 58), bar_bg, r=4)
            effective = int(vol * effective_master)
            if effective > 0:
                bar_fill = pygame.Rect(cx + 80, by + 4, int(300 * effective / 100), 18)
                rrect(self.display, col, bar_fill, r=4)
            self.txt(f"{effective}%", cx + 390, by + 4, MUTED, "small")

    # --- GAMEPLAY TAB ---
    def _draw_gameplay_tab(self, cx, cy, cw):
        y = cy
        y = self._section_header("Player Settings", cx, y, cw)

        # Player name
        self.ti_name.x = cx + 200
        self.ti_name.y = y + 4
        self.ti_name.rect = pygame.Rect(cx + 200, y + 4, 220, 32)
        self.ti_name.label = ""
        self.txt("Player Name", cx, y + 10, WHITE, "normal")
        self.ti_name.draw(self.display, self.fonts)
        y += 50

        # Starting balance
        self.sl_balance.rect.x = cx + 200
        self.sl_balance.rect.y = y
        self.sl_balance.track_rect = pygame.Rect(cx + 200, y + 15, 280, 6)
        self.sl_balance.label = ""
        self.sl_balance.suffix = ""
        self.txt("Starting Balance", cx, y + 8, WHITE, "normal")
        self.sl_balance.draw(self.display, self.fonts)
        self.txt(f"${self.sl_balance.value}", cx + 500, y + 8, GOLD, "normal")
        y += 60

        # Animation speed
        self.dd_anim_speed.x = cx + 200
        self.dd_anim_speed.y = y + 4
        self.dd_anim_speed.label = ""
        self.txt("Card Animation", cx, y + 10, WHITE, "normal")
        self.dd_anim_speed.draw(self.display, self.fonts)
        y += 50

        y += 10
        y = self._section_header("Game Options", cx, y, cw)

        toggles = [
            (self.tg_auto_save, "Auto Save", "Automatically save game progress"),
            (self.tg_show_hints, "Show Hints", "Display helpful tips during gameplay"),
            (self.tg_confirm_bets, "Confirm Bets", "Ask for confirmation before placing bets"),
            (self.tg_show_hand_value, "Show Hand Value", "Display hand total during play"),
        ]
        for tg, label, desc in toggles:
            tg.x = cx + 280
            tg.y = y + 4
            tg.rect = pygame.Rect(cx + 280, y + 4, tg.w, tg.h)
            tg.label = ""
            self.txt(label, cx, y + 4, WHITE, "normal")
            self.txt(desc, cx, y + 24, DIM, "small")
            tg.draw(self.display, self.fonts)
            y += 50

    # --- CONTROLS TAB ---
    def _draw_controls_tab(self, cx, cy, cw):
        y = cy
        y = self._section_header("Key Bindings", cx, y, cw)
        self.txt("Click a field and press a key to rebind", cx, y, DIM, "small")
        y += 30

        inputs = [
            (self.ti_hit, "Hit"),
            (self.ti_stand, "Stand"),
            (self.ti_double, "Double Down"),
            (self.ti_split, "Split"),
            (self.ti_surrender, "Surrender"),
        ]
        for ti, label in inputs:
            ti.x = cx + 220
            ti.y = y + 4
            ti.rect = pygame.Rect(cx + 220, y + 4, 80, 32)
            ti.label = ""
            self.txt(label, cx, y + 10, WHITE, "normal")
            ti.draw(self.display, self.fonts)

            # Show default
            default_keys = {"Hit": "H", "Stand": "S", "Double Down": "D", "Split": "P", "Surrender": "R"}
            self.txt(f"(default: {default_keys.get(label, '?')})", cx + 320, y + 10, DIM, "small")
            y += 48

        y += 20
        y = self._section_header("Global Controls", cx, y, cw)

        global_keys = [
            ("ESC", "Return to menu / Back"),
            ("ENTER", "Confirm / Deal / Spin"),
            ("F11", "Toggle fullscreen"),
            ("S", "Save settings (in settings screen)"),
            ("TAB", "Switch settings tab"),
        ]
        for key, desc in global_keys:
            kr = pygame.Rect(cx, y, 50, 26)
            rrect(self.display, (32, 44, 62), kr, r=5)
            rrect(self.display, BORDER, kr, r=5, bw=1)
            ks = self.fonts["key"].render(key, True, BLUE)
            self.display.blit(ks, (kr.centerx - ks.get_width() // 2, kr.centery - ks.get_height() // 2))
            self.txt(desc, cx + 62, y + 4, MUTED, "normal")
            y += 36

    # --- ACCESSIBILITY TAB ---
    def _draw_accessibility_tab(self, cx, cy, cw):
        y = cy
        y = self._section_header("Accessibility Options", cx, y, cw)

        toggles = [
            (self.tg_colorblind, "Colorblind Mode", "Adjusts colors for better visibility"),
            (self.tg_large_text, "Large Text", "Increases text size throughout the UI"),
            (self.tg_high_contrast, "High Contrast", "Increases contrast for better readability"),
            (self.tg_screen_shake, "Screen Shake", "Enable screen shake effects on events"),
        ]
        for tg, label, desc in toggles:
            tg.x = cx + 300
            tg.y = y + 4
            tg.rect = pygame.Rect(cx + 300, y + 4, tg.w, tg.h)
            tg.label = ""
            self.txt(label, cx, y + 4, WHITE, "normal")
            self.txt(desc, cx, y + 24, DIM, "small")
            tg.draw(self.display, self.fonts)
            y += 56

        # Preview
        y += 10
        y = self._section_header("Preview", cx, y, cw)
        preview_r = pygame.Rect(cx, y, cw - 40, 100)
        rrect(self.display, PANEL, preview_r, r=10)
        rrect(self.display, BORDER, preview_r, r=10, bw=1)

        fk = "large" if self.tg_large_text.value else "normal"
        sample = "The quick brown fox jumps over the lazy dog"
        tc = WHITE if not self.tg_high_contrast.value else (255, 255, 255)
        bg_c = BG if not self.tg_high_contrast.value else (0, 0, 0)
        rrect(self.display, bg_c, preview_r.inflate(-4, -4), r=8)
        self.txt(sample, preview_r.centerx, preview_r.centery - 10, tc, fk, center=True)

        if self.tg_colorblind.value:
            # Show modified color swatches
            colors = [("Red→Orange", (230, 140, 40)), ("Green→Blue", (40, 140, 230)),
                      ("Normal", WHITE)]
            sx = cx + 20
            for name, col in colors:
                pygame.draw.circle(self.display, col, (sx + 12, preview_r.bottom - 20), 10)
                self.txt(name, sx + 28, preview_r.bottom - 28, MUTED, "small")
                sx += 140

    # --- ABOUT TAB ---
    def _draw_about_tab(self, cx, cy, cw):
        y = cy
        y = self._section_header("About", cx, y, cw)

        cfg = self.config["about"]

        # Logo area
        logo_r = pygame.Rect(cx, y, cw - 40, 140)
        rrect(self.display, PANEL, logo_r, r=12)
        rrect(self.display, BORDER, logo_r, r=12, bw=1)

        self.txt(cfg["game_name"], logo_r.centerx, logo_r.y + 30, GOLD, "title", center=True)
        self.txt(cfg["studio"], logo_r.centerx, logo_r.y + 70, WHITE, "normal", center=True)
        self.txt(cfg["website"], logo_r.centerx, logo_r.y + 95, TEAL, "small", center=True)
        self.txt(f"Version {cfg['game_version']}", logo_r.centerx, logo_r.y + 118, MUTED, "small", center=True)

        y += 160

        y = self._section_header("System Information", cx, y, cw)

        info_items = [
            ("Game Version", cfg["game_version"]),
            ("Python", cfg["python_version"]),
            ("Pygame", cfg["pygame_version"]),
            ("Config File", os.path.abspath(CONFIG_FILE)),
            ("Display", f"{self.width}×{self.height}"),
        ]
        for label, value in info_items:
            self.txt(label, cx, y, MUTED, "small")
            self.txt(value, cx + 160, y, WHITE, "normal")
            y += 30

        y += 10
        y = self._section_header("Credits", cx, y, cw)
        credits = [
            ("Design", "Dark Slate UI System"),
            ("Engine", "Pygame / SDL2"),
            ("Studio", "219 Studios"),
        ]
        for role, name in credits:
            self.txt(role, cx, y, MUTED, "small")
            self.txt(name, cx + 120, y, WHITE, "normal")
            y += 28

    # ===================================================================
    # EVENTS
    # ===================================================================
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            # Tab clicks
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                # Tab sidebar
                tab_x = 15
                tab_y_start = 90
                tab_w = 200
                tab_h = 50
                for i in range(len(self.TABS)):
                    tr = pygame.Rect(tab_x, tab_y_start + i * (tab_h + 6), tab_w, tab_h)
                    if tr.collidepoint(e.pos):
                        self.active_tab = i
                        break

                # Save button
                save_r = pygame.Rect(self.width - 260, 16, 110, 38)
                if save_r.collidepoint(e.pos):
                    self.save()

                # Reset button
                reset_r = pygame.Rect(self.width - 140, 16, 120, 38)
                if reset_r.collidepoint(e.pos):
                    self.reset_defaults()

            # Keyboard shortcuts
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.unsaved:
                        self.save()
                    return False
                elif e.key == pygame.K_s and not self._any_text_active():
                    self.save()
                elif e.key == pygame.K_r and not self._any_text_active():
                    self.reset_defaults()
                elif e.key == pygame.K_TAB:
                    self.active_tab = (self.active_tab + 1) % len(self.TABS)
                elif e.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                    self.tg_fullscreen.value = not self.tg_fullscreen.value
                    self.unsaved = True

            # Widget events
            changed = False
            widgets = self._get_active_widgets()
            for w in widgets:
                if w.handle_event(e):
                    changed = True

            if changed:
                self.unsaved = True

        return True

    def _any_text_active(self):
        """Check if any text input is active."""
        text_inputs = [self.ti_name, self.ti_hit, self.ti_stand, self.ti_double, self.ti_split, self.ti_surrender]
        return any(ti.active for ti in text_inputs)

    def _get_active_widgets(self):
        """Return widgets for the current tab."""
        tab = self.TABS[self.active_tab]
        if tab == "Display":
            return [self.dd_resolution, self.dd_fps, self.tg_fullscreen, self.tg_vsync, self.dd_theme]
        elif tab == "Audio":
            return [self.sl_master, self.sl_music, self.sl_sfx, self.tg_muted]
        elif tab == "Gameplay":
            return [self.ti_name, self.sl_balance, self.dd_anim_speed,
                    self.tg_auto_save, self.tg_show_hints, self.tg_confirm_bets, self.tg_show_hand_value]
        elif tab == "Controls":
            return [self.ti_hit, self.ti_stand, self.ti_double, self.ti_split, self.ti_surrender]
        elif tab == "Accessibility":
            return [self.tg_colorblind, self.tg_large_text, self.tg_high_contrast, self.tg_screen_shake]
        return []


# =====================
# Main
# =====================
def main():
    pygame.init()

    # Load config for initial resolution
    config = load_config()
    res = config["display"]["resolution"]
    flags = 0
    if config["display"]["fullscreen"]:
        flags |= pygame.FULLSCREEN
    screen = pygame.display.set_mode((res[0], res[1]), flags)
    pygame.display.set_caption("Settings")
    clock = pygame.time.Clock()

    settings = SettingsScreen(screen)

    running = True
    while running:
        running = settings.handle_events()
        settings.draw()
        pygame.display.flip()
        fps = config["display"]["fps_limit"]
        clock.tick(fps if fps else 60)

    # Auto-save on exit if unsaved
    if settings.unsaved:
        settings.save()

    pygame.quit()


if __name__ == "__main__":
    main()