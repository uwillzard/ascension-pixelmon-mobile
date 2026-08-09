#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("uso: apply_fullscreen.py <Amethyst-Android>")

root = Path(sys.argv[1])

# ---------------------------------------------------------------------
# 1) ASCENSION WEB UI — v0.15
#    Fullscreen remains native, but the web UI now uses the whole
#    landscape height instead of shrinking everything and leaving a
#    giant dead area in the middle.
# ---------------------------------------------------------------------
ui = root / "app_pojavlauncher/src/main/assets/ui"
styles_path = ui / "styles.css"
index_path = ui / "index.html"

if not styles_path.is_file() or not index_path.is_file():
    raise SystemExit("[Ascension v0.15] UI overlay não encontrado no clone")

index = index_path.read_text(encoding="utf-8")
index = re.sub(
    r'<meta name="viewport" content="[^"]+">',
    '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">',
    index,
    count=1,
)
index_path.write_text(index, encoding="utf-8")

styles = styles_path.read_text(encoding="utf-8")

# Remove every experimental fullscreen block before appending the v0.15 layout.
markers = [
    "/* v0.10 — phone fullscreen fit */",
    "/* v0.11 — proportional phone fit.",
    "/* v0.12 — REAL responsive fullscreen phone layout */",
    "/* v0.15 — LANDSCAPE FULLSCREEN LAYOUT */",
]
positions = [styles.find(marker) for marker in markers if styles.find(marker) >= 0]
if positions:
    styles = styles[: min(positions)].rstrip() + "\n"

