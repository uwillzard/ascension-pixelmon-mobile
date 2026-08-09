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
bootstrap_path = root / "app_pojavlauncher/src/main/java/net/kdt/pojavlaunch/ascension/AscensionBootstrap.java"
downloader_path = root / "app_pojavlauncher/src/main/java/net/kdt/pojavlaunch/tasks/MinecraftDownloader.java"

if not index_path.is_file() or not styles_path.is_file():
    raise SystemExit("[Ascension v0.18] UI não encontrada")

# 1) Mantém a tela lógica aprovada na v0.17.
index = index_path.read_text(encoding="utf-8")
index = re.sub(
    r'<meta name="viewport" content="[^"]+">',
    '<meta name="viewport" content="width=780,user-scalable=no,viewport-fit=cover">',
    index,
    count=1,
)

# 2) Site + Discord no formato do modelo enviado.
old_site = '<button class="chip site" data-action="site"><img src="assets/site-ascension-icon.png"><span><small>SITE OFICIAL</small><strong>AscensionPixelmon.com.br</strong></span></button>'
new_site = '<button class="chip site" data-action="site"><img src="assets/site-ascension-icon.png"><span><small>SITE DO SERVIDOR • ONLINE</small><strong>AscensionPixelmon.com.br</strong></span><b class="chip-arrow">↗</b></button>'
if old_site in index:
    index = index.replace(old_site, new_site, 1)

old_discord = '<button class="chip discord" data-action="discord"><img src="assets/discord-icon.png"><span><small>DISCORD</small><strong>Comunidade oficial</strong></span></button>'
new_discord = '<button class="chip discord" data-action="discord"><img src="assets/discord-icon.png"><span><small>DISCORD OFICIAL</small><strong>Entrar na comunidade</strong></span><b class="chip-arrow">↗</b></button>'
if old_discord in index:
    index = index.replace(old_discord, new_discord, 1)

index = index.replace(
    '<span><small>SEU PERFIL</small><strong id="nickDisplay">Escolher Nick</strong></span>',
    '<span><small>PERFIL DE JOGADOR</small><strong id="nickDisplay">Escolher Nick</strong></span>',
    1
)
index_path.write_text(index, encoding="utf-8")

# 3) CSS final.
styles = styles_path.read_text(encoding="utf-8")
for marker in (
    "/* v0.16 - SYNCHRONIZED PHONE CANVAS */",
    "/* v0.18 - ASCENSION FINAL PHONE LAYOUT */",
):
    pos = styles.find(marker)
    if pos >= 0:
        styles = styles[:pos].rstrip() + "\n"

fit_css = r'''
/* v0.18 - ASCENSION FINAL PHONE LAYOUT */
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

html{height:100%!important}

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

/* Site + Discord + Perfil sempre visíveis. */
header{
  display:grid!important;
  grid-template-columns:184px minmax(0,1fr)!important;
  align-items:center!important;
  gap:7px!important;
  height:44px!important;
  min-height:44px!important;
  max-height:44px!important;
}

.heading{
  min-width:0!important;
  overflow:hidden!important;
}

.heading span{
  font-size:6.2px!important;
  white-space:nowrap!important;
}

.heading h1{
  margin-top:2px!important;
  font-size:16px!important;
  white-space:nowrap!important;
}

.header-actions{
  display:grid!important;
  grid-template-columns:minmax(0,1.15fr) minmax(0,1fr) 145px!important;
  align-items:center!important;
  gap:5px!important;
  width:100%!important;
  min-width:0!important;
}

.header-actions .chip,
.header-actions .nick-chip{
  display:flex!important;
  width:100%!important;
  min-width:0!important;
  max-width:none!important;
  height:36px!important;
  min-height:36px!important;
  padding:4px 6px!important;
  gap:5px!important;
  border-radius:9px!important;
  overflow:hidden!important;
}

.header-actions .chip img,
.header-actions .nick-chip img{
  flex:0 0 24px!important;
  width:24px!important;
  height:24px!important;
  border-radius:7px!important;
}

.header-actions .chip span,
.header-actions .nick-chip span{
  flex:1 1 auto!important;
  min-width:0!important;
  overflow:hidden!important;
}

.header-actions .chip small,
.header-actions .nick-chip small{
  display:block!important;
  font-size:4.7px!important;
  line-height:1.05!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}

.header-actions .chip strong,
.header-actions .nick-chip strong{
  display:block!important;
  margin-top:2px!important;
  max-width:none!important;
  font-size:6.2px!important;
  line-height:1.1!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}

.header-actions .chip-arrow{
  flex:0 0 auto!important;
  margin-left:auto!important;
  color:#8f98a4!important;
  font-size:9px!important;
}

.header-actions .nick-chip>b{
  flex:0 0 auto!important;
  margin-left:auto!important;
  font-size:12px!important;
}

/* Imagem original preservada, removendo apenas o escurecimento pesado. */
.hero-img{
  opacity:1!important;
  filter:none!important;
}

.shade{
  background:
    linear-gradient(
      90deg,
      rgba(5,9,7,.48) 0%,
      rgba(7,12,9,.30) 34%,
      rgba(7,10,8,.12) 60%,
      rgba(7,10,8,.03) 82%,
      rgba(7,10,8,0) 100%
    )!important;
}

.hero-copy{
  text-shadow:0 1px 4px rgba(0,0,0,.72)!important;
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

.progress[hidden]{display:none!important}

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
    max-height:39px!important;
  }

  .header-actions .chip,
  .header-actions .nick-chip{
    height:32px!important;
    min-height:32px!important;
  }

  .header-actions .chip img,
  .header-actions .nick-chip img{
    width:21px!important;
    height:21px!important;
    flex-basis:21px!important;
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

  .hero h2{font-size:21px!important}

  .prepare,
  .play{
    height:34px!important;
    min-height:34px!important;
  }
}
'''

