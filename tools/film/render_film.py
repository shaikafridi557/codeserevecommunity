"""Render tools/film/brand-film.htm frame by frame and build:
  assets/video/codeserve-brand-film.mp4      1920x1080, 30 fps (for social media / sharing)
  assets/video/codeserve-brand-film-720.mp4  1280x720 web version
  assets/video/codeserve-brand-film-poster.jpg poster image
Needs: a local server on :8765 serving the site root (python -m http.server 8765), Playwright + Chrome, ffmpeg.
Run:  python tools/film/render_film.py
"""
import shutil, subprocess, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
FPS, DURATION = 30, 8.5
URL = "http://localhost:8765/tools/film/brand-film.htm"
tmp = Path(tempfile.mkdtemp(prefix="film_"))
n = int(FPS * DURATION)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(URL); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
    el = pg.locator("#v")
    for i in range(n + 1):
        pg.evaluate(f"render({i / FPS})")
        el.screenshot(path=str(tmp / f"f{i:04d}.png"))
        if i % 30 == 0:
            print(f"  frame {i}/{n}", flush=True)
    b.close()

vid = ROOT / "assets/video"; vid.mkdir(parents=True, exist_ok=True)
ff = ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "f%04d.png")]
subprocess.run(ff + ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(vid / "codeserve-brand-film.mp4")], check=True)
subprocess.run(ff + ["-t", "5.8", "-vf", "scale=1280:-2", "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(vid / "codeserve-brand-film-720.mp4")], check=True)

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / f"f{int(FPS * 4.6):04d}.png"), "-vf", "scale=1280:-2", "-q:v", "3", str(vid / "codeserve-brand-film-poster.jpg")], check=True)
shutil.rmtree(tmp)
print("done:", vid)
