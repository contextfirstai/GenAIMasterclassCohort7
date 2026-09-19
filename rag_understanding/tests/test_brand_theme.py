"""
test_brand_theme.py — Context First AI brand alignment
======================================================
Guards the visual identity defined in the Context First AI Brand Guide
(Assets/Brand/BrandGuide_ContextFirstAI.md in the website repo).

These are not pixel tests. They pin the palette tokens and typefaces so a
later edit cannot quietly drift the app back off-brand.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parent.parent
CONFIG = MODULE_ROOT / ".streamlit" / "config.toml"
APP = MODULE_ROOT / "streamlit_app.py"
LAB = MODULE_ROOT / "rag_lab.py"

# ── Brand palette (Brand Guide §4) ───────────────────────────────────────────
CONTEXT_BLUE = "#41A5EE"
DEEP_SPACE = "#1A1B1E"
PURE_WHITE = "#FFFFFF"
LIGHT_BLUE = "#6BB8F2"
DARK_BLUE = "#2B8ED9"
MUTED_GRAY = "#9CA3AF"
BORDER_GRAY = "#2D2E33"

# Colours from the stock template that are not in the brand palette.
OFF_BRAND = ["#667eea", "#764ba2", "#2c3e50", "#3498db", "#e8f4fd", "#f8f9fa"]


def test_streamlit_theme_config_exists():
    assert CONFIG.is_file(), f"missing {CONFIG.relative_to(MODULE_ROOT)}"


def test_theme_uses_brand_palette():
    theme = tomllib.loads(CONFIG.read_text())["theme"]
    assert theme["base"] == "dark", "brand guide mandates dark backgrounds"
    assert theme["primaryColor"].upper() == CONTEXT_BLUE
    assert theme["backgroundColor"].upper() == DEEP_SPACE
    assert theme["textColor"].upper() == PURE_WHITE
    # Panels must be lifted off the background, not equal to it.
    assert theme["secondaryBackgroundColor"].upper() != DEEP_SPACE


def test_app_css_declares_brand_colours():
    css = APP.read_text()
    for token in (CONTEXT_BLUE, DEEP_SPACE, MUTED_GRAY, BORDER_GRAY):
        assert token in css, f"{token} absent from app CSS"


def test_app_uses_brand_typefaces():
    css = APP.read_text()
    assert "Montserrat" in css, "headings must use Montserrat (Brand Guide §5)"
    assert "Inter" in css, "body text must use Inter (Brand Guide §5)"


def test_no_off_brand_colours_remain():
    offenders: list[str] = []
    for path in (APP, LAB):
        text = path.read_text()
        for colour in OFF_BRAND:
            if re.search(re.escape(colour), text, re.IGNORECASE):
                offenders.append(f"{path.name}: {colour}")
    assert not offenders, "off-brand colours still present: " + ", ".join(offenders)


def test_charts_use_brand_colourway():
    """Plotly defaults are light-theme; charts must be themed centrally."""
    app = APP.read_text()
    assert "plotly" in app.lower(), "no central plotly theming in streamlit_app.py"
    assert CONTEXT_BLUE in app