styles_path.write_text(styles.rstrip() + fit_css, encoding="utf-8")

# 4) Escala de texto consistente.
if fragment_path.is_file():
    fragment = fragment_path.read_text(encoding="utf-8")
    anchor = "        settings.setLoadWithOverviewMode(true);\n"
    replacement = "        settings.setLoadWithOverviewMode(true);\n        settings.setTextZoom(100);\n"
    if "settings.setTextZoom(100);" not in fragment and anchor in fragment:
        fragment = fragment.replace(anchor, replacement, 1)
    fragment_path.write_text(fragment, encoding="utf-8")

# 5) Progresso real do downloader Minecraft -> UI Ascension.
if downloader_path.is_file():
    downloader = downloader_path.read_text(encoding="utf-8")

    if "AscensionProgressListener" not in downloader:
        pattern = re.compile(
            r'    public void startForcedDownload\(@NonNull Activity activity,.*?'
            r'\n    \}\n\n(?=    private void downloadGame)',
            re.S
        )

        replacement = r'''    public interface AscensionProgressListener {
        void onProgress(int percent, String message);
    }

    private volatile AscensionProgressListener mAscensionProgressListener;
    private volatile long mLastAscensionProgressAt;
    private volatile int mLastAscensionProgress = -1;

    public void startForcedDownload(@NonNull Activity activity,
                                    @Nullable JMinecraftVersionList.Version version,
                                    @NonNull String realVersion,
                                    @NonNull AsyncMinecraftDownloader.DoneListener listener) {
        startForcedDownload(activity, version, realVersion, listener, null);
    }

    public void startForcedDownload(@NonNull Activity activity,
                                    @Nullable JMinecraftVersionList.Version version,
                                    @NonNull String realVersion,
                                    @NonNull AsyncMinecraftDownloader.DoneListener listener,
                                    @Nullable AscensionProgressListener progressListener) {
        isOnline = Tools.isOnline(activity);
        Tools.switchDemo(false);
        mAscensionProgressListener = progressListener;
        mLastAscensionProgressAt = 0L;
        mLastAscensionProgress = -1;

        sExecutorService.execute(() -> {
            try {
                if (!isOnline) {
                    throw new IOException("Sem conexão com a internet para instalar Minecraft " + realVersion);
                }
                reportAscensionProgress(0, "Preparando arquivos do Minecraft...");
                downloadGame(activity, version, realVersion);
                reportAscensionProgress(100, "Arquivos do Minecraft verificados.");
                listener.onDownloadDone();
            } catch (Exception e) {
                listener.onDownloadFailed(e);
            } finally {
                mAscensionProgressListener = null;
                ProgressLayout.clearProgress(ProgressLayout.DOWNLOAD_MINECRAFT);
            }
        });
    }

    private void reportAscensionProgress(int percent, String message) {
        AscensionProgressListener callback = mAscensionProgressListener;
        if (callback == null) return;

        int safe = Math.max(0, Math.min(100, percent));
        long now = System.currentTimeMillis();

        if (mLastAscensionProgress >= 0 && safe < mLastAscensionProgress) {
            return;
        }

        if (safe != 100 && safe == mLastAscensionProgress && (now - mLastAscensionProgressAt) < 180L) {
            return;
        }

        if (safe != 100 && (now - mLastAscensionProgressAt) < 120L) {
            return;
        }

        mLastAscensionProgress = safe;
        mLastAscensionProgressAt = now;

        try {
            callback.onProgress(safe, message);
        } catch (Throwable ignored) {
        }
    }

'''
        downloader, count = pattern.subn(replacement, downloader, count=1)
        if count != 1:
            raise SystemExit("[Ascension v0.18] não consegui atualizar startForcedDownload")

    file_counter_line = "        int progress = (int)((dlFileCounter * 100L) / mTotalFileCount);\n"
    if file_counter_line in downloader:
        pos = downloader.find(file_counter_line)
        chunk = downloader[pos:pos + 350]
        if 'reportAscensionProgress(progress, "Baixando arquivos do Minecraft...");' not in chunk:
            downloader = downloader.replace(
                file_counter_line,
                file_counter_line + '        reportAscensionProgress(progress, "Baixando arquivos do Minecraft...");\n',
                1
            )

    size_counter_line = "        int progress = (int)((dlFileSize * 100L) / mTotalSize);\n"
    if size_counter_line in downloader:
        pos = downloader.find(size_counter_line)
        chunk = downloader[pos:pos + 350]
        if 'reportAscensionProgress(progress, "Baixando arquivos do Minecraft...");' not in chunk:
            downloader = downloader.replace(
                size_counter_line,
                size_counter_line + '        reportAscensionProgress(progress, "Baixando arquivos do Minecraft...");\n',
                1
            )

    jre_check = "        if(activity != null && !NewJREUtil.installNewJreIfNeeded(activity, verInfo)){\n"
    if jre_check in downloader and "Verificando Java 21..." not in downloader:
        downloader = downloader.replace(
            jre_check,
            '        if(activity != null) reportAscensionProgress(5, "Verificando Java 21...");\n'
            + jre_check,
            1
        )
        jre_end = '''            throw new RuntimeException(activity.getString(R.string.exception_failed_to_unpack_jre17));
        }
'''
        if jre_end in downloader:
            downloader = downloader.replace(
                jre_end,
                jre_end + '        if(activity != null) reportAscensionProgress(10, "Java 21 pronto. Preparando arquivos...");\n',
                1
            )

    downloader_path.write_text(downloader, encoding="utf-8")

