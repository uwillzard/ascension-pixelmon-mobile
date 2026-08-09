#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('uso: apply_fullscreen.py <Amethyst-Android>')
root = Path(sys.argv[1])
path = root / 'app_pojavlauncher/src/main/java/net/kdt/pojavlaunch/LauncherActivity.java'
text = path.read_text(encoding='utf-8')
old = """    @Override
    public boolean setFullscreen() {
        return false;
    }"""
new = """    @Override
    public boolean setFullscreen() {
        return true;
    }"""
if new in text:
    print('[Ascension fullscreen] já aplicado')
elif old in text:
    path.write_text(text.replace(old, new, 1), encoding='utf-8')
    print('[Ascension fullscreen] OK')
else:
    raise SystemExit('[Ascension fullscreen] método setFullscreen esperado não encontrado')
