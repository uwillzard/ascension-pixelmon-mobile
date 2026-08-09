#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("uso: apply_fit.py <Amethyst-Android>")

root = Path(sys.argv[1])
ui = root / "app_pojavlauncher/src/main/assets/ui"
index_path = ui / "index.html"
styles_path = ui / "styles.css"
fragment_path = root / "app_pojavlauncher/src/main/java/net/kdt/pojavlaunch/fragments/MainMenuFragment.java"

if not index_path.is_file() or not styles_path.is_file():
    raise SystemExit("[Ascension v0.16] UI não encontrada")

index = index_path.read_text(encoding="utf-8")
index = re.sub(
    r'<meta name="viewport" content="[^"]+">',
    '<meta name="viewport" content="width=780,user-scalable=no,viewport-fit=cover">',
    index,
    count=1,
)
index_path.write_text(index, encoding="utf-8")

styles = styles_path.read_text(encoding="utf-8")
marker = "/* v0.16 - SYNCHRONIZED PHONE CANVAS */"
pos = styles.find(marker)
if pos >= 0:
    styles = styles[:pos].rstrip() + "\n"

fit_css = r"""
/* v0.16 - SYNCHRONIZED PHONE CANVAS */
*{
  box-sizing:border-box!important;
  -webkit-text-size-adjust:100%!important;
  text-size-adjust:100%!important;
}

html,body{
  width:780px!important;
  min-width:780px!important;
  max-width:780px!important;
  margin:0!important;
  padding:0!important;
  overflow:hidden!important;
  background:#090a0e!important;
}

html{
  height:100%!important;
}

body{
  height:100vh!important;
  height:100dvh!important;
}

.shell{
  width:780px!important;
  min-width:780px!important;
  max-width:780px!important;
  height:100vh!important;
  height:100dvh!important;
  margin:0!important;
  grid-template-columns:46px minmax(0,1fr)!important;
  zoom:1!important;
  transform:none!important;
  overflow:hidden!important;
}

.rail{
  width:46px!important;
  min-width:46px!important;
  max-width:46px!important;
}

main{
  width:734px!important;
  min-width:0!important;
  max-width:734px!important;
  height:100%!important;
  grid-template-rows:44px minmax(0,1fr) 54px 14px!important;
  overflow:hidden!important;
}

header{
  height:44px!important;
  min-height:44px!important;
}

.page,
.top-grid,
.hero,
.status-card,
.notice-row,
.dock,
footer{
  min-width:0!important;
  max-width:100%!important;
}

#page-home.active{
  display:grid!important;
  grid-template-rows:minmax(0,1fr) 46px!important;
  gap:6px!important;
}

.top-grid{
  grid-template-columns:minmax(0,1fr) 152px!important;
  gap:6px!important;
}

.status-card{
  width:152px!important;
  min-width:152px!important;
  max-width:152px!important;
}

.notice-row{
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:6px!important;
  height:46px!important;
  min-height:46px!important;
}

.notice-row article{
  min-width:0!important;
  height:46px!important;
  min-height:46px!important;
  overflow:hidden!important;
}

.dock{
  display:flex!important;
  align-items:center!important;
  height:54px!important;
  min-height:54px!important;
  min-width:0!important;
  gap:6px!important;
  padding:5px 0!important;
  overflow:hidden!important;
}

.dock-profile{
  flex:1 1 auto!important;
  min-width:0!important;
}

.progress{
  flex:0 1 145px!important;
  min-width:0!important;
  max-width:145px!important;
}

.progress[hidden]{
  display:none!important;
}

.prepare{
  flex:0 0 178px!important;
  width:178px!important;
  min-width:178px!important;
  max-width:178px!important;
}

.play{
  flex:0 0 98px!important;
  width:98px!important;
  min-width:98px!important;
  max-width:98px!important;
}

.heading,
.header-actions,
.nick-chip,
.hero-copy,
.status-card dl,
.status-card dl>div,
.status-card dt,
.status-card dd,
.notice-row article>div,
.dock-profile span{
  min-width:0!important;
}

.status-card dd{
  overflow-wrap:anywhere!important;
  word-break:break-word!important;
}

.prepare strong,
.prepare small,
.play strong,
.play small{
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}

footer{
  height:14px!important;
  min-height:14px!important;
}

@media (max-height:340px){
  main{
    grid-template-rows:39px minmax(0,1fr) 47px 12px!important;
  }

  header{
    height:39px!important;
    min-height:39px!important;
  }

  #page-home.active{
    grid-template-rows:minmax(0,1fr) 40px!important;
  }

  .notice-row,
  .notice-row article{
    height:40px!important;
    min-height:40px!important;
  }

  .dock{
    height:47px!important;
    min-height:47px!important;
    padding:3px 0!important;
  }

  footer{
    height:12px!important;
    min-height:12px!important;
  }

  .hero h2{
    font-size:21px!important;
  }

  .prepare,
  .play{
    height:34px!important;
    min-height:34px!important;
  }
}
"""

styles_path.write_text(styles.rstrip() + fit_css, encoding="utf-8")

if fragment_path.is_file():
    fragment = fragment_path.read_text(encoding="utf-8")
    anchor = "        settings.setLoadWithOverviewMode(true);\n"
    replacement = "        settings.setLoadWithOverviewMode(true);\n        settings.setTextZoom(100);\n"
    if "settings.setTextZoom(100);" not in fragment and anchor in fragment:
        fragment = fragment.replace(anchor, replacement, 1)
    fragment_path.write_text(fragment, encoding="utf-8")

print("[Ascension v0.16] synchronized phone canvas OK")
