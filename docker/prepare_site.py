"""Assemble tracked client files at the URLs used by homepage.html."""
from pathlib import Path
import re
import shutil

root = Path(__file__).resolve().parent.parent
page = (root / 'homepage.html').read_text()
build = re.search(r"const BASE = '(/b/[^']+)'", page).group(1).lstrip('/')
site = root / 'site'
for source, destination in [
    ('homepage.html', 'index.html'),
    *[(name, f'{build}/{name}') for name in
      ('loader.js', 'game.js', 'io_worker.js', 'wgpu_worker.js')],
    ('data-manifest.json', 'data/manifest.json'),
    ('shader-index.json', f'{build}/shaders/index.json'),
]:
    target = site / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / source, target)
