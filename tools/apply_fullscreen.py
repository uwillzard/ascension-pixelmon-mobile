#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("uso: apply_fullscreen.py <Amethyst-Android>")

root = Path(sys.argv[1])

# ---------------------------------------------------------------------
# 1) ASCENSION WEB UI: remove the bad v0.11 zoom/width compensation and
#    replace it with a real responsive layout that NEVER exceeds 100%.
# ---------------------------------------------------------------------
ui = root / "app_pojavlauncher/src/main/assets/ui"
styles_path = ui / "styles.css"
index_path = ui / "index.html"

if not styles_path.is_file() or not index_path.is_file():
    raise SystemExit("[Ascension v0.12] UI overlay não encontrado no clone")

index = index_path.read_text(encoding="utf-8")
index = re.sub(
    r'<meta name="viewport" content="[^"]+">',
    '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">',
    index,
    count=1
)
index_path.write_text(index, encoding="utf-8")

styles = styles_path.read_text(encoding="utf-8")

# These experimental blocks were appended at the end in v0.10/v0.11.
# Delete them entirely before adding the correct layout.
markers = [
    "/* v0.10 — phone fullscreen fit */",
    "/* v0.11 — proportional phone fit.",
    "/* v0.12 — REAL responsive fullscreen phone layout */",
]
positions = [styles.find(m) for m in markers if styles.find(m) >= 0]
if positions:
    styles = styles[:min(positions)].rstrip() + "\n"