# 6) Mapeia 0..100 do download para a etapa 12..35 do launcher.
if bootstrap_path.is_file():
    bootstrap = bootstrap_path.read_text(encoding="utf-8")

    if "downloadPercent, downloadMessage" not in bootstrap:
        old = '''                            @Override
                            public void onDownloadFailed(Throwable throwable) {
                                listener.onError("Falha ao instalar Minecraft 1.21.1: " + cleanMessage(throwable), throwable);
                            }
                        }
                );'''
        new = '''                            @Override
                            public void onDownloadFailed(Throwable throwable) {
                                listener.onError("Falha ao instalar Minecraft 1.21.1: " + cleanMessage(throwable), throwable);
                            }
                        },
                        (downloadPercent, downloadMessage) -> {
                            int raw = Math.max(0, Math.min(100, downloadPercent));
                            int mapped = 12 + ((raw * 23) / 100);
                            String message = (downloadMessage == null || downloadMessage.trim().isEmpty())
                                    ? "Baixando arquivos do Minecraft 1.21.1..."
                                    : downloadMessage;
                            listener.onStatus(message, mapped);
                        }
                );'''
        if old not in bootstrap:
            raise SystemExit("[Ascension v0.18] ponto do progresso Minecraft não encontrado em AscensionBootstrap")
        bootstrap = bootstrap.replace(old, new, 1)

    bootstrap = bootstrap.replace(
        'listener.onStatus("Instalando/verificando Minecraft 1.21.1 e Java 21...", 12);',
        'listener.onStatus("Preparando Java 21 e arquivos do Minecraft 1.21.1...", 12);',
        1
    )

    bootstrap_path.write_text(bootstrap, encoding="utf-8")

print("[Ascension v0.18] Site + Discord + banner claro + progresso real OK")
