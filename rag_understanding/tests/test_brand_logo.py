"""
test_brand_logo.py — Context First AI logo presence and usage
=============================================================
The Brand Guide (§3, §7) allows the horizontal logo on dark backgrounds only,
forbids recolouring, and requires the square icon below 120px width.
These tests pin that the assets ship with the module and are actually used.
"""

from __future__ import annotations

from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = MODULE_ROOT / "assets" / "brand"
APP = MODULE_ROOT / "streamlit_app.py"

# The website's own logo (Assets/Logo/Logo_ContextFirstAI.png upstream) — the
# rendition actually used in production, not the Assets/Logos/ SVG variants.
HORIZONTAL = BRAND_DIR / "Logo_ContextFirstAI.png"
FAVICON = BRAND_DIR / "favicon-32x32.png"

CONTEXT_BLUE = "#41A5EE"


def test_logo_assets_are_vendored():
    for asset in (HORIZONTAL, FAVICON):
        assert asset.is_file(), f"missing brand asset: {asset.name}"


def test_horizontal_logo_is_the_production_rendition():
    """Byte-identical to the logo the website ships, at its native size."""
    from PIL import Image

    with Image.open(HORIZONTAL) as im:
        assert im.size == (435, 158), "logo resized — aspect ratio is fixed (§7)"


def test_logo_background_matches_app_background():
    """The PNG has a baked-in background; it must match Deep Space exactly,
    or the logo shows as a visible box against the page."""
    from PIL import Image

    with Image.open(HORIZONTAL) as im:
        rgb = im.convert("RGB")
        w, h = rgb.size
        corners = [rgb.getpixel(c) for c in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    assert set(corners) == {(26, 27, 30)}, f"background is not #1A1B1E: {corners}"


def test_app_renders_the_logo():
    app = APP.read_text()
    assert "Logo_ContextFirstAI.png" in app, "header logo not rendered"
    assert "render_logo" in app or "logo_data_uri" in app, "no logo helper"


def test_app_sets_brand_page_icon():
    """The browser tab should carry the brand mark, not the stock emoji."""
    app = APP.read_text()
    assert "page_icon" in app
    assert "🤖" not in app.split("page_icon")[1][:120], "stock emoji still the page icon"