layout_css = r'''

/* v0.15 — LANDSCAPE FULLSCREEN LAYOUT */
html,body{
  width:100%!important;
  height:100%!important;
  min-width:0!important;
  min-height:0!important;
  max-width:100%!important;
  max-height:100%!important;
  margin:0!important;
  overflow:hidden!important;
}

body{overscroll-behavior:none!important}

.shell{
  display:grid!important;
  grid-template-columns:60px minmax(0,1fr)!important;
  width:100%!important;
  max-width:100%!important;
  height:100vh!important;
  height:100dvh!important;
  min-width:0!important;
  min-height:0!important;
  margin:0!important;
  overflow:hidden!important;
  zoom:1!important;
  transform:none!important;
}

.rail{
  width:60px!important;
  min-width:60px!important;
  height:100%!important;
  padding:8px 6px 7px!important;
  overflow:hidden!important;
}
.brand{
  width:39px!important;
  height:39px!important;
  padding:2px!important;
  border-radius:12px!important;
}
.rail nav{
  width:100%!important;
  margin-top:15px!important;
  gap:6px!important;
}
.rail-button{
  width:100%!important;
  min-width:0!important;
  padding:7px 2px!important;
  gap:3px!important;
  border-radius:10px!important;
  font-size:7px!important;
  line-height:1.1!important;
}
.rail-button b{font-size:16px!important;line-height:1!important}
.rail>small{font-size:6px!important;line-height:1.1!important}

main{
  display:grid!important;
  grid-template-rows:56px minmax(0,1fr) 64px 18px!important;
  width:100%!important;
  max-width:100%!important;
  height:100%!important;
  min-width:0!important;
  min-height:0!important;
  padding:0 12px 4px!important;
  overflow:hidden!important;
}

header{
  display:flex!important;
  align-items:center!important;
  justify-content:space-between!important;
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  height:56px!important;
  min-height:56px!important;
  gap:10px!important;
  overflow:hidden!important;
}
.heading{min-width:0!important}
.heading span{
  font-size:6px!important;
  letter-spacing:.18em!important;
  line-height:1!important;
}
.heading h1{
  margin:3px 0 0!important;
  font-size:16px!important;
  line-height:1.05!important;
  white-space:nowrap!important;
}
.header-actions{
  display:flex!important;
  align-items:center!important;
  justify-content:flex-end!important;
  min-width:0!important;
  gap:6px!important;
}
.chip,.nick-chip{
  flex:0 0 auto!important;
  height:39px!important;
  min-height:39px!important;
  padding:5px 8px!important;
  gap:7px!important;
  border-radius:10px!important;
  overflow:hidden!important;
}
.chip img{width:23px!important;height:23px!important}
.chip small,.nick-chip small{font-size:5px!important;line-height:1!important}
.chip strong,.nick-chip strong{font-size:7px!important;line-height:1.1!important}
.nick-chip{min-width:145px!important;max-width:175px!important}
.nick-chip img{width:26px!important;height:26px!important}
.nick-chip strong{max-width:92px!important}
.nick-chip>b{font-size:16px!important}

/* On phone-sized CSS viewports, keep only the useful profile chip. */
@media (max-width:1180px){
  .header-actions .chip{display:none!important}
}

.page{
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  min-height:0!important;
  padding:7px 0 6px!important;
  overflow:hidden!important;
}
.page.active{display:block!important}

/* HOME occupies every pixel between header and dock. */
#page-home.active{
  display:grid!important;
  grid-template-rows:minmax(0,1fr) 56px!important;
  gap:7px!important;
}

.top-grid{
  display:grid!important;
  grid-template-columns:minmax(0,1fr) 190px!important;
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  min-height:0!important;
  height:100%!important;
  gap:8px!important;
}

.hero,.status-card{
  width:100%!important;
  height:100%!important;
  min-width:0!important;
  min-height:0!important;
  max-width:100%!important;
  border-radius:14px!important;
  overflow:hidden!important;
}
.hero-img{
  width:100%!important;
  height:100%!important;
  object-fit:cover!important;
}
.hero-copy{
  width:58%!important;
  height:100%!important;
  padding:18px 18px!important;
  display:flex!important;
  flex-direction:column!important;
  align-items:flex-start!important;
  justify-content:center!important;
  min-width:0!important;
}
.badge{
  padding:4px 7px!important;
  border-radius:6px!important;
  font-size:6px!important;
  line-height:1.1!important;
}
.hero h2{
  margin:10px 0 7px!important;
  font-size:29px!important;
  line-height:.9!important;
}
.hero p{
  font-size:7px!important;
  line-height:1.2!important;
  white-space:nowrap!important;
}
.tags{
  margin-top:12px!important;
  gap:5px!important;
}
.tags span{
  padding:4px 7px!important;
  font-size:6px!important;
  line-height:1.1!important;
}

.status-card{
  display:flex!important;
  flex-direction:column!important;
  padding:12px!important;
}
.status-head small{font-size:6px!important;line-height:1!important}
.status-head h3{
  margin:3px 0 0!important;
  font-size:13px!important;
  line-height:1!important;
}
.server-orb{
  flex:0 0 42px!important;
  height:42px!important;
  min-height:42px!important;
}
.server-orb i{
  width:21px!important;
  height:21px!important;
  box-shadow:0 0 0 7px rgba(109,232,155,.06),0 0 20px rgba(54,203,114,.32)!important;
}
.status-card dl{
  margin:auto 0 0!important;
  min-width:0!important;
}
.status-card dl>div{
  min-width:0!important;
  gap:7px!important;
  padding:5px 0!important;
  align-items:flex-start!important;
}
.status-card dt{
  flex:0 0 auto!important;
  font-size:6px!important;
  line-height:1.15!important;
}
.status-card dd{
  min-width:0!important;
  max-width:118px!important;
  font-size:6px!important;
  line-height:1.15!important;
  text-align:right!important;
  overflow-wrap:anywhere!important;
  word-break:break-word!important;
}
/* Long server address gets its own line instead of being cut. */
.status-card dl>div:first-child{
  display:block!important;
}
.status-card dl>div:first-child dt,
.status-card dl>div:first-child dd{
  display:block!important;
  width:100%!important;
  max-width:100%!important;
  text-align:left!important;
}
.status-card dl>div:first-child dd{
  margin-top:3px!important;
  font-size:5.5px!important;
  overflow-wrap:anywhere!important;
}

.notice-row{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  height:56px!important;
  min-height:56px!important;
  margin:0!important;
  gap:7px!important;
}
.notice-row article{
  display:grid!important;
  grid-template-columns:24px minmax(0,1fr)!important;
  align-items:center!important;
  min-width:0!important;
  min-height:0!important;
  height:56px!important;
  padding:8px 9px!important;
  gap:7px!important;
  border-radius:11px!important;
  overflow:hidden!important;
}
.notice-row article>b{font-size:17px!important;line-height:1!important}
.notice-row small{font-size:5.5px!important;line-height:1!important}
.notice-row strong{
  margin-top:3px!important;
  font-size:8px!important;
  line-height:1.05!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.notice-row p{display:none!important}

/* Bottom area is flex, so hidden progress no longer shifts PREPARAR/JOGAR. */
.dock{
  display:flex!important;
  align-items:center!important;
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  height:64px!important;
  min-height:64px!important;
  padding:7px 0!important;
  gap:8px!important;
  overflow:hidden!important;
}
.dock-profile{
  flex:1 1 auto!important;
  min-width:0!important;
  gap:8px!important;
}
.dock-profile img{
  width:34px!important;
  height:34px!important;
  flex:0 0 34px!important;
  border-radius:9px!important;
}
.dock-profile span{min-width:0!important}
.dock-profile small{font-size:5.5px!important;line-height:1!important}
.dock-profile strong{font-size:8px!important;line-height:1.1!important}
.dock-profile em{font-size:6px!important;line-height:1.1!important}
.progress{
  flex:0 1 220px!important;
  width:min(220px,24vw)!important;
  min-width:120px!important;
}
.progress[hidden]{display:none!important}
.progress>div:first-child{font-size:5.5px!important}
.bar{height:4px!important;margin-top:4px!important}
.prepare,.play{
  flex:0 0 auto!important;
  height:42px!important;
  min-height:42px!important;
  padding:6px 11px!important;
  gap:8px!important;
  border-radius:10px!important;
  overflow:hidden!important;
}
.prepare{width:205px!important;min-width:205px!important}
.play{width:112px!important;min-width:112px!important}
.prepare>span,.play>span{font-size:14px!important;line-height:1!important}
.prepare strong,.play strong{
  font-size:8px!important;
  line-height:1.05!important;
  white-space:nowrap!important;
}
.prepare small,.play small{
  margin-top:2px!important;
  font-size:5.5px!important;
  line-height:1.05!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}

footer{
  display:flex!important;
  align-items:center!important;
  justify-content:space-between!important;
  min-width:0!important;
  height:18px!important;
  min-height:18px!important;
  padding:0!important;
  font-size:5.5px!important;
  line-height:1!important;
  overflow:hidden!important;
}
footer span{
  min-width:0!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}

/* Setup/settings pages use the same full area but may scroll internally. */
#page-setup.active,#page-settings.active{
  display:block!important;
  overflow-y:auto!important;
  overscroll-behavior:contain!important;
}
.page-title{margin-bottom:9px!important}
.page-title small{font-size:6px!important}
.page-title h2{margin:3px 0!important;font-size:18px!important}
.page-title p{font-size:7px!important}
.official{padding:4px 7px!important;font-size:6px!important}
.setup-grid,.settings-grid{gap:8px!important}
.profile-card{
  grid-template-columns:44px minmax(0,1fr) auto!important;
  gap:10px!important;
  padding:10px!important;
  border-radius:12px!important;
}
.profile-card img{width:44px!important;height:44px!important;border-radius:10px!important}
.profile-card small,.setup-card>small{font-size:5.5px!important}
.profile-card h3,.setup-card h3{font-size:10px!important}
.profile-card p,.setup-card p{font-size:7px!important}
.setup-card{min-width:0!important;min-height:84px!important;padding:11px!important;border-radius:12px!important}
.secondary{margin-top:8px!important;padding:6px 8px!important;font-size:6px!important}

/* Nick modal: fit landscape phone height without cropping buttons. */
.modal{padding:8px!important}
.modal-card{
  width:min(700px,calc(100vw - 16px))!important;
  max-height:calc(100dvh - 16px)!important;
  grid-template-columns:.72fr 1.28fr!important;
  border-radius:14px!important;
}
.modal-art{min-height:0!important}
.modal-content{
  min-height:0!important;
  padding:16px!important;
  overflow-y:auto!important;
}
.modal-content h2{margin:3px 0 8px!important;font-size:19px!important}
.warning{padding:8px!important}
.warning strong{font-size:6px!important}
.warning p{font-size:5.5px!important}
.modal-content label{margin:8px 0 4px!important;font-size:6px!important}
.nick-input input{height:34px!important;font-size:9px!important}
.rule{margin:4px 0 7px!important;font-size:5.5px!important}
.save{height:34px!important;font-size:7px!important}
.close{width:26px!important;height:26px!important;font-size:16px!important}

/* Prevent any card or row from expanding the physical viewport. */
header,.header-actions,.page,.top-grid,.hero,.status-card,.notice-row,
.notice-row article,.dock,.dock-profile,.progress,.setup-grid,.settings-grid,
.profile-card,.setup-card{
  min-width:0!important;
  max-width:100%!important;
}

/* Small/short landscape phones. */
@media (orientation:landscape) and (max-width:900px){
  .shell{grid-template-columns:54px minmax(0,1fr)!important}
  .rail{width:54px!important;min-width:54px!important;padding-left:5px!important;padding-right:5px!important}
  .brand{width:35px!important;height:35px!important}
  main{padding-left:9px!important;padding-right:9px!important}
  .top-grid{grid-template-columns:minmax(0,1fr) 170px!important}
  .hero-copy{width:61%!important;padding:15px!important}
  .hero h2{font-size:25px!important}
  .hero p{font-size:6.5px!important}
  .prepare{width:185px!important;min-width:185px!important}
  .play{width:104px!important;min-width:104px!important}
}

@media (orientation:landscape) and (max-height:430px){
  main{grid-template-rows:48px minmax(0,1fr) 56px 15px!important}
  header{height:48px!important;min-height:48px!important}
  .heading h1{font-size:14px!important}
  .nick-chip{height:34px!important;min-height:34px!important}
  #page-home.active{grid-template-rows:minmax(0,1fr) 49px!important;gap:6px!important}
  .notice-row,.notice-row article{height:49px!important;min-height:49px!important}
  .hero-copy{padding-top:12px!important;padding-bottom:12px!important}
  .hero h2{font-size:24px!important;margin-top:7px!important;margin-bottom:5px!important}
  .tags{margin-top:8px!important}
  .status-card{padding:9px!important}
  .server-orb{height:30px!important;min-height:30px!important;flex-basis:30px!important}
  .status-card dl>div{padding:3px 0!important}
  .dock{height:56px!important;min-height:56px!important;padding:5px 0!important}
  .dock-profile img{width:30px!important;height:30px!important;flex-basis:30px!important}
  .prepare,.play{height:36px!important;min-height:36px!important}
  footer{height:15px!important;min-height:15px!important;font-size:5px!important}
}
'''

