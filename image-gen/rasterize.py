#!/usr/bin/env python3
"""Render the control/*.html "structure" compositions to PNGs.

These PNGs are the structure input for Stability control-structure (see
generate.py). Run this once (or whenever you edit a control HTML).

Requires Playwright:
    pip install playwright && python -m playwright install chromium

Usage:
    python image-gen/rasterize.py
"""
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
CONTROL = HERE / "control"
W, H = 1280, 720

def main():
    htmls = sorted(CONTROL.glob("*.html"))
    if not htmls:
        print("no control/*.html found"); return
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(viewport={"width": W, "height": H})
        for f in htmls:
            pg.goto(f.as_uri(), wait_until="networkidle")
            pg.wait_for_timeout(300)
            out = f.with_suffix(".png")
            pg.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": W, "height": H})
            print("wrote", out.relative_to(HERE.parent))
        b.close()

if __name__ == "__main__":
    main()