compact_css = r"""

/* v0.12 — REAL responsive fullscreen phone layout */
html,body{
  width:100%!important;
  height:100%!important;
  min-width:0!important;
  min-height:0!important;
  max-width:100%!important;
  overflow:hidden!important;
}

.shell{
  width:100%!important;
  max-width:100%!important;
  height:100vh!important;
  min-width:0!important;
  min-height:0!important;
  margin:0!important;
  grid-template-columns:48px minmax(0,1fr)!important;
  zoom:1!important;
  transform:none!important;
  overflow:hidden!important;
}

.rail{
  width:48px!important;
  min-width:48px!important;
  padding:6px 4px 5px!important;
}
.brand{
  width:31px!important;
  height:31px!important;
  padding:2px!important;
  border-radius:9px!important;
}
.rail nav{
  margin-top:10px!important;
  gap:3px!important;
}
.rail-button{
  padding:4px 1px!important;
  gap:2px!important;
  border-radius:8px!important;
  font-size:5.5px!important;
}
.rail-button b{font-size:12px!important}
.rail>small{font-size:4.5px!important}

main{
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  min-height:0!important;
  padding:0 8px 3px!important;
  overflow:hidden!important;
}

header{
  min-height:39px!important;
  height:39px!important;
  gap:6px!important;
}
.heading span{
  font-size:5px!important;
  letter-spacing:.15em!important;
}
.heading h1{
  margin:1px 0 0!important;
  font-size:12px!important;
}
.header-actions{gap:4px!important}
.chip,.nick-chip{
  height:27px!important;
  gap:4px!important;
  padding:3px 5px!important;
  border-radius:7px!important;
}
.chip img{width:16px!important;height:16px!important}
.chip small,.nick-chip small{font-size:4.5px!important}
.chip strong,.nick-chip strong{font-size:5.5px!important}
.nick-chip{min-width:103px!important}
.nick-chip img{width:18px!important;height:18px!important}
.nick-chip strong{max-width:61px!important}
.nick-chip>b{font-size:12px!important}

.page{
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  padding:6px 0 4px!important;
  overflow-x:hidden!important;
  overflow-y:auto!important;
}
.page.active{display:block!important}

.top-grid{
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  grid-template-columns:minmax(0,1fr) minmax(138px,19%)!important;
  gap:6px!important;
}

.hero,.status-card{
  width:100%!important;
  min-width:0!important;
  height:clamp(142px,43vh,185px)!important;
  min-height:0!important;
  border-radius:10px!important;
}
.hero-copy{
  width:53%!important;
  padding:11px 12px!important;
}
.badge{
  padding:3px 5px!important;
  border-radius:5px!important;
  font-size:4.5px!important;
}
.hero h2{
  margin:7px 0 4px!important;
  font-size:21px!important;
  line-height:.9!important;
}
.hero p{font-size:5.5px!important}
.tags{
  gap:3px!important;
  margin-top:8px!important;
}
.tags span{
  padding:3px 5px!important;
  font-size:4.5px!important;
}

.status-card{padding:8px!important}
.status-head small{font-size:4.5px!important}
.status-head h3{
  margin:1px 0 0!important;
  font-size:10px!important;
}
.server-orb{height:29px!important}
.server-orb i{
  width:15px!important;
  height:15px!important;
  box-shadow:0 0 0 5px rgba(109,232,155,.06),0 0 15px rgba(54,203,114,.30)!important;
}
dl>div{
  gap:5px!important;
  padding:2.5px 0!important;
}
dt,dd{font-size:4.5px!important}

.notice-row{
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:5px!important;
  margin-top:5px!important;
}
.notice-row article{
  min-width:0!important;
  min-height:41px!important;
  padding:5px!important;
  grid-template-columns:16px minmax(0,1fr)!important;
  gap:4px!important;
  border-radius:8px!important;
  overflow:hidden!important;
}
.notice-row article>b{font-size:12px!important}
.notice-row small{font-size:4.5px!important}
.notice-row strong{
  margin-top:1px!important;
  font-size:6px!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.notice-row p{
  margin:1px 0 0!important;
  font-size:4.5px!important;
  line-height:1.15!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}

.dock{
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
  grid-template-columns:minmax(110px,1fr) minmax(85px,.55fr) 86px 86px!important;
  gap:4px!important;
  padding:3px 0!important;
}
.dock-profile{
  min-width:0!important;
  gap:4px!important;
}
.dock-profile img{
  width:21px!important;
  height:21px!important;
  border-radius:6px!important;
}
.dock-profile small{font-size:4.5px!important}
.dock-profile strong{font-size:6px!important}
.dock-profile em{font-size:4.5px!important}
.progress>div:first-child{font-size:4.5px!important}
.bar{
  height:3px!important;
  margin-top:2px!important;
}
.prepare,.play{
  width:100%!important;
  min-width:0!important;
  height:28px!important;
  gap:4px!important;
  padding:3px 6px!important;
  border-radius:7px!important;
}
.prepare>span,.play>span{font-size:10px!important}
.prepare strong,.play strong{font-size:6.5px!important}
.prepare small,.play small{font-size:4.5px!important}

footer{
  padding-bottom:0!important;
  font-size:4.5px!important;
}

.page-title{margin-bottom:6px!important}
.page-title small{font-size:4.5px!important}
.page-title h2{
  margin:1px 0!important;
  font-size:14px!important;
}
.page-title p{font-size:5.5px!important}
.official{
  padding:3px 5px!important;
  font-size:4.5px!important;
}
.setup-grid,.settings-grid{gap:5px!important}
.profile-card{
  grid-template-columns:34px minmax(0,1fr) auto!important;
  gap:6px!important;
  padding:7px!important;
  border-radius:9px!important;
}
.profile-card img{
  width:34px!important;
  height:34px!important;
  border-radius:8px!important;
}
.profile-card small,.setup-card>small{font-size:4.5px!important}
.profile-card h3,.setup-card h3{font-size:8px!important}
.profile-card p,.setup-card p{font-size:5.5px!important}
.setup-card{
  min-width:0!important;
  min-height:67px!important;
  padding:8px!important;
  border-radius:9px!important;
}
.secondary{
  margin-top:6px!important;
  padding:4px 6px!important;
  font-size:4.5px!important;
}

/* Never allow any main section to make the page wider than the phone. */
header,.header-actions,.page,.top-grid,.hero,.status-card,
.notice-row,.notice-row article,.dock,.dock-profile,.progress,
.setup-grid,.settings-grid,.profile-card,.setup-card{
  min-width:0!important;
  max-width:100%!important;
}

/* On short landscape phones, keep every control visible at once. */
@media (orientation:landscape) and (max-height:460px){
  .shell{grid-template-columns:44px minmax(0,1fr)!important}
  .rail{width:44px!important;min-width:44px!important}
  header{height:35px!important;min-height:35px!important}
  .top-grid{grid-template-columns:minmax(0,1fr) 126px!important}
  .hero,.status-card{height:clamp(125px,42vh,155px)!important}
  .hero h2{font-size:18px!important}
  .notice-row article{min-height:36px!important}
  .notice-row p{display:none!important}
  .dock{grid-template-columns:minmax(100px,1fr) minmax(76px,.5fr) 78px 78px!important}
  .prepare,.play{height:25px!important}
}

/* Extra narrow CSS viewport: status still remains visible; nothing goes offscreen. */
@media (orientation:landscape) and (max-width:760px){
  .top-grid{grid-template-columns:minmax(0,1fr) 118px!important}
  .hero-copy{width:58%!important}
  .notice-row p{display:none!important}
  .dock{grid-template-columns:minmax(95px,1fr) minmax(70px,.45fr) 74px 74px!important}
}
"""

styles_path.write_text(styles.rstrip() + compact_css, encoding="utf-8")

# ---------------------------------------------------------------------
# 2) NATIVE ACTIVITY: hide the stock account/settings bar and use all area.
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
    p = root / f"app_pojavlauncher/src/main/res/{folder}/activity_pojav_launcher.xml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(fullscreen_layout, encoding="utf-8")

# ---------------------------------------------------------------------
# 3) REAL ANDROID IMMERSIVE MODE: hide top status bar + side nav bar.
# ---------------------------------------------------------------------
launcher = root / "app_pojavlauncher/src/main/java/net/kdt/pojavlaunch/LauncherActivity.java"
text = launcher.read_text(encoding="utf-8")

if "import android.view.WindowInsets;" not in text:
    text = text.replace(
        "import android.view.View;\n",
        "import android.view.View;\n"
        "import android.view.WindowInsets;\n"
        "import android.view.WindowInsetsController;\n"
        "import android.view.WindowManager;\n"
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
        raise SystemExit("[Ascension v0.12] onCreate não encontrado")
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
print("[Ascension v0.12] UI compacta + immersive fullscreen OK")