styles_path.write_text(styles.rstrip() + layout_css, encoding="utf-8")

# ---------------------------------------------------------------------
# 2) NATIVE ACTIVITY: keep only the Ascension FragmentContainerView.
# ---------------------------------------------------------------------
fullscreen_layout = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="false"
    android:background="#090A0E">

    <com.kdt.mcgui.mcAccountSpinner
        android:id="@+id/account_spinner"
        android:layout_width="1dp"
        android:layout_height="1dp"
        android:visibility="gone"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <ImageButton
        android:id="@+id/setting_button"
        android:layout_width="1dp"
        android:layout_height="1dp"
        android:visibility="gone"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/container_fragment"
        android:layout_width="0dp"
        android:layout_height="0dp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />

    <com.kdt.mcgui.ProgressLayout
        android:id="@+id/progress_layout"
        android:layout_width="1dp"
        android:layout_height="1dp"
        android:visibility="gone"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""

for folder in ("layout", "layout-land"):
    path = root / f"app_pojavlauncher/src/main/res/{folder}/activity_pojav_launcher.xml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fullscreen_layout, encoding="utf-8")

# ---------------------------------------------------------------------
# 3) REAL ANDROID IMMERSIVE MODE: preserve v0.14 fullscreen behavior.
# ---------------------------------------------------------------------
launcher = root / "app_pojavlauncher/src/main/java/net/kdt/pojavlaunch/LauncherActivity.java"
text = launcher.read_text(encoding="utf-8")

if "import android.view.WindowInsets;" not in text:
    text = text.replace(
        "import android.view.View;\n",
        "import android.view.View;\n"
        "import android.view.WindowInsets;\n"
        "import android.view.WindowInsetsController;\n"
        "import android.view.WindowManager;\n",
    )

old_fs = """    @Override
    public boolean setFullscreen() {
        return false;
    }"""
new_fs = """    @Override
    public boolean setFullscreen() {
        return true;
    }"""
if old_fs in text:
    text = text.replace(old_fs, new_fs, 1)

immersive_method = """
    private void applyAscensionImmersiveMode() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                WindowManager.LayoutParams attrs = getWindow().getAttributes();
                attrs.layoutInDisplayCutoutMode =
                        WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
                getWindow().setAttributes(attrs);
            }

            View decor = getWindow().getDecorView();
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                getWindow().setDecorFitsSystemWindows(false);
                WindowInsetsController controller = decor.getWindowInsetsController();
                if (controller != null) {
                    controller.hide(
                            WindowInsets.Type.statusBars()
                                    | WindowInsets.Type.navigationBars()
                    );
                    controller.setSystemBarsBehavior(
                            WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                    );
                }
            } else {
                decor.setSystemUiVisibility(
                        View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                                | View.SYSTEM_UI_FLAG_FULLSCREEN
                                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                                | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                );
            }
        } catch (Throwable ignored) {
        }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) applyAscensionImmersiveMode();
    }

"""

if "private void applyAscensionImmersiveMode()" not in text:
    marker = "    @Override\n    protected void onCreate(Bundle savedInstanceState) {"
    if marker not in text:
        raise SystemExit("[Ascension v0.15] onCreate não encontrado")
    text = text.replace(marker, immersive_method + marker, 1)

old_create = """    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pojav_launcher);"""
new_create = """    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        applyAscensionImmersiveMode();
        setContentView(R.layout.activity_pojav_launcher);"""
if old_create in text:
    text = text.replace(old_create, new_create, 1)

old_resume = """    protected void onResume() {
        super.onResume();
        ContextExecutor.setActivity(this);"""
new_resume = """    protected void onResume() {
        super.onResume();
        applyAscensionImmersiveMode();
        ContextExecutor.setActivity(this);"""
if old_resume in text:
    text = text.replace(old_resume, new_resume, 1)

launcher.write_text(text, encoding="utf-8")
print("[Ascension v0.15] layout landscape + immersive fullscreen OK")
