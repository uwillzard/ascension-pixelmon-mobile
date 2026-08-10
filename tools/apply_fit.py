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
    raise SystemExit("[Ascension v0.19] UI não encontrada")

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
    "/* v0.19 - ASCENSION FINAL PHONE LAYOUT */",
):
    pos = styles.find(marker)
    if pos >= 0:
        styles = styles[:pos].rstrip() + "\n"

fit_css = r'''
/* v0.19 - ASCENSION FINAL PHONE LAYOUT */
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

    # v0.19: NeoForge installer handoff must survive Fragment detach/recreation.
    # The old callback used requireContext() inside a posted Runnable and crashed
    # if Android detached MainMenuFragment before the Runnable executed.
    if "PREF_PENDING_NEOFORGE_INSTALLER" not in fragment:
        fields_old = """    private AscensionBootstrap bootstrap;

    private final ActivityResultLauncher<Intent> neoForgeInstallerLauncher ="""
        fields_new = """    private AscensionBootstrap bootstrap;
    private static final String PREF_PENDING_NEOFORGE_INSTALLER = "pending_neoforge_installer";
    private static final String PREF_PENDING_NEOFORGE_LAUNCH_AFTER = "pending_neoforge_launch_after";
    private boolean neoForgeInstallerLaunchInFlight;

    private final ActivityResultLauncher<Intent> neoForgeInstallerLauncher ="""
        if fields_old not in fragment:
            raise SystemExit("[Ascension v0.19] campos do MainMenuFragment não encontrados")
        fragment = fragment.replace(fields_old, fields_new, 1)

        callback_old = """            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                busy = false;
                if (bootstrap == null) bootstrap = createBootstrap();
                if (result.getResultCode() != Activity.RESULT_OK) {
                    sendEvent("error", "A instalação do NeoForge não foi concluída.", -1);
                    sendState();
                    return;
                }
                busy = true;
                sendEvent("progress", "Finalizando instalação do NeoForge...", 52);
                bootstrap.resumeAfterNeoForgeInstaller(pendingNick, pendingLaunchAfterInstaller);
            });"""
        callback_new = """            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                neoForgeInstallerLaunchInFlight = false;
                busy = false;

                if (prefs != null) {
                    if (pendingNick == null || !pendingNick.matches("^[A-Za-z0-9_]{3,16}$")) {
                        pendingNick = prefs.getString("nick", "");
                    }
                    pendingLaunchAfterInstaller = prefs.getBoolean(
                            PREF_PENDING_NEOFORGE_LAUNCH_AFTER,
                            pendingLaunchAfterInstaller
                    );
                    prefs.edit()
                            .remove(PREF_PENDING_NEOFORGE_INSTALLER)
                            .remove(PREF_PENDING_NEOFORGE_LAUNCH_AFTER)
                            .commit();
                }

                if (bootstrap == null) bootstrap = createBootstrap();

                if (result.getResultCode() != Activity.RESULT_OK) {
                    sendEvent("error", "A instalação do NeoForge não foi concluída.", -1);
                    sendState();
                    return;
                }

                busy = true;
                sendEvent("progress", "Finalizando instalação do NeoForge...", 52);
                bootstrap.resumeAfterNeoForgeInstaller(pendingNick, pendingLaunchAfterInstaller);
            });"""
        if callback_old not in fragment:
            raise SystemExit("[Ascension v0.19] callback ActivityResult do NeoForge não encontrado")
        fragment = fragment.replace(callback_old, callback_new, 1)

        resume_old = """        sendState();
    }

    @Override
    public void onDestroyView() {"""
        resume_new = """        sendState();
        launchPendingNeoForgeInstallerIfPossible();
    }

    @Override
    public void onDestroyView() {"""
        if resume_old not in fragment:
            raise SystemExit("[Ascension v0.19] onResume do MainMenuFragment não encontrado")
        fragment = fragment.replace(resume_old, resume_new, 1)

        installer_old = """            @Override
            public void onNeoForgeInstallerReady(File installer) {
                main.post(() -> {
                    Intent intent = new Intent(requireContext(), JavaGUILauncherActivity.class);
                    intent.putExtra("javaArgs", "-jar " + installer.getAbsolutePath() + " --install-client");
                    intent.putExtra("openLogOutput", false);
                    intent.putExtra("ascension_return_after_vm", true);
                    neoForgeInstallerLauncher.launch(intent);
                });
            }"""
        installer_new = """            @Override
            public void onNeoForgeInstallerReady(File installer) {
                if (installer == null || !installer.isFile()) {
                    busy = false;
                    sendEvent("error", "O instalador do NeoForge não foi encontrado.", -1);
                    sendState();
                    return;
                }

                if (prefs != null) {
                    prefs.edit()
                            .putString(PREF_PENDING_NEOFORGE_INSTALLER, installer.getAbsolutePath())
                            .putBoolean(PREF_PENDING_NEOFORGE_LAUNCH_AFTER, pendingLaunchAfterInstaller)
                            .commit();
                }

                main.post(MainMenuFragment.this::launchPendingNeoForgeInstallerIfPossible);
            }"""
        if installer_old not in fragment:
            raise SystemExit("[Ascension v0.19] onNeoForgeInstallerReady antigo não encontrado")
        fragment = fragment.replace(installer_old, installer_new, 1)

        method_anchor = """    private void launchGame(String versionId) {
"""
        lifecycle_method = """    private void launchPendingNeoForgeInstallerIfPossible() {
        if (neoForgeInstallerLaunchInFlight || prefs == null) return;
        if (!isAdded() || !isResumed()) return;

        Activity host = getActivity();
        if (host == null || host.isFinishing() || host.isDestroyed()) return;

        String installerPath = prefs.getString(PREF_PENDING_NEOFORGE_INSTALLER, "");
        if (installerPath == null || installerPath.trim().isEmpty()) return;

        File installer = new File(installerPath);
        if (!installer.isFile() || installer.length() <= 0) {
            prefs.edit()
                    .remove(PREF_PENDING_NEOFORGE_INSTALLER)
                    .remove(PREF_PENDING_NEOFORGE_LAUNCH_AFTER)
                    .commit();
            busy = false;
            sendEvent("error", "O instalador do NeoForge desapareceu. Toque em PREPARAR para tentar novamente.", -1);
            sendState();
            return;
        }

        pendingNick = prefs.getString("nick", "");
        pendingLaunchAfterInstaller = prefs.getBoolean(
                PREF_PENDING_NEOFORGE_LAUNCH_AFTER,
                pendingLaunchAfterInstaller
        );

        Intent intent = new Intent(host, JavaGUILauncherActivity.class);
        intent.putExtra("javaArgs", "-jar " + installer.getAbsolutePath() + " --install-client");
        intent.putExtra("openLogOutput", false);
        intent.putExtra("ascension_return_after_vm", true);

        try {
            neoForgeInstallerLaunchInFlight = true;
            neoForgeInstallerLauncher.launch(intent);
        } catch (Throwable t) {
            neoForgeInstallerLaunchInFlight = false;
            busy = false;
            sendEvent("error", "Falha ao abrir o instalador do NeoForge: " + cleanMessage(t), -1);
            sendState();
        }
    }

"""
        if method_anchor not in fragment:
            raise SystemExit("[Ascension v0.19] ponto para método de retomada não encontrado")
        fragment = fragment.replace(method_anchor, lifecycle_method + method_anchor, 1)

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
            raise SystemExit("[Ascension v0.19] não consegui atualizar startForcedDownload")

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
            raise SystemExit("[Ascension v0.19] ponto do progresso Minecraft não encontrado em AscensionBootstrap")
        bootstrap = bootstrap.replace(old, new, 1)

    bootstrap = bootstrap.replace(
        'listener.onStatus("Instalando/verificando Minecraft 1.21.1 e Java 21...", 12);',
        'listener.onStatus("Preparando Java 21 e arquivos do Minecraft 1.21.1...", 12);',
        1
    )

    bootstrap_path.write_text(bootstrap, encoding="utf-8")

print("[Ascension v0.19] interface preservada + NeoForge lifecycle-safe + progresso real OK")

# ---------------------------------------------------------------------
# 7) v0.20 - RAM configurável real na página Ajustes.
# ---------------------------------------------------------------------
app_js_path = ui / "app.js"

index = index_path.read_text(encoding="utf-8")
if 'id="memorySlider"' not in index:
    settings_pattern = re.compile(
        r'      <section class="page" id="page-settings">.*?'
        r'      </section>\n\n(?=      <section class="dock">)',
        re.S
    )
    settings_html = """      <section class="page" id="page-settings">
        <div class="page-title settings-title">
          <div><small>PREFERÊNCIAS</small><h2>Ajustes do jogo</h2><p>Configure a memória do Minecraft e ferramentas do launcher antes de jogar.</p></div>
        </div>
        <div class="settings-grid">
          <article class="setup-card memory-card">
            <div class="memory-head">
              <div><small>DESEMPENHO</small><h3>Memória para o Minecraft</h3><p>Para Pixelmon, recomendamos 6 GB ou mais quando o aparelho tiver memória disponível.</p></div>
              <strong id="memoryValue">— GB</strong>
            </div>
            <div class="memory-control">
              <button class="memory-step" id="memoryMinus" aria-label="Diminuir memória">−</button>
              <div class="memory-slider-shell">
                <input id="memorySlider" type="range" min="2048" max="6144" step="512" value="2048" aria-label="Memória RAM do Minecraft">
              </div>
              <button class="memory-step" id="memoryPlus" aria-label="Aumentar memória">+</button>
            </div>
            <div class="memory-scale"><span id="memoryMin">2 GB</span><span id="memoryMax">6 GB</span></div>
            <p class="memory-note" id="memoryNote">O limite máximo é calculado pelo launcher para não usar toda a RAM do Android.</p>
          </article>

          <article class="setup-card"><small>REPARAÇÃO</small><h3>Forçar download dos mods</h3><p>Na próxima preparação, o launcher ignora o hash salvo e baixa <code>mods.zip</code> novamente. A pasta atual só é removida depois que a nova passar na validação.</p><button class="secondary" id="repairButton">Preparar reparo</button></article>
          <article class="setup-card"><small>ARQUIVOS DO CLIENTE</small><h3>Config e options preservados</h3><p>Esses arquivos não são reinstalados a cada toque em Jogar, evitando sobrescrever suas preferências.</p></article>
          <article class="setup-card"><small>SERVIDOR</small><h3>Jogar.AscensionPixelmon.com.br</h3><p>Servidor oficial Ascension Pixelmon.</p><button class="secondary" id="checkServerButton">Verificar servidor</button></article>
        </div>
      </section>

"""
    index, count = settings_pattern.subn(settings_html, index, count=1)
    if count != 1:
        raise SystemExit("[Ascension v0.20] página Ajustes não encontrada")
    index_path.write_text(index, encoding="utf-8")

# CSS do controle de memória. Não altera a Home aprovada na v0.19.
styles = styles_path.read_text(encoding="utf-8")
ram_marker = "/* v0.20 - RAM SETTINGS */"
if ram_marker not in styles:
    ram_css = r"""

/* v0.20 - RAM SETTINGS */
#page-settings.active{
  padding-top:9px!important;
}
#page-settings .settings-title{
  margin-bottom:7px!important;
}
#page-settings .settings-title h2{
  font-size:18px!important;
}
#page-settings .settings-title p{
  font-size:6.5px!important;
}
#page-settings .settings-grid{
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  gap:6px!important;
}
#page-settings .setup-card{
  min-height:78px!important;
  padding:10px!important;
  border-radius:12px!important;
}
#page-settings .memory-card{
  grid-column:1/-1!important;
  min-height:118px!important;
  padding:12px!important;
  background:linear-gradient(145deg,rgba(25,28,35,.98),rgba(18,20,27,.98))!important;
  border-color:rgba(109,232,155,.13)!important;
}
.memory-head{
  display:flex!important;
  align-items:flex-start!important;
  justify-content:space-between!important;
  gap:12px!important;
}
.memory-head>div{
  min-width:0!important;
}
.memory-head h3{
  margin:3px 0 2px!important;
  font-size:11px!important;
}
.memory-head p{
  font-size:6.4px!important;
  line-height:1.35!important;
}
.memory-head>strong{
  flex:0 0 auto!important;
  color:var(--green)!important;
  font-size:15px!important;
  line-height:1!important;
  white-space:nowrap!important;
}
.memory-control{
  display:grid!important;
  grid-template-columns:29px minmax(0,1fr) 29px!important;
  align-items:center!important;
  gap:8px!important;
  margin-top:12px!important;
}
.memory-step{
  display:grid!important;
  place-items:center!important;
  width:29px!important;
  height:29px!important;
  padding:0!important;
  border:1px solid rgba(109,232,155,.18)!important;
  border-radius:9px!important;
  background:rgba(109,232,155,.07)!important;
  color:var(--green)!important;
  font-size:17px!important;
  font-weight:900!important;
}
.memory-step:disabled{
  opacity:.28!important;
}
.memory-slider-shell{
  display:flex!important;
  align-items:center!important;
  height:29px!important;
  min-width:0!important;
  padding:0 2px!important;
  touch-action:none!important;
}
#memorySlider{
  width:100%!important;
  height:24px!important;
  margin:0!important;
  padding:0!important;
  accent-color:var(--green2)!important;
  background:transparent!important;
  touch-action:none!important;
  -webkit-appearance:none!important;
  appearance:none!important;
}
#memorySlider::-webkit-slider-runnable-track{
  height:5px!important;
  border-radius:99px!important;
  background:linear-gradient(90deg,rgba(54,203,114,.82),rgba(109,232,155,.42))!important;
}
#memorySlider::-webkit-slider-thumb{
  width:16px!important;
  height:16px!important;
  margin-top:-5.5px!important;
  border:0!important;
  border-radius:50%!important;
  background:var(--green)!important;
  box-shadow:0 0 0 4px rgba(109,232,155,.10)!important;
  -webkit-appearance:none!important;
}
.memory-scale{
  display:flex!important;
  justify-content:space-between!important;
  margin:1px 37px 0!important;
  color:#626a76!important;
  font-size:5.8px!important;
}
.memory-note{
  margin:5px 37px 0!important;
  color:#79818d!important;
  font-size:5.8px!important;
  line-height:1.25!important;
}
"""
    styles_path.write_text(styles.rstrip() + ram_css, encoding="utf-8")

# JavaScript: valor, +/- e arraste do slider no touch nativo.
if not app_js_path.is_file():
    raise SystemExit("[Ascension v0.20] app.js não encontrado")

appjs = app_js_path.read_text(encoding="utf-8")
if "function renderMemory()" not in appjs:
    appjs = appjs.replace(
        "let state = {nick:'',engineReady:true,minecraftInstalled:false,neoforgeInstalled:false,prepared:false,busy:false};",
        "let state = {nick:'',engineReady:true,minecraftInstalled:false,neoforgeInstalled:false,prepared:false,busy:false,memoryMb:2048,memoryMinMb:2048,memoryMaxMb:6144};",
        1
    )

    render_anchor = "    $('#serverStatus').textContent='Online';\n  }"
    if render_anchor not in appjs:
        raise SystemExit("[Ascension v0.20] render() não encontrado")
    appjs = appjs.replace(
        render_anchor,
        "    $('#serverStatus').textContent='Online';\n    renderMemory();\n  }",
        1
    )

    funcs_anchor = "  function switchTab(tab){\n"
    memory_funcs = r"""  let ramDragging=false;

  function formatMemory(mb){
    const gb=(Number(mb)||0)/1024;
    return (Math.abs(gb-Math.round(gb))<0.001 ? String(Math.round(gb)) : gb.toFixed(1).replace('.0',''))+' GB';
  }

  function memoryBounds(){
    let min=Number(state.memoryMinMb)||2048;
    let max=Number(state.memoryMaxMb)||Math.max(min,6144);
    if(max<min) min=max;
    return {min,max};
  }

  function renderMemory(){
    const slider=$('#memorySlider');
    if(!slider) return;
    const {min,max}=memoryBounds();
    let value=Number(state.memoryMb)||min;
    value=Math.max(min,Math.min(max,value));
    slider.min=String(min);
    slider.max=String(max);
    slider.step='512';
    slider.value=String(value);
    $('#memoryValue').textContent=formatMemory(value);
    $('#memoryMin').textContent=formatMemory(min);
    $('#memoryMax').textContent=formatMemory(max);
    const note=$('#memoryNote');
    if(note){
      note.textContent=max<6144
        ? `Neste aparelho o limite seguro calculado é ${formatMemory(max)}.`
        : 'Para Pixelmon, 6 GB ou mais costuma funcionar melhor. Evite usar toda a RAM do aparelho.';
    }
    const minus=$('#memoryMinus'), plus=$('#memoryPlus');
    if(minus) minus.disabled=value<=min;
    if(plus) plus.disabled=value>=max;
  }

  function previewMemory(value){
    const {min,max}=memoryBounds();
    let v=Math.max(min,Math.min(max,Number(value)||min));
    v=Math.round(v/512)*512;
    v=Math.max(min,Math.min(max,v));
    const slider=$('#memorySlider');
    if(slider) slider.value=String(v);
    const label=$('#memoryValue');
    if(label) label.textContent=formatMemory(v);
    return v;
  }

  function saveMemory(value, showToast=true){
    const v=previewMemory(value);
    const saved=call('setMemoryMb',v);
    const finalValue=(typeof saved==='number' && saved>0) ? saved : v;
    state.memoryMb=finalValue;
    renderMemory();
    if(showToast) toast(`Memória do Minecraft: ${formatMemory(finalValue)}`,'success');
  }

  function stepMemory(direction){
    const slider=$('#memorySlider');
    const current=Number((slider && slider.value)||state.memoryMb||2048);
    saveMemory(current+(direction*1024));
  }

  function memoryValueFromViewportX(x){
    const slider=$('#memorySlider');
    if(!slider) return null;
    const rect=slider.getBoundingClientRect();
    if(rect.width<=0) return null;
    const {min,max}=memoryBounds();
    const ratio=Math.max(0,Math.min(1,(x-rect.left)/rect.width));
    return min+(max-min)*ratio;
  }

  function nativePointerDown(nx,ny){
    const x=Math.max(0,Math.min(window.innerWidth-1,nx*window.innerWidth));
    const y=Math.max(0,Math.min(window.innerHeight-1,ny*window.innerHeight));
    const el=document.elementFromPoint(x,y);
    const shell=el && el.closest ? el.closest('.memory-slider-shell') : null;
    ramDragging=!!shell;
    if(ramDragging){
      const v=memoryValueFromViewportX(x);
      if(v!==null) previewMemory(v);
    }
  }

  function nativePointerUp(nx,ny){
    if(ramDragging){
      const x=Math.max(0,Math.min(window.innerWidth-1,nx*window.innerWidth));
      const v=memoryValueFromViewportX(x);
      ramDragging=false;
      if(v!==null) saveMemory(v,false);
      return;
    }
    ramDragging=false;
  }

  function nativePointerCancel(){ ramDragging=false; }

"""
    if funcs_anchor not in appjs:
        raise SystemExit("[Ascension v0.20] ponto para funções de RAM não encontrado")
    appjs = appjs.replace(funcs_anchor, memory_funcs + funcs_anchor, 1)

    input_anchor = "    if(el.tagName === 'INPUT'){\n"
    if input_anchor not in appjs:
        raise SystemExit("[Ascension v0.20] tratamento de INPUT não encontrado")
    appjs = appjs.replace(
        input_anchor,
        "    if(el.id === 'memoryMinus'){ stepMemory(-1); return true; }\n"
        "    if(el.id === 'memoryPlus'){ stepMemory(1); return true; }\n"
        "    if(el.id === 'memorySlider'){ return true; }\n\n"
        + input_anchor,
        1
    )

    old_touch = r"""  function nativeTouch(nx, ny){
    const x = Math.max(0, Math.min(window.innerWidth - 1, nx * window.innerWidth));
    const y = Math.max(0, Math.min(window.innerHeight - 1, ny * window.innerHeight));
    const el = document.elementFromPoint(x, y);
    if(!el) return;
    if(el.id === 'nickModal'){ closeNick(); return; }
    activateNativeElement(el);
  }

  function nativeScroll(deltaRatio){
    const page = document.querySelector('.page.active');
    if(page) page.scrollTop += deltaRatio * window.innerHeight;
  }
"""
    new_touch = r"""  function nativeTouch(nx, ny){
    const x = Math.max(0, Math.min(window.innerWidth - 1, nx * window.innerWidth));
    const y = Math.max(0, Math.min(window.innerHeight - 1, ny * window.innerHeight));
    const el = document.elementFromPoint(x, y);
    const sliderHit = el && el.closest ? el.closest('.memory-slider-shell') : null;
    if(ramDragging || sliderHit){
      const v=memoryValueFromViewportX(x);
      ramDragging=false;
      if(v!==null) saveMemory(v,false);
      return;
    }
    ramDragging=false;
    if(!el) return;
    if(el.id === 'nickModal'){ closeNick(); return; }
    activateNativeElement(el);
  }

  function nativeScroll(deltaRatio,nx,ny){
    if(ramDragging){
      const x=Math.max(0,Math.min(window.innerWidth-1,(Number(nx)||0)*window.innerWidth));
      const v=memoryValueFromViewportX(x);
      if(v!==null) previewMemory(v);
      return;
    }
    const page = document.querySelector('.page.active');
    if(page) page.scrollTop += deltaRatio * window.innerHeight;
  }
"""
    if old_touch not in appjs:
        raise SystemExit("[Ascension v0.20] nativeTouch/nativeScroll antigos não encontrados")
    appjs = appjs.replace(old_touch, new_touch, 1)

    bridge_obj_old = """    nativeTouch(nx,ny){ nativeTouch(nx,ny); },
    nativeScroll(deltaRatio){ nativeScroll(deltaRatio); },"""
    bridge_obj_new = """    nativePointerDown(nx,ny){ nativePointerDown(nx,ny); },
    nativePointerUp(nx,ny){ nativePointerUp(nx,ny); },
    nativePointerCancel(){ nativePointerCancel(); },
    nativeTouch(nx,ny){ nativeTouch(nx,ny); },
    nativeScroll(deltaRatio,nx,ny){ nativeScroll(deltaRatio,nx,ny); },"""
    if bridge_obj_old not in appjs:
        raise SystemExit("[Ascension v0.20] ponte AscensionMobile não encontrada")
    appjs = appjs.replace(bridge_obj_old, bridge_obj_new, 1)

    bind_anchor = "  bindTap($('#repairButton'),()=>call('repair'));\n"
    bind_new = """  bindTap($('#memoryMinus'),()=>stepMemory(-1));
  bindTap($('#memoryPlus'),()=>stepMemory(1));
  const memorySlider=$('#memorySlider');
  if(memorySlider){
    memorySlider.addEventListener('input',()=>previewMemory(memorySlider.value));
    memorySlider.addEventListener('change',()=>saveMemory(memorySlider.value,false));
  }
""" + bind_anchor
    if bind_anchor not in appjs:
        raise SystemExit("[Ascension v0.20] bindings da UI não encontrados")
    appjs = appjs.replace(bind_anchor, bind_new, 1)

    app_js_path.write_text(appjs, encoding="utf-8")

# ---------------------------------------------------------------------
# 8) v0.20 - Ponte Android para RAM real do Pojav + arraste touch.
# ---------------------------------------------------------------------
fragment = fragment_path.read_text(encoding="utf-8")

if "import net.kdt.pojavlaunch.prefs.LauncherPreferences;" not in fragment:
    import_anchor = "import net.kdt.pojavlaunch.Tools;\n"
    if import_anchor not in fragment:
        raise SystemExit("[Ascension v0.20] import Tools não encontrado")
    fragment = fragment.replace(
        import_anchor,
        import_anchor
        + "import net.kdt.pojavlaunch.Architecture;\n"
        + "import net.kdt.pojavlaunch.prefs.LauncherPreferences;\n"
        + "import androidx.preference.PreferenceManager;\n",
        1
    )

if 'o.put("memoryMaxMb"' not in fragment:
    state_anchor = '                o.put("server", AscensionConfig.SERVER_HOST);\n'
    if state_anchor not in fragment:
        raise SystemExit("[Ascension v0.20] estado do launcher não encontrado")
    fragment = fragment.replace(
        state_anchor,
        state_anchor
        + '                o.put("memoryMb", currentMemoryMb());\n'
        + '                o.put("memoryMinMb", memoryMinMb());\n'
        + '                o.put("memoryMaxMb", memoryMaxMb());\n',
        1
    )

if "public int setMemoryMb(" not in fragment:
    bridge_anchor = "        @JavascriptInterface public void prepare() { begin(false); }\n"
    bridge_method = """        @JavascriptInterface
        public int setMemoryMb(int requestedMb) {
            int value = sanitizeMemoryMb(requestedMb);
            Context context = getContext();
            SharedPreferences memoryPrefs = LauncherPreferences.DEFAULT_PREF;
            if (memoryPrefs == null && context != null) {
                memoryPrefs = PreferenceManager.getDefaultSharedPreferences(context);
            }
            if (memoryPrefs != null) {
                memoryPrefs.edit().putInt("allocation", value).commit();
            }
            LauncherPreferences.PREF_RAM_ALLOCATION = value;
            sendState();
            return value;
        }

"""
    if bridge_anchor not in fragment:
        raise SystemExit("[Ascension v0.20] ponto para setMemoryMb não encontrado")
    fragment = fragment.replace(bridge_anchor, bridge_method + bridge_anchor, 1)

if "private int memoryMaxMb()" not in fragment:
    helper_anchor = "    private void begin(boolean launchAfter) {\n"
    helper_methods = """    private int memoryMaxMb() {
        Context context = getContext();
        int deviceRam = context == null ? 6144 : Tools.getTotalDeviceMemory(context);
        int maxRam;
        if (Architecture.is32BitsDevice() || deviceRam < 2048) {
            maxRam = Math.min(1024, deviceRam);
        } else {
            maxRam = deviceRam - (deviceRam < 3064 ? 800 : 1024);
        }
        maxRam = Math.min(16384, maxRam);
        maxRam = (maxRam / 512) * 512;
        return Math.max(512, maxRam);
    }

    private int memoryMinMb() {
        int max = memoryMaxMb();
        return Math.min(2048, max);
    }

    private int sanitizeMemoryMb(int requestedMb) {
        int min = memoryMinMb();
        int max = memoryMaxMb();
        int rounded = Math.round(requestedMb / 512f) * 512;
        return Math.max(min, Math.min(max, rounded));
    }

    private int currentMemoryMb() {
        int fallback = LauncherPreferences.PREF_RAM_ALLOCATION > 0
                ? LauncherPreferences.PREF_RAM_ALLOCATION
                : memoryMinMb();
        SharedPreferences memoryPrefs = LauncherPreferences.DEFAULT_PREF;
        Context context = getContext();
        if (memoryPrefs == null && context != null) {
            memoryPrefs = PreferenceManager.getDefaultSharedPreferences(context);
        }
        int stored = memoryPrefs == null ? fallback : memoryPrefs.getInt("allocation", fallback);
        int safe = sanitizeMemoryMb(stored);
        if (memoryPrefs != null && stored != safe) {
            memoryPrefs.edit().putInt("allocation", safe).commit();
        }
        LauncherPreferences.PREF_RAM_ALLOCATION = safe;
        return safe;
    }

"""
    if helper_anchor not in fragment:
        raise SystemExit("[Ascension v0.20] ponto para helpers de RAM não encontrado")
    fragment = fragment.replace(helper_anchor, helper_methods + helper_anchor, 1)

if "nativePointerDown(" not in fragment:
    down_old = """            if (action == MotionEvent.ACTION_DOWN) {
                down[0] = last[0] = event.getX();
                down[1] = last[1] = event.getY();
                moved[0] = false;
                return true;
            }"""
    down_new = """            if (action == MotionEvent.ACTION_DOWN) {
                down[0] = last[0] = event.getX();
                down[1] = last[1] = event.getY();
                moved[0] = false;
                if (webView.getWidth() > 0 && webView.getHeight() > 0) {
                    float nx = Math.max(0f, Math.min(1f, event.getX() / (float) webView.getWidth()));
                    float ny = Math.max(0f, Math.min(1f, event.getY() / (float) webView.getHeight()));
                    webView.evaluateJavascript(
                            "window.AscensionMobile && window.AscensionMobile.nativePointerDown(" + nx + "," + ny + ")",
                            null
                    );
                }
                return true;
            }"""
    if down_old not in fragment:
        raise SystemExit("[Ascension v0.20] ACTION_DOWN não encontrado")
    fragment = fragment.replace(down_old, down_new, 1)

    move_old = """                    float dy = event.getY() - last[1];
                    float ratio = -dy / (float) webView.getHeight();
                    String js = "window.AscensionMobile && window.AscensionMobile.nativeScroll(" + ratio + ")";
                    webView.evaluateJavascript(js, null);"""
    move_new = """                    float dy = event.getY() - last[1];
                    float ratio = -dy / (float) webView.getHeight();
                    float nx = Math.max(0f, Math.min(1f, event.getX() / (float) webView.getWidth()));
                    float ny = Math.max(0f, Math.min(1f, event.getY() / (float) webView.getHeight()));
                    String js = "window.AscensionMobile && window.AscensionMobile.nativeScroll("
                            + ratio + "," + nx + "," + ny + ")";
                    webView.evaluateJavascript(js, null);"""
    if move_old not in fragment:
        raise SystemExit("[Ascension v0.20] ACTION_MOVE não encontrado")
    fragment = fragment.replace(move_old, move_new, 1)

    up_old = """            if (action == MotionEvent.ACTION_UP) {
                if (!moved[0] && webView.getWidth() > 0 && webView.getHeight() > 0) {
                    float nx = event.getX() / (float) webView.getWidth();
                    float ny = event.getY() / (float) webView.getHeight();
                    nx = Math.max(0f, Math.min(1f, nx));
                    ny = Math.max(0f, Math.min(1f, ny));
                    String js = "window.AscensionMobile && window.AscensionMobile.nativeTouch("
                            + nx + "," + ny + ")";
                    webView.evaluateJavascript(js, null);
                }

                android.view.ViewParent p = v.getParent();"""
    up_new = """            if (action == MotionEvent.ACTION_UP) {
                if (webView.getWidth() > 0 && webView.getHeight() > 0) {
                    float nx = Math.max(0f, Math.min(1f, event.getX() / (float) webView.getWidth()));
                    float ny = Math.max(0f, Math.min(1f, event.getY() / (float) webView.getHeight()));
                    String js;
                    if (moved[0]) {
                        js = "window.AscensionMobile && window.AscensionMobile.nativePointerUp("
                                + nx + "," + ny + ")";
                    } else {
                        js = "window.AscensionMobile && window.AscensionMobile.nativeTouch("
                                + nx + "," + ny + ")";
                    }
                    webView.evaluateJavascript(js, null);
                }

                android.view.ViewParent p = v.getParent();"""
    if up_old not in fragment:
        raise SystemExit("[Ascension v0.20] ACTION_UP não encontrado")
    fragment = fragment.replace(up_old, up_new, 1)

    cancel_old = """            if (action == MotionEvent.ACTION_CANCEL) {
                android.view.ViewParent p = v.getParent();"""
    cancel_new = """            if (action == MotionEvent.ACTION_CANCEL) {
                webView.evaluateJavascript(
                        "window.AscensionMobile && window.AscensionMobile.nativePointerCancel()",
                        null
                );
                android.view.ViewParent p = v.getParent();"""
    if cancel_old not in fragment:
        raise SystemExit("[Ascension v0.20] ACTION_CANCEL não encontrado")
    fragment = fragment.replace(cancel_old, cancel_new, 1)

fragment_path.write_text(fragment, encoding="utf-8")

# ---------------------------------------------------------------------
# 9) v0.21 - Performance mobile + nome final do aplicativo.
# ---------------------------------------------------------------------

# Nome visível do APK: remove "(Debug)" sem alterar package/applicationId.
build_gradle_path = root / "app_pojavlauncher/build.gradle"
if build_gradle_path.is_file():
    gradle_text = build_gradle_path.read_text(encoding="utf-8")
    gradle_text = gradle_text.replace(
        'resValue "string", "app_name", "Ascension Pixelmon (Debug)"',
        'resValue "string", "app_name", "Ascension Pixelmon"'
    )
    gradle_text = gradle_text.replace(
        'resValue "string", "app_short_name", "Ascension Pixelmon (Debug)"',
        'resValue "string", "app_short_name", "Ascension Pixelmon"'
    )
    build_gradle_path.write_text(gradle_text, encoding="utf-8")

# ---------------------------------------------------------------------
# 9.1) Launcher mais leve: mantém o visual, mas remove efeitos caros.
# ---------------------------------------------------------------------
styles = styles_path.read_text(encoding="utf-8")
perf_marker = "/* v0.21 - MOBILE PERFORMANCE */"
if perf_marker not in styles:
    perf_css = r"""

/* v0.21 - MOBILE PERFORMANCE */
html,body,.shell{
  overscroll-behavior:none!important;
}

.modal{
  backdrop-filter:none!important;
  -webkit-backdrop-filter:none!important;
  background:rgba(0,0,0,.82)!important;
}

.modal-card{
  box-shadow:0 12px 34px rgba(0,0,0,.48)!important;
}

.brand{
  box-shadow:0 5px 15px rgba(54,203,114,.10)!important;
}

.server-orb i{
  box-shadow:
    0 0 0 6px rgba(109,232,155,.05),
    0 0 14px rgba(54,203,114,.24)!important;
}

.play{
  box-shadow:0 6px 16px rgba(54,203,114,.13)!important;
}

.toast{
  box-shadow:0 5px 18px rgba(0,0,0,.42)!important;
}

.bar i{
  transition:width .08s linear!important;
}

#memorySlider::-webkit-slider-thumb{
  box-shadow:0 0 0 2px rgba(109,232,155,.08)!important;
}

.hero-img,
.shade,
.hero-copy{
  will-change:auto!important;
}

#page-settings .performance-card{
  grid-column:1/-1!important;
  min-height:86px!important;
  padding:10px 12px!important;
  border-color:rgba(135,148,255,.12)!important;
}

.performance-head{
  display:flex!important;
  justify-content:space-between!important;
  align-items:flex-start!important;
  gap:10px!important;
}

.performance-head h3{
  margin:3px 0 2px!important;
  font-size:11px!important;
}

.performance-head p{
  margin:0!important;
  color:var(--muted)!important;
  font-size:6.2px!important;
  line-height:1.3!important;
}

.performance-value{
  flex:0 0 auto!important;
  color:var(--green)!important;
  font-size:13px!important;
  font-weight:900!important;
  white-space:nowrap!important;
}

.performance-presets{
  display:grid!important;
  grid-template-columns:repeat(4,minmax(0,1fr))!important;
  gap:5px!important;
  margin-top:9px!important;
}

.performance-preset{
  min-width:0!important;
  height:28px!important;
  padding:0 4px!important;
  border:1px solid rgba(255,255,255,.08)!important;
  border-radius:8px!important;
  background:#191c23!important;
  color:#8f96a1!important;
  font-size:5.7px!important;
  font-weight:900!important;
  white-space:nowrap!important;
}

.performance-preset.active{
  border-color:rgba(109,232,155,.30)!important;
  background:rgba(109,232,155,.10)!important;
  color:var(--green)!important;
}
"""
    styles_path.write_text(styles.rstrip() + perf_css, encoding="utf-8")

# ---------------------------------------------------------------------
# 9.2) Presets de resolução interna para Pixelmon.
# ---------------------------------------------------------------------
index = index_path.read_text(encoding="utf-8")
if 'id="resolutionValue"' not in index:
    insert_after = '''            <p class="memory-note" id="memoryNote">O limite máximo é calculado pelo launcher para não usar toda a RAM do Android.</p>
          </article>

'''
    performance_card = '''            <p class="memory-note" id="memoryNote">O limite máximo é calculado pelo launcher para não usar toda a RAM do Android.</p>
          </article>

          <article class="setup-card performance-card">
            <div class="performance-head">
              <div>
                <small>OTIMIZAÇÃO MOBILE</small>
                <h3>Resolução interna do jogo</h3>
                <p>Reduz a carga da GPU sem mudar o tamanho da interface. Menor resolução costuma dar mais FPS e menos aquecimento.</p>
              </div>
              <strong class="performance-value" id="resolutionValue">--%</strong>
            </div>
            <div class="performance-presets">
              <button class="performance-preset" id="perfSmooth">LISO · 65%</button>
              <button class="performance-preset" id="perfBalanced">EQUILIBRADO · 75%</button>
              <button class="performance-preset" id="perfQuality">QUALIDADE · 90%</button>
              <button class="performance-preset" id="perfNative">NATIVO · 100%</button>
            </div>
          </article>

'''
    if insert_after not in index:
        raise SystemExit("[Ascension v0.21] ponto da memória para inserir desempenho não encontrado")
    index = index.replace(insert_after, performance_card, 1)
    index_path.write_text(index, encoding="utf-8")

# JavaScript dos presets.
appjs = app_js_path.read_text(encoding="utf-8")
if "function renderPerformance()" not in appjs:
    appjs = appjs.replace(
        "memoryMaxMb:6144};",
        "memoryMaxMb:6144,resolutionPercent:75};",
        1
    )

    if "    renderMemory();\n  }" not in appjs:
        raise SystemExit("[Ascension v0.21] renderMemory no render() não encontrado")
    appjs = appjs.replace(
        "    renderMemory();\n  }",
        "    renderMemory();\n    renderPerformance();\n  }",
        1
    )

    perf_funcs = r"""  function renderPerformance(){
    const value=Math.max(25,Math.min(100,Number(state.resolutionPercent)||75));
    const label=$('#resolutionValue');
    if(label) label.textContent=value+'%';

    const presets=[
      ['#perfSmooth',65],
      ['#perfBalanced',75],
      ['#perfQuality',90],
      ['#perfNative',100]
    ];
    presets.forEach(([selector,preset])=>{
      const el=$(selector);
      if(!el) return;
      el.classList.toggle('active',Math.abs(value-preset)<3);
    });
  }

  function saveResolution(percent){
    let value=Math.max(25,Math.min(100,Math.round((Number(percent)||75)/5)*5));
    const saved=call('setResolutionPercent',value);
    if(typeof saved==='number' && saved>=25) value=saved;
    state.resolutionPercent=value;
    renderPerformance();
    toast(`Resolução interna: ${value}%`,'success');
  }

"""
    anchor = "  function switchTab(tab){\n"
    if anchor not in appjs:
        raise SystemExit("[Ascension v0.21] switchTab não encontrado")
    appjs = appjs.replace(anchor, perf_funcs + anchor, 1)

    input_anchor = "    if(el.id === 'memoryMinus'){ stepMemory(-1); return true; }\n"
    perf_activation = """    if(el.id === 'perfSmooth'){ saveResolution(65); return true; }
    if(el.id === 'perfBalanced'){ saveResolution(75); return true; }
    if(el.id === 'perfQuality'){ saveResolution(90); return true; }
    if(el.id === 'perfNative'){ saveResolution(100); return true; }
"""
    if input_anchor not in appjs:
        raise SystemExit("[Ascension v0.21] ativação dos controles de memória não encontrada")
    appjs = appjs.replace(input_anchor, perf_activation + input_anchor, 1)

    bind_anchor = "  bindTap($('#memoryMinus'),()=>stepMemory(-1));\n"
    perf_bindings = """  bindTap($('#perfSmooth'),()=>saveResolution(65));
  bindTap($('#perfBalanced'),()=>saveResolution(75));
  bindTap($('#perfQuality'),()=>saveResolution(90));
  bindTap($('#perfNative'),()=>saveResolution(100));
"""
    if bind_anchor not in appjs:
        raise SystemExit("[Ascension v0.21] bindings de memória não encontrados")
    appjs = appjs.replace(bind_anchor, perf_bindings + bind_anchor, 1)

    app_js_path.write_text(appjs, encoding="utf-8")

# ---------------------------------------------------------------------
# 9.3) Ponte Android: resolução real do Pojav + padrão otimizado uma vez.
# ---------------------------------------------------------------------
fragment = fragment_path.read_text(encoding="utf-8")

if 'o.put("resolutionPercent"' not in fragment:
    state_anchor = '                o.put("memoryMaxMb", memoryMaxMb());\n'
    if state_anchor not in fragment:
        raise SystemExit("[Ascension v0.21] estado de RAM não encontrado")
    fragment = fragment.replace(
        state_anchor,
        state_anchor + '                o.put("resolutionPercent", currentResolutionPercent());\n',
        1
    )

if "public int setResolutionPercent(" not in fragment:
    bridge_anchor = "        @JavascriptInterface public void prepare() { begin(false); }\n"
    bridge_method = """        @JavascriptInterface
        public int setResolutionPercent(int requestedPercent) {
            int value = sanitizeResolutionPercent(requestedPercent);
            Context context = getContext();
            SharedPreferences gamePrefs = LauncherPreferences.DEFAULT_PREF;
            if (gamePrefs == null && context != null) {
                gamePrefs = PreferenceManager.getDefaultSharedPreferences(context);
            }
            if (gamePrefs != null) {
                gamePrefs.edit().putInt("resolutionRatio", value).commit();
            }
            LauncherPreferences.PREF_SCALE_FACTOR = value / 100f;
            if (prefs != null) {
                prefs.edit().putBoolean("performance_v021_initialized", true).commit();
            }
            sendState();
            return value;
        }

"""
    if bridge_anchor not in fragment:
        raise SystemExit("[Ascension v0.21] ponto da ponte de resolução não encontrado")
    fragment = fragment.replace(bridge_anchor, bridge_method + bridge_anchor, 1)

if "private int recommendedResolutionPercent()" not in fragment:
    helper_anchor = "    private void begin(boolean launchAfter) {\n"
    helpers = """    private int sanitizeResolutionPercent(int requestedPercent) {
        int rounded = Math.round(requestedPercent / 5f) * 5;
        return Math.max(25, Math.min(100, rounded));
    }

    private int recommendedResolutionPercent() {
        Context context = getContext();
        if (context == null) return 75;

        android.util.DisplayMetrics metrics = context.getResources().getDisplayMetrics();
        int minSide = Math.min(metrics.widthPixels, metrics.heightPixels);
        int recommended;

        if (minSide <= 720) recommended = 100;
        else if (minSide <= 900) recommended = 90;
        else if (minSide <= 1080) recommended = 75;
        else if (minSide <= 1440) recommended = 65;
        else recommended = 55;

        int totalRam = Tools.getTotalDeviceMemory(context);
        if (totalRam > 0 && totalRam < 4096) recommended -= 10;
        else if (totalRam > 0 && totalRam < 6144) recommended -= 5;

        return sanitizeResolutionPercent(Math.max(50, recommended));
    }

    private int currentResolutionPercent() {
        Context context = getContext();
        SharedPreferences gamePrefs = LauncherPreferences.DEFAULT_PREF;
        if (gamePrefs == null && context != null) {
            gamePrefs = PreferenceManager.getDefaultSharedPreferences(context);
        }
        int fallback = LauncherPreferences.PREF_SCALE_FACTOR > 0f
                ? Math.round(LauncherPreferences.PREF_SCALE_FACTOR * 100f)
                : 100;
        int stored = gamePrefs == null ? fallback : gamePrefs.getInt("resolutionRatio", fallback);
        int safe = sanitizeResolutionPercent(stored);
        LauncherPreferences.PREF_SCALE_FACTOR = safe / 100f;
        return safe;
    }

    private void ensureAscensionPerformanceDefaults() {
        if (prefs == null || prefs.getBoolean("performance_v021_initialized", false)) return;

        Context context = getContext();
        SharedPreferences gamePrefs = LauncherPreferences.DEFAULT_PREF;
        if (gamePrefs == null && context != null) {
            gamePrefs = PreferenceManager.getDefaultSharedPreferences(context);
        }

        int current = currentResolutionPercent();
        int recommended = recommendedResolutionPercent();
        int selected = Math.min(current, recommended);

        if (gamePrefs != null) {
            gamePrefs.edit().putInt("resolutionRatio", selected).commit();
        }
        LauncherPreferences.PREF_SCALE_FACTOR = selected / 100f;
        prefs.edit().putBoolean("performance_v021_initialized", true).commit();
    }

"""
    if helper_anchor not in fragment:
        raise SystemExit("[Ascension v0.21] ponto para helpers de desempenho não encontrado")
    fragment = fragment.replace(helper_anchor, helpers + helper_anchor, 1)

if "ASCENSION_V021_WEBVIEW_PERFORMANCE" not in fragment:
    web_anchor = "        settings.setTextZoom(100);\n"
    web_perf = """        settings.setTextZoom(100);
        // ASCENSION_V021_WEBVIEW_PERFORMANCE
        webView.setLayerType(android.view.View.LAYER_TYPE_HARDWARE, null);
        webView.setVerticalScrollBarEnabled(false);
        webView.setHorizontalScrollBarEnabled(false);
        webView.setScrollbarFadingEnabled(true);
        webView.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);
"""
    if web_anchor not in fragment:
        raise SystemExit("[Ascension v0.21] setTextZoom não encontrado")
    fragment = fragment.replace(web_anchor, web_perf, 1)

if "ensureAscensionPerformanceDefaults();\n        webView.loadUrl" not in fragment:
    load_anchor = '        webView.loadUrl("file:///android_asset/ui/index.html");\n'
    if load_anchor not in fragment:
        raise SystemExit("[Ascension v0.21] loadUrl não encontrado")
    fragment = fragment.replace(
        load_anchor,
        '        ensureAscensionPerformanceDefaults();\n' + load_anchor,
        1
    )

fragment_path.write_text(fragment, encoding="utf-8")

print("[Ascension v0.21] app Ascension Pixelmon + launcher leve + resolução Pixelmon otimizada OK")

# ---------------------------------------------------------------------
# 10) v0.22 - Novo release Mobile + atualização segura igual ao PC.
# ---------------------------------------------------------------------
asc_config_path = root / "app_pojavlauncher/src/main/java/net/kdt/pojavlaunch/ascension/AscensionConfig.java"
updater_path = root / "app_pojavlauncher/src/main/java/net/kdt/pojavlaunch/ascension/AscensionUpdater.java"

if not asc_config_path.is_file():
    raise SystemExit("[Ascension v0.22] AscensionConfig.java não encontrado")

asc_config = asc_config_path.read_text(encoding="utf-8")

url_replacements = {
    "https://github.com/uwillzard/ascension-pixelmon-modpack/releases/download/v1.0.0/mods.zip":
        "https://github.com/uwillzard/ascension-modpack-mobile/releases/download/Mobile/mods.zip",
    "https://github.com/uwillzard/ascension-pixelmon-modpack/releases/download/v1.0.0/config.zip":
        "https://github.com/uwillzard/ascension-modpack-mobile/releases/download/Mobile/config.zip",
    "https://github.com/uwillzard/ascension-pixelmon-modpack/releases/download/v1.0.0/options.txt":
        "https://github.com/uwillzard/ascension-modpack-mobile/releases/download/Mobile/options.txt",
    "https://api.github.com/repos/uwillzard/ascension-pixelmon-modpack/releases/tags/v1.0.0":
        "https://api.github.com/repos/uwillzard/ascension-modpack-mobile/releases/tags/Mobile",
}

for old, new in url_replacements.items():
    asc_config = asc_config.replace(old, new)

if 'public static final String RELEASE_PAGE' not in asc_config:
    api_line = '    public static final String RELEASE_API = "https://api.github.com/repos/uwillzard/ascension-modpack-mobile/releases/tags/Mobile";\n'
    page_line = '    public static final String RELEASE_PAGE = "https://github.com/uwillzard/ascension-modpack-mobile/releases/tag/Mobile";\n'
    if api_line not in asc_config:
        raise SystemExit("[Ascension v0.22] RELEASE_API novo não encontrado")
    asc_config = asc_config.replace(api_line, page_line + api_line, 1)

asc_config_path.write_text(asc_config, encoding="utf-8")

if not updater_path.is_file():
    raise SystemExit("[Ascension v0.22] AscensionUpdater.java não encontrado")

updater = updater_path.read_text(encoding="utf-8")

old_method_start = '    private void installClientFilesFirstTime(File root) throws Exception {\n'
old_method_end = '    private void ensureBundledCleanMenu(File root) throws IOException {\n'
start = updater.find(old_method_start)
end = updater.find(old_method_end)

if start < 0 or end < 0 or end <= start:
    raise SystemExit("[Ascension v0.22] installClientFilesFirstTime não encontrado")

new_method = '''    private void installClientFilesFirstTime(File root) throws Exception {
        File config = new File(root, "config");
        File options = new File(root, "options.txt");

        boolean configInstalled = prefs.getBoolean("config_installed_once", false);
        boolean optionsInstalled = prefs.getBoolean("options_installed_once", false);

        if (config.isDirectory()) {
            configInstalled = true;
            prefs.edit().putBoolean("config_installed_once", true).apply();
        }
        if (options.isFile() && options.length() > 0) {
            optionsInstalled = true;
            prefs.edit().putBoolean("options_installed_once", true).apply();
        }

        if (configInstalled && optionsInstalled) {
            prefs.edit().putBoolean("client_files_installed", true).apply();
            progress("Config e options preservados.", 91);
            return;
        }

        if (!configInstalled) {
            File cfgZip = new File(root, "config.download.tmp");
            File cfgStage = new File(root, "config.stage");
            File cfgNormalized = new File(root, "config.normalized");

            deleteRecursively(cfgStage);
            deleteRecursively(cfgNormalized);
            if (cfgZip.exists()) cfgZip.delete();

            try {
                downloadFile(AscensionConfig.CONFIG_URL, cfgZip,
                        "Baixando configuração inicial", 83, 87);
                unzipSafely(cfgZip, cfgStage);

                File extracted = normalizeExtractedFolder(cfgStage, "config");
                File incoming = extracted;

                if (!incoming.equals(cfgStage)) {
                    if (!incoming.renameTo(cfgNormalized)) {
                        copyDirectory(incoming, cfgNormalized);
                    }
                    deleteRecursively(cfgStage);
                    incoming = cfgNormalized;
                }

                if (!config.exists()) {
                    if (!incoming.renameTo(config)) {
                        copyDirectory(incoming, config);
                    }
                }

                prefs.edit().putBoolean("config_installed_once", true).apply();
            } finally {
                deleteRecursively(cfgStage);
                deleteRecursively(cfgNormalized);
                if (cfgZip.exists()) cfgZip.delete();
            }
        }

        if (!optionsInstalled) {
            File optTmp = new File(root, "options.download.tmp");
            if (optTmp.exists()) optTmp.delete();

            try {
                downloadFile(AscensionConfig.OPTIONS_URL, optTmp,
                        "Baixando options.txt inicial", 88, 91);

                if (!options.exists()) {
                    replaceFile(optTmp, options);
                }

                prefs.edit().putBoolean("options_installed_once", true).apply();
            } finally {
                if (optTmp.exists()) optTmp.delete();
            }
        }

        prefs.edit()
                .putBoolean("client_files_installed", true)
                .putBoolean("config_installed_once", true)
                .putBoolean("options_installed_once", true)
                .apply();

        progress("Config e options instalados uma única vez.", 91);
    }

'''

updater = updater[:start] + new_method + updater[end:]

sync_anchor = '''        if (!gameDir.exists() && !gameDir.mkdirs()) {
            throw new IOException("Não foi possível criar a pasta do Ascension.");
        }

        progress("Verificando mods do Ascension...", 66);
'''
sync_replacement = '''        if (!gameDir.exists() && !gameDir.mkdirs()) {
            throw new IOException("Não foi possível criar a pasta do Ascension.");
        }

        deleteRecursively(new File(gameDir, "mods.stage"));
        deleteRecursively(new File(gameDir, "mods.normalized"));
        File staleModsTmp = new File(gameDir, "mods.download.tmp");
        if (staleModsTmp.exists()) staleModsTmp.delete();

        progress("Verificando atualização dos mods...", 66);
'''
if sync_anchor in updater and "Verificando atualização dos mods..." not in updater:
    updater = updater.replace(sync_anchor, sync_replacement, 1)

updater_path.write_text(updater, encoding="utf-8")

build_gradle_path = root / "app_pojavlauncher/build.gradle"
if build_gradle_path.is_file():
    gradle_text = build_gradle_path.read_text(encoding="utf-8")
    gradle_text = gradle_text.replace(
        'resValue "string", "app_name", "Ascension Pixelmon (Debug)"',
        'resValue "string", "app_name", "Ascension Pixelmon"'
    )
    gradle_text = gradle_text.replace(
        'resValue "string", "app_short_name", "Ascension Pixelmon (Debug)"',
        'resValue "string", "app_short_name", "Ascension Pixelmon"'
    )
    build_gradle_path.write_text(gradle_text, encoding="utf-8")

print("[Ascension v0.23] release uwillzard mobile + config/options uma vez + mods por SHA-256 + nome final OK")

# ---------------------------------------------------------------------
# 11) v0.25 - Perfis seguros de desempenho + correção de Pokémon invisíveis.
# ---------------------------------------------------------------------
index = index_path.read_text(encoding="utf-8")
index = index.replace(
    '<h3>Resolução interna do jogo</h3>',
    '<h3>Perfil de desempenho do Pixelmon</h3>',
    1
)
index = index.replace(
    '<p>Reduz a carga da GPU sem mudar o tamanho da interface. Menor resolução costuma dar mais FPS e menos aquecimento.</p>',
    '<p>Perfis seguros para Pixelmon: reduzem carga, travadas e aquecimento sem diminuir a distância de renderização dos Pokémon.</p>',
    1
)
index = index.replace('LISO · 65%', 'LISO · 40% / 40 FPS')
index = index.replace('EQUILIBRADO · 75%', 'EQUILIBRADO · 50% / 45 FPS')
index = index.replace('QUALIDADE · 90%', 'QUALIDADE · 65% / 50 FPS')
index = index.replace('NATIVO · 100%', 'NATIVO · 100% / 60 FPS')
index_path.write_text(index, encoding="utf-8")

styles = styles_path.read_text(encoding="utf-8")
if "/* v0.25 - SAFE PERFORMANCE PROFILES */" not in styles:
    styles += r"""

/* v0.25 - SAFE PERFORMANCE PROFILES */
.performance-preset{
  font-size:5.1px!important;
  letter-spacing:.01em!important;
}
.performance-value{
  font-size:10.5px!important;
}
"""
    styles_path.write_text(styles, encoding="utf-8")

appjs = app_js_path.read_text(encoding="utf-8")
appjs = appjs.replace(
    "memoryMaxMb:6144,resolutionPercent:75};",
    "memoryMaxMb:6144,resolutionPercent:50,performanceProfile:'balanced',performanceFps:45};",
    1
)

old_render = r"""  function renderPerformance(){
    const value=Math.max(25,Math.min(100,Number(state.resolutionPercent)||75));
    const label=$('#resolutionValue');
    if(label) label.textContent=value+'%';

    const presets=[
      ['#perfSmooth',65],
      ['#perfBalanced',75],
      ['#perfQuality',90],
      ['#perfNative',100]
    ];
    presets.forEach(([selector,preset])=>{
      const el=$(selector);
      if(!el) return;
      el.classList.toggle('active',Math.abs(value-preset)<3);
    });
  }

  function saveResolution(percent){
    let value=Math.max(25,Math.min(100,Math.round((Number(percent)||75)/5)*5));
    const saved=call('setResolutionPercent',value);
    if(typeof saved==='number' && saved>=25) value=saved;
    state.resolutionPercent=value;
    renderPerformance();
    toast(`Resolução interna: ${value}%`,'success');
  }

"""
new_render = r"""  function renderPerformance(){
    const value=Math.max(25,Math.min(100,Number(state.resolutionPercent)||50));
    const fps=Math.max(30,Number(state.performanceFps)||45);
    const profile=String(state.performanceProfile||'balanced').toLowerCase();
    const label=$('#resolutionValue');
    if(label) label.textContent=value+'% · '+fps+' FPS';

    const presets=[
      ['#perfSmooth','smooth'],
      ['#perfBalanced','balanced'],
      ['#perfQuality','quality'],
      ['#perfNative','native']
    ];
    presets.forEach(([selector,name])=>{
      const el=$(selector);
      if(!el) return;
      el.classList.toggle('active',profile===name);
    });
  }

  function applyPerformanceProfile(profile){
    const name=String(profile||'balanced').toLowerCase();
    call('setPerformanceProfile',name);
    state.performanceProfile=name;

    if(name==='smooth'){
      state.resolutionPercent=40;
      state.performanceFps=40;
    }else if(name==='quality'){
      state.resolutionPercent=65;
      state.performanceFps=50;
    }else if(name==='native'){
      state.resolutionPercent=100;
      state.performanceFps=60;
    }else{
      state.performanceProfile='balanced';
      state.resolutionPercent=50;
      state.performanceFps=45;
    }

    renderPerformance();
    const titles={smooth:'Liso',balanced:'Equilibrado',quality:'Qualidade',native:'Nativo'};
    toast(`Perfil ${titles[state.performanceProfile]||'Equilibrado'} aplicado`,'success');
  }

"""
if old_render not in appjs:
    raise SystemExit("[Ascension v0.25] funções v0.21 de desempenho não encontradas")
appjs = appjs.replace(old_render, new_render, 1)

replacements = {
    "if(el.id === 'perfSmooth'){ saveResolution(65); return true; }": "if(el.id === 'perfSmooth'){ applyPerformanceProfile('smooth'); return true; }",
    "if(el.id === 'perfBalanced'){ saveResolution(75); return true; }": "if(el.id === 'perfBalanced'){ applyPerformanceProfile('balanced'); return true; }",
    "if(el.id === 'perfQuality'){ saveResolution(90); return true; }": "if(el.id === 'perfQuality'){ applyPerformanceProfile('quality'); return true; }",
    "if(el.id === 'perfNative'){ saveResolution(100); return true; }": "if(el.id === 'perfNative'){ applyPerformanceProfile('native'); return true; }",
    "bindTap($('#perfSmooth'),()=>saveResolution(65));": "bindTap($('#perfSmooth'),()=>applyPerformanceProfile('smooth'));",
    "bindTap($('#perfBalanced'),()=>saveResolution(75));": "bindTap($('#perfBalanced'),()=>applyPerformanceProfile('balanced'));",
    "bindTap($('#perfQuality'),()=>saveResolution(90));": "bindTap($('#perfQuality'),()=>applyPerformanceProfile('quality'));",
    "bindTap($('#perfNative'),()=>saveResolution(100));": "bindTap($('#perfNative'),()=>applyPerformanceProfile('native'));",
}
for old, new in replacements.items():
    if old not in appjs:
        raise SystemExit("[Ascension v0.25] binding de perfil não encontrado: " + old)
    appjs = appjs.replace(old, new, 1)
app_js_path.write_text(appjs, encoding="utf-8")

fragment = fragment_path.read_text(encoding="utf-8")
state_anchor = '                o.put("resolutionPercent", currentResolutionPercent());\n'
if 'o.put("performanceProfile"' not in fragment:
    if state_anchor not in fragment:
        raise SystemExit("[Ascension v0.25] estado de resolução não encontrado")
    fragment = fragment.replace(
        state_anchor,
        state_anchor
        + '                o.put("performanceProfile", currentPerformanceProfile());\n'
        + '                o.put("performanceFps", performanceFps(currentPerformanceProfile()));\n',
        1
    )

bridge_anchor = "        @JavascriptInterface public void prepare() { begin(false); }\n"
if "public String setPerformanceProfile(" not in fragment:
    bridge = """        @JavascriptInterface
        public String setPerformanceProfile(String requestedProfile) {
            String profile = normalizePerformanceProfile(requestedProfile);
            applyPerformanceProfile(profile, true);
            sendState();
            return profile;
        }

"""
    if bridge_anchor not in fragment:
        raise SystemExit("[Ascension v0.25] ponte prepare não encontrada")
    fragment = fragment.replace(bridge_anchor, bridge + bridge_anchor, 1)

helper_anchor = "    private void begin(boolean launchAfter) {\n"
if "private String normalizePerformanceProfile(" not in fragment:
    helpers = r'''    private String normalizePerformanceProfile(String value) {
        if ("smooth".equalsIgnoreCase(value)) return "smooth";
        if ("quality".equalsIgnoreCase(value)) return "quality";
        if ("native".equalsIgnoreCase(value)) return "native";
        return "balanced";
    }

    private String currentPerformanceProfile() {
        if (prefs == null) return "balanced";
        return normalizePerformanceProfile(prefs.getString("performance_profile_v024", "balanced"));
    }

    private int performanceResolution(String profile) {
        switch (normalizePerformanceProfile(profile)) {
            case "smooth": return 40;
            case "quality": return 65;
            case "native": return 100;
            default: return 50;
        }
    }

    private int performanceFps(String profile) {
        switch (normalizePerformanceProfile(profile)) {
            case "smooth": return 40;
            case "quality": return 50;
            case "native": return 60;
            default: return 45;
        }
    }

    private int performanceRenderDistance(String profile) {
        switch (normalizePerformanceProfile(profile)) {
            case "smooth": return 4;
            case "quality": return 8;
            case "native": return 10;
            default: return 6;
        }
    }

    private int performanceSimulationDistance(String profile) {
        switch (normalizePerformanceProfile(profile)) {
            case "smooth": return 4;
            case "quality": return 6;
            case "native": return 8;
            default: return 4;
        }
    }

    // Pixelmon usa entidades customizadas. Não reduzimos este multiplicador,
    // pois valores como 0.5/0.75 podem fazer Pokémon desaparecerem cedo demais.
    private String performanceEntityDistance(String profile) {
        return "1.0";
    }

    private String performanceOptionValue(String key, String profile) {
        String p = normalizePerformanceProfile(profile);
        if ("maxFps".equals(key)) return Integer.toString(performanceFps(p));
        if ("renderDistance".equals(key)) return Integer.toString(performanceRenderDistance(p));
        if ("simulationDistance".equals(key)) return Integer.toString(performanceSimulationDistance(p));
        if ("entityDistanceScaling".equals(key)) return "1.0";
        if ("enableVsync".equals(key)) return "false";
        if ("particles".equals(key)) {
            if ("smooth".equals(p) || "balanced".equals(p)) return "2";
            if ("quality".equals(p)) return "1";
            return "0";
        }
        if ("mipmapLevels".equals(key)) {
            if ("smooth".equals(p)) return "0";
            if ("balanced".equals(p)) return "1";
            if ("quality".equals(p)) return "2";
            return "3";
        }
        if ("biomeBlendRadius".equals(key)) {
            if ("smooth".equals(p) || "balanced".equals(p)) return "0";
            if ("quality".equals(p)) return "1";
            return "2";
        }
        if ("graphicsMode".equals(key)) {
            if ("smooth".equals(p) || "balanced".equals(p)) return "0";
            return "1";
        }
        if ("entityShadows".equals(key)) {
            return "native".equals(p) ? "true" : "false";
        }
        if ("ao".equals(key)) {
            return ("smooth".equals(p) || "balanced".equals(p)) ? "false" : "true";
        }
        return null;
    }

    private void applyMinecraftVideoProfile(String profile) {
        File gameDir = new File(Tools.DIR_GAME_HOME, AscensionConfig.GAME_DIR_NAME);
        File options = new File(gameDir, "options.txt");
        if (!options.isFile() || options.length() <= 0) return;

        File temp = new File(gameDir, "options.performance.tmp");
        File backup = new File(gameDir, "options.performance.old");
        java.util.ArrayList<String> lines = new java.util.ArrayList<>();

        try (java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.FileReader(options))) {
            String line;
            while ((line = reader.readLine()) != null) {
                int colon = line.indexOf(':');
                if (colon > 0) {
                    String key = line.substring(0, colon);
                    String value = performanceOptionValue(key, profile);
                    if (value != null) line = key + ":" + value;
                }
                lines.add(line);
            }
        } catch (Exception ignored) {
            return;
        }

        try (java.io.BufferedWriter writer = new java.io.BufferedWriter(new java.io.FileWriter(temp, false))) {
            for (String line : lines) {
                writer.write(line);
                writer.newLine();
            }
        } catch (Exception ignored) {
            temp.delete();
            return;
        }

        if (backup.exists()) backup.delete();
        if (!options.renameTo(backup)) {
            temp.delete();
            return;
        }

        boolean committed = false;
        try {
            if (temp.renameTo(options)) committed = true;
        } finally {
            if (!committed) {
                temp.delete();
                options.delete();
                backup.renameTo(options);
            } else {
                backup.delete();
            }
        }
    }

    private void disableIrisShadersForMobile() {
        File gameDir = new File(Tools.DIR_GAME_HOME, AscensionConfig.GAME_DIR_NAME);
        File iris = new File(new File(gameDir, "config"), "iris.properties");
        if (!iris.isFile()) return;

        File temp = new File(iris.getParentFile(), "iris.properties.ascension.tmp");
        File backup = new File(iris.getParentFile(), "iris.properties.ascension.old");
        java.util.ArrayList<String> lines = new java.util.ArrayList<>();
        boolean found = false;

        try (java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.FileReader(iris))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().startsWith("enableShaders=")) {
                    line = "enableShaders=false";
                    found = true;
                }
                lines.add(line);
            }
        } catch (Exception ignored) {
            return;
        }

        if (!found) lines.add("enableShaders=false");

        try (java.io.BufferedWriter writer = new java.io.BufferedWriter(new java.io.FileWriter(temp, false))) {
            for (String line : lines) {
                writer.write(line);
                writer.newLine();
            }
        } catch (Exception ignored) {
            temp.delete();
            return;
        }

        if (backup.exists()) backup.delete();
        if (!iris.renameTo(backup)) {
            temp.delete();
            return;
        }

        boolean committed = false;
        try {
            committed = temp.renameTo(iris);
        } finally {
            if (!committed) {
                temp.delete();
                iris.delete();
                backup.renameTo(iris);
            } else {
                backup.delete();
            }
        }
    }

    private void applyPerformanceProfile(String requestedProfile, boolean persistProfile) {
        String profile = normalizePerformanceProfile(requestedProfile);
        int resolution = performanceResolution(profile);
        Context context = getContext();
        SharedPreferences gamePrefs = LauncherPreferences.DEFAULT_PREF;
        if (gamePrefs == null && context != null) {
            gamePrefs = PreferenceManager.getDefaultSharedPreferences(context);
        }

        if (gamePrefs != null) {
            // Só altera preferências seguras. Não força renderer, Turnip,
            // MobileGlues, SurfaceView ou driver gráfico do aparelho.
            gamePrefs.edit()
                    .putInt("resolutionRatio", resolution)
                    .putBoolean("sustainedPerformance", true)
                    .putBoolean("force_vsync", false)
                    .putBoolean("vsync_in_zink", true)
                    .putBoolean("dump_shaders", false)
                    .commit();
        }

        LauncherPreferences.PREF_SCALE_FACTOR = resolution / 100f;
        LauncherPreferences.PREF_SUSTAINED_PERFORMANCE = true;
        LauncherPreferences.PREF_FORCE_VSYNC = false;
        LauncherPreferences.PREF_VSYNC_IN_ZINK = true;
        LauncherPreferences.PREF_DUMP_SHADERS = false;

        if (persistProfile && prefs != null) {
            prefs.edit()
                    .putString("performance_profile_v024", profile)
                    .putBoolean("performance_v024_initialized", true)
                    .commit();
        }

        // Shaders/Iris em NeoForge 1.21.1 podem causar corrupção visual em
        // combinações específicas. No mobile priorizamos Pokémon visíveis e FPS.
        disableIrisShadersForMobile();
        applyMinecraftVideoProfile(profile);
    }

    private void ensurePerformanceProfileV024() {
        if (prefs == null) return;
        if (!prefs.getBoolean("performance_v024_initialized", false)) {
            prefs.edit()
                    .putString("performance_profile_v024", "balanced")
                    .putBoolean("performance_v024_initialized", true)
                    .commit();
        }
        applyPerformanceProfile(currentPerformanceProfile(), false);
    }

'''
    if helper_anchor not in fragment:
        raise SystemExit("[Ascension v0.25] ponto para helpers não encontrado")
    fragment = fragment.replace(helper_anchor, helpers + helper_anchor, 1)

load_anchor = '        ensureAscensionPerformanceDefaults();\n        webView.loadUrl("file:///android_asset/ui/index.html");\n'
if "ensurePerformanceProfileV024();" not in fragment:
    if load_anchor not in fragment:
        raise SystemExit("[Ascension v0.25] ponto de inicialização não encontrado")
    fragment = fragment.replace(
        load_anchor,
        '        ensureAscensionPerformanceDefaults();\n        ensurePerformanceProfileV024();\n        webView.loadUrl("file:///android_asset/ui/index.html");\n',
        1
    )

begin_anchor = '''    private void begin(boolean launchAfter) {
        String nick = prefs.getString("nick", "");
'''
if begin_anchor not in fragment:
    raise SystemExit("[Ascension v0.25] begin não encontrado")
fragment = fragment.replace(
    begin_anchor,
    '''    private void begin(boolean launchAfter) {
        applyPerformanceProfile(currentPerformanceProfile(), false);
        String nick = prefs.getString("nick", "");
''',
    1
)

launch_anchor = '''    private void launchGame(String versionId) {
        main.post(() -> {
            try {
'''
if launch_anchor not in fragment:
    raise SystemExit("[Ascension v0.25] launchGame não encontrado")
fragment = fragment.replace(
    launch_anchor,
    '''    private void launchGame(String versionId) {
        main.post(() -> {
            try {
                applyPerformanceProfile(currentPerformanceProfile(), false);
''',
    1
)

fragment_path.write_text(fragment, encoding="utf-8")
print("[Ascension v0.25] Pokemon visiveis + Iris shaders off + perfis seguros 40/50/65/100 + FPS estavel OK")


# ---------------------------------------------------------------------
# 13) v0.27 - Controles Mundo Cobblemon sem tocar no fluxo de launch.
# ---------------------------------------------------------------------
# IMPORTANTE:
# - parte da v0.25, que era a base funcional;
# - NÃO usa profile.controlFile customizado;
# - NÃO deixa falha de controle abortar o bootstrap;
# - recupera instalações que já receberam a v0.26.
import base64 as _asc_b64
import hashlib as _asc_hashlib

_asc_controls_b64 = "ewogICJtQ29udHJvbERhdGFMaXN0IjogWwogICAgewogICAgICAiYmdDb2xvciI6IDEyOTE4NDU2MzIsCiAgICAgICJjb3JuZXJSYWRpdXMiOiAzMC4wLAogICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICJkaXNwbGF5SW5NZW51IjogdHJ1ZSwKICAgICAgImR5bmFtaWNYIjogIiR7bWFyZ2lufSAqIDMgKyAocHgoNzkuMjM4MSkgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKiAyICsgKHB4KDc5LjIzODEpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IiwKICAgICAgImR5bmFtaWNZIjogIiR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gJHtoZWlnaHR9IC0gJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDI4LjU3MTQyOCwKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgLTEsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiVGVjbGFkbyIsCiAgICAgICJvcGFjaXR5IjogMC43LAogICAgICAicGFzc1RocnVFbmFibGVkIjogZmFsc2UsCiAgICAgICJzdHJva2VDb2xvciI6IC0xNjc3NzIxNiwKICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAid2lkdGgiOiA3OC40NzYxOQogICAgfSwKICAgIHsKICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAiY29ybmVyUmFkaXVzIjogMzAuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IGZhbHNlLAogICAgICAiZHluYW1pY1giOiAiMC45Nzk3MDc4ICogJHtzY3JlZW5fd2lkdGh9IC0gKHB4KDQ4Ljc2MTkwNikgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke3dpZHRofSAtICR7bWFyZ2lufSIsCiAgICAgICJkeW5hbWljWSI6ICIwLjcyMDgwNDQgKiAke3NjcmVlbl9oZWlnaHR9IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDQ5LjE0Mjg1NywKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgLTMsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiUFJJIiwKICAgICAgIm9wYWNpdHkiOiAwLjYsCiAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAic3Ryb2tlV2lkdGgiOiAzLjAsCiAgICAgICJ3aWR0aCI6IDU2Ljc2MTkwNgogICAgfSwKICAgIHsKICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAiY29ybmVyUmFkaXVzIjogMzAuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IHRydWUsCiAgICAgICJkeW5hbWljWCI6ICIwLjk3OTcwNzggKiAke3NjcmVlbl93aWR0aH0gLSAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7d2lkdGh9IC0gJHttYXJnaW59IiwKICAgICAgImR5bmFtaWNZIjogIjAuNzIwODA0NCAqICR7c2NyZWVuX2hlaWdodH0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSIsCiAgICAgICJoZWlnaHQiOiA0OS4xNDI4NTcsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiBmYWxzZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIC00LAogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwCiAgICAgIF0sCiAgICAgICJuYW1lIjogIlNFQyIsCiAgICAgICJvcGFjaXR5IjogMC42LAogICAgICAicGFzc1RocnVFbmFibGVkIjogZmFsc2UsCiAgICAgICJzdHJva2VDb2xvciI6IC0xNjc3NzIxNiwKICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAid2lkdGgiOiA1Ni43NjE5MDYKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiB0cnVlLAogICAgICAiZHluYW1pY1giOiAiJHttYXJnaW59ICogMyArIChweCg3OS4yMzgxKSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAqIDIgLSAke3dpZHRofSAtICR7bWFyZ2lufSIsCiAgICAgICJkeW5hbWljWSI6ICIke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDI4LjU3MTQyOCwKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgLTUsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiTW91c2UiLAogICAgICAib3BhY2l0eSI6IDAuNywKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTY3NzcyMTYsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNzguNDc2MTkKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiB0cnVlLAogICAgICAiZHluYW1pY1giOiAiJHttYXJnaW59ICogNSArIChweCg3OS4yMzgxKSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAqIDQiLAogICAgICAiZHluYW1pY1kiOiAiJHttYXJnaW59ICsgKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAke2hlaWdodH0gLSAke21hcmdpbn0iLAogICAgICAiaGVpZ2h0IjogMjguNTcxNDI4LAogICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgImlzVG9nZ2xlIjogZmFsc2UsCiAgICAgICJrZXljb2RlcyI6IFsKICAgICAgICAtMTAsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiU0IiLAogICAgICAib3BhY2l0eSI6IDAuNywKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTY3NzcyMTYsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNzguNDc2MTkKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiB0cnVlLAogICAgICAiZHluYW1pY1giOiAiJHttYXJnaW59ICogMyArIChweCg3OS4yMzgxKSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAqIDIgLSAke3dpZHRofSAtICR7bWFyZ2lufSIsCiAgICAgICJkeW5hbWljWSI6ICIke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gJHtoZWlnaHR9IC0gJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDI4LjU3MTQyOCwKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgMjkyLAogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwCiAgICAgIF0sCiAgICAgICJuYW1lIjogIkYzIiwKICAgICAgIm9wYWNpdHkiOiAwLjcsCiAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAic3Ryb2tlV2lkdGgiOiAzLjAsCiAgICAgICJ3aWR0aCI6IDc4LjQ3NjE5CiAgICB9LAogICAgewogICAgICAiYmdDb2xvciI6IDEyOTE4NDU2MzIsCiAgICAgICJjb3JuZXJSYWRpdXMiOiAzMC4wLAogICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICJkaXNwbGF5SW5NZW51IjogdHJ1ZSwKICAgICAgImR5bmFtaWNYIjogIiR7bWFyZ2lufSIsCiAgICAgICJkeW5hbWljWSI6ICIke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAke2hlaWdodH0gLSAke21hcmdpbn0iLAogICAgICAiaGVpZ2h0IjogMjguNTcxNDI4LAogICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgImlzVG9nZ2xlIjogZmFsc2UsCiAgICAgICJrZXljb2RlcyI6IFsKICAgICAgICAyNTYsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiRVNDIiwKICAgICAgIm9wYWNpdHkiOiAwLjcsCiAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAic3Ryb2tlV2lkdGgiOiAzLjAsCiAgICAgICJ3aWR0aCI6IDc4LjQ3NjE5CiAgICB9LAogICAgewogICAgICAiYmdDb2xvciI6IDEyOTE4NDU2MzIsCiAgICAgICJjb3JuZXJSYWRpdXMiOiAzMC4wLAogICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICJkaXNwbGF5SW5NZW51IjogdHJ1ZSwKICAgICAgImR5bmFtaWNYIjogIiR7bWFyZ2lufSAqIDMgKyAocHgoNzkuMjM4MSkgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKiAyIiwKICAgICAgImR5bmFtaWNZIjogIiR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gJHtoZWlnaHR9IC0gJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDI4LjU3MTQyOCwKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgODQsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiQ2hhdCIsCiAgICAgICJvcGFjaXR5IjogMC43LAogICAgICAicGFzc1RocnVFbmFibGVkIjogZmFsc2UsCiAgICAgICJzdHJva2VDb2xvciI6IC0xNjc3NzIxNiwKICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAid2lkdGgiOiA3OC40NzYxOQogICAgfSwKICAgIHsKICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAiY29ybmVyUmFkaXVzIjogMzAuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IHRydWUsCiAgICAgICJkeW5hbWljWCI6ICIke21hcmdpbn0gKiAzICsgKHB4KDc5LjIzODEpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICogMiArIChweCg3OC40NzYxOSkgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0iLAogICAgICAiZHluYW1pY1kiOiAiJHttYXJnaW59ICsgKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoMjguNjY2NjY2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDI4LjY2NjY2NikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSIsCiAgICAgICJoZWlnaHQiOiAyOC41NzE0MjgsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiB0cnVlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgMjU4LAogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwCiAgICAgIF0sCiAgICAgICJuYW1lIjogIlRhYiIsCiAgICAgICJvcGFjaXR5IjogMC43LAogICAgICAicGFzc1RocnVFbmFibGVkIjogZmFsc2UsCiAgICAgICJzdHJva2VDb2xvciI6IC0xNjc3NzIxNiwKICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAid2lkdGgiOiA3OC40NzYxOQogICAgfSwKICAgIHsKICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAiY29ybmVyUmFkaXVzIjogMzAuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IHRydWUsCiAgICAgICJkeW5hbWljWCI6ICIke21hcmdpbn0iLAogICAgICAiZHluYW1pY1kiOiAiJHttYXJnaW59ICsgKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0iLAogICAgICAiaGVpZ2h0IjogMjguNTcxNDI4LAogICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgImlzVG9nZ2xlIjogZmFsc2UsCiAgICAgICJrZXljb2RlcyI6IFsKICAgICAgICAyOTQsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiRjUiLAogICAgICAib3BhY2l0eSI6IDAuNywKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTY3NzcyMTYsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNzguNDc2MTkKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiB0cnVlLAogICAgICAiZHluYW1pY1giOiAiMC45Nzk3MDc4ICogJHtzY3JlZW5fd2lkdGh9IC0gKHB4KDQ4Ljc2MTkwNikgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke3dpZHRofSAtICR7bWFyZ2lufSIsCiAgICAgICJkeW5hbWljWSI6ICIwLjcyMDgwNDQgKiAke3NjcmVlbl9oZWlnaHR9IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDQ5LjE0Mjg1NywKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgNjksCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiSW52IiwKICAgICAgIm9wYWNpdHkiOiAwLjYsCiAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAic3Ryb2tlV2lkdGgiOiAzLjAsCiAgICAgICJ3aWR0aCI6IDU2Ljc2MTkwNgogICAgfSwKICAgIHsKICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAiY29ybmVyUmFkaXVzIjogMzAuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IHRydWUsCiAgICAgICJkeW5hbWljWCI6ICIwLjk3OTcwNzggKiAke3NjcmVlbl93aWR0aH0gLSAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtIChweCg1Ny4xNDI4NTcpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59IC0gKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg1Ny4xNDI4NTcpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg1Ny4xNDI4NTcpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gKyAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSIsCiAgICAgICJkeW5hbWljWSI6ICIwLjcyMDgwNDQgKiAke3NjcmVlbl9oZWlnaHR9IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0iLAogICAgICAiaGVpZ2h0IjogNDkuMTQyODU3LAogICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgImlzVG9nZ2xlIjogdHJ1ZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIDM0MCwKICAgICAgICAwLAogICAgICAgIDAsCiAgICAgICAgMAogICAgICBdLAogICAgICAibmFtZSI6ICJTSElGVCIsCiAgICAgICJvcGFjaXR5IjogMC42LAogICAgICAicGFzc1RocnVFbmFibGVkIjogZmFsc2UsCiAgICAgICJzdHJva2VDb2xvciI6IC0xNjc3NzIxNiwKICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAid2lkdGgiOiA1Ni43NjE5MDYKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMzM1NTQ0MzIwLAogICAgICAiY29ybmVyUmFkaXVzIjogNjAuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IGZhbHNlLAogICAgICAiZHluYW1pY1giOiAiMC44MzA0MjgwNiAqICR7c2NyZWVuX3dpZHRofSAtICR7d2lkdGh9IiwKICAgICAgImR5bmFtaWNZIjogIjAuNzg3NzA2MiAqICR7c2NyZWVuX2hlaWdodH0gLSAke2hlaWdodH0iLAogICAgICAiaGVpZ2h0IjogNzIuMCwKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgMzIsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAi4qybIiwKICAgICAgIm9wYWNpdHkiOiAwLjU5LAogICAgICAicGFzc1RocnVFbmFibGVkIjogZmFsc2UsCiAgICAgICJzdHJva2VDb2xvciI6IC0xNjc3NzIxNiwKICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAid2lkdGgiOiA3Mi4wCiAgICB9LAogICAgewogICAgICAiYmdDb2xvciI6IDEyOTE4NDU2MzIsCiAgICAgICJjb3JuZXJSYWRpdXMiOiAzMC4wLAogICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICJkaXNwbGF5SW5NZW51IjogZmFsc2UsCiAgICAgICJkeW5hbWljWCI6ICIwLjk3OTcwNzggKiAke3NjcmVlbl93aWR0aH0gLSAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSIsCiAgICAgICJkeW5hbWljWSI6ICIwLjcyMDgwNDQgKiAke3NjcmVlbl9oZWlnaHR9IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0iLAogICAgICAiaGVpZ2h0IjogNDguMzgwOTUsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiBmYWxzZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIDI2NCwKICAgICAgICAwLAogICAgICAgIDAsCiAgICAgICAgMAogICAgICBdLAogICAgICAibmFtZSI6ICLilrwiLAogICAgICAib3BhY2l0eSI6IDAuNiwKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTY3NzcyMTYsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNDguMzgwOTUKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiBmYWxzZSwKICAgICAgImR5bmFtaWNYIjogIjAuOTc5NzA3OCAqICR7c2NyZWVuX3dpZHRofSAtIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIiwKICAgICAgImR5bmFtaWNZIjogIjAuNzIwODA0NCAqICR7c2NyZWVuX2hlaWdodH0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0iLAogICAgICAiaGVpZ2h0IjogNDguMzgwOTUsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiBmYWxzZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIDgyLAogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwCiAgICAgIF0sCiAgICAgICJuYW1lIjogIlIiLAogICAgICAib3BhY2l0eSI6IDAuNiwKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTY3NzcyMTYsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNDguMzgwOTUKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiBmYWxzZSwKICAgICAgImR5bmFtaWNYIjogIjAuOTc5NzA3OCAqICR7c2NyZWVuX3dpZHRofSAtIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIiwKICAgICAgImR5bmFtaWNZIjogIjAuNzIwODA0NCAqICR7c2NyZWVuX2hlaWdodH0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC42NjY2NjgpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNjY2NjY4KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDQ4LjM4MDk1LAogICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgImlzVG9nZ2xlIjogZmFsc2UsCiAgICAgICJrZXljb2RlcyI6IFsKICAgICAgICAyNjUsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAi4payIiwKICAgICAgIm9wYWNpdHkiOiAwLjYsCiAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAic3Ryb2tlV2lkdGgiOiAzLjAsCiAgICAgICJ3aWR0aCI6IDQ4LjM4MDk1CiAgICB9LAogICAgewogICAgICAiYmdDb2xvciI6IDEyOTE4NDU2MzIsCiAgICAgICJjb3JuZXJSYWRpdXMiOiAzMC4wLAogICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICJkaXNwbGF5SW5NZW51IjogZmFsc2UsCiAgICAgICJkeW5hbWljWCI6ICIwLjk3OTcwNzggKiAke3NjcmVlbl93aWR0aH0gLSAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSIsCiAgICAgICJkeW5hbWljWSI6ICIwLjcyMDgwNDQgKiAke3NjcmVlbl9oZWlnaHR9IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAke2hlaWdodH0gLSAke21hcmdpbn0iLAogICAgICAiaGVpZ2h0IjogNDguMzgwOTUsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiBmYWxzZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIDc3LAogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwCiAgICAgIF0sCiAgICAgICJuYW1lIjogIm0iLAogICAgICAib3BhY2l0eSI6IDAuNiwKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTU5MjI0MjEsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNDguMzgwOTUKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiBmYWxzZSwKICAgICAgImR5bmFtaWNYIjogIjAuOTc5NzA3OCAqICR7c2NyZWVuX3dpZHRofSAtIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gLSAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg1Ny4xNDI4NTcpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg1Ny4xNDI4NTcpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSIsCiAgICAgICJkeW5hbWljWSI6ICIwLjcyMDgwNDQgKiAke3NjcmVlbl9oZWlnaHR9IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0iLAogICAgICAiaGVpZ2h0IjogNDkuMTQyODU3LAogICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgImlzVG9nZ2xlIjogdHJ1ZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIDM0MSwKICAgICAgICAwLAogICAgICAgIDAsCiAgICAgICAgMAogICAgICBdLAogICAgICAibmFtZSI6ICJDVFJMIiwKICAgICAgIm9wYWNpdHkiOiAwLjYsCiAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAic3Ryb2tlV2lkdGgiOiAzLjAsCiAgICAgICJ3aWR0aCI6IDU2Ljc2MTkwNgogICAgfSwKICAgIHsKICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAiY29ybmVyUmFkaXVzIjogMzEuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IHRydWUsCiAgICAgICJkeW5hbWljWCI6ICIke21hcmdpbn0gKiAzICsgKHB4KDc5LjIzODEpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICogMiIsCiAgICAgICJkeW5hbWljWSI6ICIke21hcmdpbn0gKyAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCgyOC45NTIzODEpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoMjguOTUyMzgxKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDI4Ljk1MjM4MSkgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCgyOC42NjY2NjYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoMjguNjY2NjY2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDI4LjU3MTQyOCwKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgLTIsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiR1VJIFtGMV0iLAogICAgICAib3BhY2l0eSI6IDAuNywKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTY3NzcyMTYsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNzguNDc2MTkKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiBmYWxzZSwKICAgICAgImR5bmFtaWNYIjogIjAuNjA4MjAxNDQgKiAke3NjcmVlbl93aWR0aH0gLSAocHgoNzIuMzgwOTUpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgKHB4KDcyLjM4MDk1KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg3Mi4zODA5NSkgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNzIuMzgwOTUpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gJHt3aWR0aH0gLSAke21hcmdpbn0iLAogICAgICAiZHluYW1pY1kiOiAiMC44Nzg4NjQ2NSAqICR7c2NyZWVuX2hlaWdodH0gLSAocHgoMzQuMjg1NzEzKSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIiwKICAgICAgImhlaWdodCI6IDMzLjkwNDc2MiwKICAgICAgImlzU3dpcGVhYmxlIjogZmFsc2UsCiAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAia2V5Y29kZXMiOiBbCiAgICAgICAgLTgsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiwqsiLAogICAgICAib3BhY2l0eSI6IDAuNiwKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTY3NzcyMTYsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNzIuMAogICAgfSwKICAgIHsKICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAiY29ybmVyUmFkaXVzIjogMzAuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IGZhbHNlLAogICAgICAiZHluYW1pY1giOiAiMC42MDgyMDE0NCAqICR7c2NyZWVuX3dpZHRofSAtIChweCg3Mi4zODA5NSkgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAocHgoNzIuMzgwOTUpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDcyLjM4MDk1KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg3Mi4zODA5NSkgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNzIuMzMzMzM2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg3Mi4zMzMzMzYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IiwKICAgICAgImR5bmFtaWNZIjogIjAuODc4ODY0NjUgKiAke3NjcmVlbl9oZWlnaHR9IC0gKHB4KDM0LjI4NTcxMykgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSIsCiAgICAgICJoZWlnaHQiOiAzMy45MDQ3NjIsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiBmYWxzZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIC03LAogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwCiAgICAgIF0sCiAgICAgICJuYW1lIjogIsK7IiwKICAgICAgIm9wYWNpdHkiOiAwLjYsCiAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAic3Ryb2tlV2lkdGgiOiAzLjAsCiAgICAgICJ3aWR0aCI6IDcyLjAKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiBmYWxzZSwKICAgICAgImR5bmFtaWNYIjogIjAuOTc5NzA3OCAqICR7c2NyZWVuX3dpZHRofSAtIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gLSAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg1Ny4xNDI4NTcpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgLSAke21hcmdpbn0gKyAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSArICR7bWFyZ2lufSAtIChweCg1Ny4xNDI4NTcpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDU3LjE0Mjg1NykgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNTcuMTQyODU3KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSAtIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pIC0gJHttYXJnaW59ICsgKHB4KDQ4Ljc2MTkwNikgLyAxMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gLSAocHgoNDguNzYxOTA2KSAvIDEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8gMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gJHt3aWR0aH0gLSAke21hcmdpbn0iLAogICAgICAiZHluYW1pY1kiOiAiMC43MjA4MDQ0ICogJHtzY3JlZW5faGVpZ2h0fSAtIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IC0gKHB4KDQ4Ljc2MTkwNikgLzEwMC4wICogJHtwcmVmZXJyZWRfc2NhbGV9KSAtICR7bWFyZ2lufSArIChweCg0OC43NjE5MDYpIC8xMDAuMCAqICR7cHJlZmVycmVkX3NjYWxlfSkgKyAke21hcmdpbn0gKyAocHgoNDguNzYxOTA2KSAvMTAwLjAgKiAke3ByZWZlcnJlZF9zY2FsZX0pICsgJHttYXJnaW59IiwKICAgICAgImhlaWdodCI6IDQ4LjM4MDk1LAogICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgImlzVG9nZ2xlIjogZmFsc2UsCiAgICAgICJrZXljb2RlcyI6IFsKICAgICAgICA4MSwKICAgICAgICAwLAogICAgICAgIDAsCiAgICAgICAgMAogICAgICBdLAogICAgICAibmFtZSI6ICJxIiwKICAgICAgIm9wYWNpdHkiOiAwLjYsCiAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAic3Ryb2tlV2lkdGgiOiAzLjAsCiAgICAgICJ3aWR0aCI6IDQ4LjM4MDk1CiAgICB9LAogICAgewogICAgICAiYmdDb2xvciI6IDEyOTE4NDU2MzIsCiAgICAgICJjb3JuZXJSYWRpdXMiOiAzMC4wLAogICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICJkaXNwbGF5SW5NZW51IjogZmFsc2UsCiAgICAgICJkeW5hbWljWCI6ICIwLjMwNDAwODIyICogJHtzY3JlZW5fd2lkdGh9IiwKICAgICAgImR5bmFtaWNZIjogIjAuOTUxODU4OSAqICR7c2NyZWVuX2hlaWdodH0gLSAke2hlaWdodH0iLAogICAgICAiaGVpZ2h0IjogNDguMzgwOTUsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiBmYWxzZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIDcwLAogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwCiAgICAgIF0sCiAgICAgICJuYW1lIjogIkYiLAogICAgICAib3BhY2l0eSI6IDAuNiwKICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAic3Ryb2tlQ29sb3IiOiAtMTU5MjI0MjEsCiAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgIndpZHRoIjogNDguMzgwOTUKICAgIH0sCiAgICB7CiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDUwLjAsCiAgICAgICJkaXNwbGF5SW5HYW1lIjogdHJ1ZSwKICAgICAgImRpc3BsYXlJbk1lbnUiOiB0cnVlLAogICAgICAiZHluYW1pY1giOiAiMC4wNTczMjU0ODYgKiAke3NjcmVlbl93aWR0aH0iLAogICAgICAiZHluYW1pY1kiOiAiMS4wICogJHtzY3JlZW5faGVpZ2h0fSAtICR7aGVpZ2h0fSIsCiAgICAgICJoZWlnaHQiOiAxOC42NjY2NjYsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiBmYWxzZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiVFRzeSIsCiAgICAgICJvcGFjaXR5IjogMC4xLAogICAgICAicGFzc1RocnVFbmFibGVkIjogZmFsc2UsCiAgICAgICJzdHJva2VDb2xvciI6IC0xLAogICAgICAic3Ryb2tlV2lkdGgiOiAwLjAsCiAgICAgICJ3aWR0aCI6IDM3LjcxNDI4NwogICAgfQogIF0sCiAgIm1EcmF3ZXJEYXRhTGlzdCI6IFsKICAgIHsKICAgICAgImJ1dHRvblByb3BlcnRpZXMiOiBbCiAgICAgICAgewogICAgICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICAgICAiZGlzcGxheUluTWVudSI6IHRydWUsCiAgICAgICAgICAiZHluYW1pY1giOiAiMC43ODc3NzE0NiAqICR7c2NyZWVuX3dpZHRofSAtICR7d2lkdGh9IiwKICAgICAgICAgICJkeW5hbWljWSI6ICIwLjEwNzQxNzM2ICogJHtzY3JlZW5faGVpZ2h0fSIsCiAgICAgICAgICAiaGVpZ2h0IjogNDEuNTIzODEsCiAgICAgICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAgICAgImtleWNvZGVzIjogWwogICAgICAgICAgICA3NCwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMAogICAgICAgICAgXSwKICAgICAgICAgICJuYW1lIjogIkFCUklSIiwKICAgICAgICAgICJvcGFjaXR5IjogMC43LAogICAgICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAgICAgInN0cm9rZUNvbG9yIjogLTE2MTE5ODAwLAogICAgICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAgICAgIndpZHRoIjogNzIuMAogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICAgICAiZGlzcGxheUluTWVudSI6IHRydWUsCiAgICAgICAgICAiZHluYW1pY1giOiAiMC43ODc3NzE0NiAqICR7c2NyZWVuX3dpZHRofSAtICR7d2lkdGh9IiwKICAgICAgICAgICJkeW5hbWljWSI6ICIwLjIxMjk3MjkyICogJHtzY3JlZW5faGVpZ2h0fSIsCiAgICAgICAgICAiaGVpZ2h0IjogNDEuNTIzODEsCiAgICAgICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAgICAgImtleWNvZGVzIjogWwogICAgICAgICAgICA3OCwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMAogICAgICAgICAgXSwKICAgICAgICAgICJuYW1lIjogIldheXBvaW50ICIsCiAgICAgICAgICAib3BhY2l0eSI6IDAuNywKICAgICAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgICAgICJzdHJva2VDb2xvciI6IC0xNjc3NzIxNiwKICAgICAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgICAgICJ3aWR0aCI6IDcyLjAKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgICAgICJjb3JuZXJSYWRpdXMiOiAzMC4wLAogICAgICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAgICAgImRpc3BsYXlJbk1lbnUiOiB0cnVlLAogICAgICAgICAgImR5bmFtaWNYIjogIjAuNzg3NzcxNDYgKiAke3NjcmVlbl93aWR0aH0gLSAke3dpZHRofSIsCiAgICAgICAgICAiZHluYW1pY1kiOiAiMC4zMTg1Mjg1ICogJHtzY3JlZW5faGVpZ2h0fSIsCiAgICAgICAgICAiaGVpZ2h0IjogNDEuNTIzODEsCiAgICAgICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAgICAgImtleWNvZGVzIjogWwogICAgICAgICAgICA2NiwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMAogICAgICAgICAgXSwKICAgICAgICAgICJuYW1lIjogIkNSSUFSIiwKICAgICAgICAgICJvcGFjaXR5IjogMC43LAogICAgICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAgICAgIndpZHRoIjogNzIuMAogICAgICAgIH0sCiAgICAgICAgewogICAgICAgICAgImJnQ29sb3IiOiAxMjkxODQ1NjMyLAogICAgICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICAgICAiZGlzcGxheUluR2FtZSI6IHRydWUsCiAgICAgICAgICAiZGlzcGxheUluTWVudSI6IHRydWUsCiAgICAgICAgICAiZHluYW1pY1giOiAiMC43ODc3NzE0NiAqICR7c2NyZWVuX3dpZHRofSAtICR7d2lkdGh9IiwKICAgICAgICAgICJkeW5hbWljWSI6ICIwLjQyNDA4NDA0ICogJHtzY3JlZW5faGVpZ2h0fSIsCiAgICAgICAgICAiaGVpZ2h0IjogNDEuNTIzODEsCiAgICAgICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAgICAgImtleWNvZGVzIjogWwogICAgICAgICAgICA2MSwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMAogICAgICAgICAgXSwKICAgICAgICAgICJuYW1lIjogIisgWm9vbSIsCiAgICAgICAgICAib3BhY2l0eSI6IDAuNywKICAgICAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgICAgICJzdHJva2VDb2xvciI6IC0xNjc3NzIxNiwKICAgICAgICAgICJzdHJva2VXaWR0aCI6IDMuMCwKICAgICAgICAgICJ3aWR0aCI6IDcyLjAKICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgICAgICJjb3JuZXJSYWRpdXMiOiAzMC4wLAogICAgICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAgICAgImRpc3BsYXlJbk1lbnUiOiB0cnVlLAogICAgICAgICAgImR5bmFtaWNYIjogIjAuNzg3NzcxNDYgKiAke3NjcmVlbl93aWR0aH0gLSAke3dpZHRofSIsCiAgICAgICAgICAiZHluYW1pY1kiOiAiMC42MzA1NjU2ICogJHtzY3JlZW5faGVpZ2h0fSAtICR7aGVpZ2h0fSIsCiAgICAgICAgICAiaGVpZ2h0IjogNDEuNTIzODEsCiAgICAgICAgICAiaXNTd2lwZWFibGUiOiBmYWxzZSwKICAgICAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAgICAgImtleWNvZGVzIjogWwogICAgICAgICAgICA0NSwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMCwKICAgICAgICAgICAgMAogICAgICAgICAgXSwKICAgICAgICAgICJuYW1lIjogIi1ab29tIiwKICAgICAgICAgICJvcGFjaXR5IjogMC43LAogICAgICAgICAgInBhc3NUaHJ1RW5hYmxlZCI6IGZhbHNlLAogICAgICAgICAgInN0cm9rZUNvbG9yIjogLTE2Nzc3MjE2LAogICAgICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAgICAgIndpZHRoIjogNzIuMAogICAgICAgIH0KICAgICAgXSwKICAgICAgIm9yaWVudGF0aW9uIjogIkRPV04iLAogICAgICAicHJvcGVydGllcyI6IHsKICAgICAgICAiYmdDb2xvciI6IDEyOTE4NDU2MzIsCiAgICAgICAgImNvcm5lclJhZGl1cyI6IDMwLjAsCiAgICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAgICJkaXNwbGF5SW5NZW51IjogdHJ1ZSwKICAgICAgICAiZHluYW1pY1giOiAiMC43ODc3NzE0NiAqICR7c2NyZWVuX3dpZHRofSAtICR7d2lkdGh9IiwKICAgICAgICAiZHluYW1pY1kiOiAiMC4wMDE4NjE3OTgzICogJHtzY3JlZW5faGVpZ2h0fSIsCiAgICAgICAgImhlaWdodCI6IDQxLjUyMzgxLAogICAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAgICJpc1RvZ2dsZSI6IGZhbHNlLAogICAgICAgICJrZXljb2RlcyI6IFsKICAgICAgICAgIDAsCiAgICAgICAgICAwLAogICAgICAgICAgMCwKICAgICAgICAgIDAKICAgICAgICBdLAogICAgICAgICJuYW1lIjogIm1hcGEiLAogICAgICAgICJvcGFjaXR5IjogMC42LAogICAgICAgICJwYXNzVGhydUVuYWJsZWQiOiBmYWxzZSwKICAgICAgICAic3Ryb2tlQ29sb3IiOiAtMTY3NzcyMTYsCiAgICAgICAgInN0cm9rZVdpZHRoIjogMy4wLAogICAgICAgICJ3aWR0aCI6IDcyLjAKICAgICAgfQogICAgfQogIF0sCiAgIm1Kb3lzdGlja0RhdGFMaXN0IjogWwogICAgewogICAgICAiYWJzb2x1dGUiOiBmYWxzZSwKICAgICAgImZvcndhcmRMb2NrIjogZmFsc2UsCiAgICAgICJiZ0NvbG9yIjogMTI5MTg0NTYzMiwKICAgICAgImNvcm5lclJhZGl1cyI6IDAuMCwKICAgICAgImRpc3BsYXlJbkdhbWUiOiB0cnVlLAogICAgICAiZGlzcGxheUluTWVudSI6IGZhbHNlLAogICAgICAiZHluYW1pY1giOiAiMC4wNDkwNjY1NiAqICR7c2NyZWVuX3dpZHRofSIsCiAgICAgICJkeW5hbWljWSI6ICIwLjg3MTU4MjAzICogJHtzY3JlZW5faGVpZ2h0fSAtICR7aGVpZ2h0fSIsCiAgICAgICJoZWlnaHQiOiAxOTAuMDk1MjUsCiAgICAgICJpc1N3aXBlYWJsZSI6IGZhbHNlLAogICAgICAiaXNUb2dnbGUiOiBmYWxzZSwKICAgICAgImtleWNvZGVzIjogWwogICAgICAgIDAsCiAgICAgICAgMCwKICAgICAgICAwLAogICAgICAgIDAKICAgICAgXSwKICAgICAgIm5hbWUiOiAiYnV0dG9uIiwKICAgICAgIm9wYWNpdHkiOiAwLjYxLAogICAgICAicGFzc1RocnVFbmFibGVkIjogZmFsc2UsCiAgICAgICJzdHJva2VDb2xvciI6IC0xNjE4NTU5MywKICAgICAgInN0cm9rZVdpZHRoIjogMTAuMCwKICAgICAgIndpZHRoIjogMTkwLjA5NTI1CiAgICB9CiAgXSwKICAic2NhbGVkQXQiOiAxMDAuMCwKICAidmVyc2lvbiI6IDgKfQ=="
_asc_controls_bytes = _asc_b64.b64decode(_asc_controls_b64)
if _asc_hashlib.sha256(_asc_controls_bytes).hexdigest() != "156b2d4669bff8c9377b73d79941ae6bd44682d356aebba230bd018530ea5491":
    raise SystemExit("[Ascension v0.27] SHA-256 do oficial.json não confere")

_asc_controls_asset = root / "app_pojavlauncher/src/main/assets/ascension-mundo-controls.json"
_asc_controls_asset.parent.mkdir(parents=True, exist_ok=True)
_asc_controls_asset.write_bytes(_asc_controls_bytes)

bootstrap = bootstrap_path.read_text(encoding="utf-8")

profile_anchor = '        profile.gameDir = AscensionConfig.GAME_DIR_NAME;\n'
recovery_line = '        profile.controlFile = null; // v0.27: não prende o launch a arquivo customizado\n'
if recovery_line not in bootstrap:
    if profile_anchor not in bootstrap:
        raise SystemExit("[Ascension v0.27] ponto do profile não encontrado")
    bootstrap = bootstrap.replace(profile_anchor, profile_anchor + recovery_line, 1)

ready_anchor = '''        AscensionUpdater updater = new AscensionUpdater(activity, listener::onStatus);
        updater.sync(gameDir);
        listener.onReady(neoId, launchAfter);
'''
ready_replacement = '''        AscensionUpdater updater = new AscensionUpdater(activity, listener::onStatus);
        updater.sync(gameDir);
        installAscensionControlsSafely();
        listener.onReady(neoId, launchAfter);
'''
if "installAscensionControlsSafely();" not in bootstrap:
    if ready_anchor not in bootstrap:
        raise SystemExit("[Ascension v0.27] ponto pós-updater não encontrado")
    bootstrap = bootstrap.replace(ready_anchor, ready_replacement, 1)

helper_anchor = '    private void ensureLocalAccount(String nick, String selectedVersion) throws Exception {\n'
if "private void installAscensionControlsSafely()" not in bootstrap:
    helper = r'''    private void installAscensionControlsSafely() {
        try {
            File controlDir = new File(Tools.CTRLMAP_PATH);
            if (!controlDir.exists() && !controlDir.mkdirs()) return;

            File target = new File(Tools.CTRLDEF_FILE);
            File temp = new File(controlDir, "default.ascension-v027.tmp");
            File backup = new File(controlDir, "default.before-ascension-v027.json");

            if (target.isFile() && target.length() > 0 && !backup.exists()) {
                try (java.io.FileInputStream in = new java.io.FileInputStream(target);
                     java.io.FileOutputStream out = new java.io.FileOutputStream(backup, false)) {
                    byte[] buf = new byte[8192];
                    int n;
                    while ((n = in.read(buf)) >= 0) {
                        if (n > 0) out.write(buf, 0, n);
                    }
                    out.flush();
                } catch (Throwable ignored) {}
            }

            try (java.io.InputStream in = activity.getAssets().open("ascension-mundo-controls.json");
                 java.io.FileOutputStream out = new java.io.FileOutputStream(temp, false)) {
                byte[] buffer = new byte[8192];
                int read;
                while ((read = in.read(buffer)) >= 0) {
                    if (read > 0) out.write(buffer, 0, read);
                }
                out.flush();
                try { out.getFD().sync(); } catch (Throwable ignored) {}
            }

            if (!temp.isFile() || temp.length() < 1000) {
                temp.delete();
                return;
            }

            try {
                String raw = Tools.read(temp.getAbsolutePath());
                net.kdt.pojavlaunch.customcontrols.CustomControls parsed =
                        Tools.GLOBAL_GSON.fromJson(raw, net.kdt.pojavlaunch.customcontrols.CustomControls.class);
                if (parsed == null || parsed.version != 8 || parsed.mControlDataList == null ||
                        parsed.mControlDataList.size() < 20 || parsed.mJoystickDataList == null) {
                    temp.delete();
                    return;
                }
            } catch (Throwable invalid) {
                temp.delete();
                return;
            }

            File old = new File(controlDir, "default.ascension-v027.old");
            if (old.exists()) old.delete();
            boolean hadTarget = target.exists();
            if (hadTarget && !target.renameTo(old)) {
                temp.delete();
                return;
            }

            if (!temp.renameTo(target)) {
                temp.delete();
                if (hadTarget && old.exists()) old.renameTo(target);
                return;
            }
            if (old.exists()) old.delete();

            android.content.SharedPreferences pojavPrefs = LauncherPreferences.DEFAULT_PREF;
            if (pojavPrefs != null) {
                pojavPrefs.edit().putString("defaultCtrl", Tools.CTRLDEF_FILE).commit();
            }
            LauncherPreferences.PREF_DEFAULTCTRL_PATH = Tools.CTRLDEF_FILE;
        } catch (Throwable ignored) {
            // Controles jamais podem impedir Minecraft/NeoForge de iniciar.
        }
    }

'''
    if helper_anchor not in bootstrap:
        raise SystemExit("[Ascension v0.27] ponto para helper não encontrado")
    bootstrap = bootstrap.replace(helper_anchor, helper + helper_anchor, 1)

bootstrap_path.write_text(bootstrap, encoding="utf-8")
print("[Ascension v0.27] base v0.25 preservada + controles via default.json seguro + recovery v0.26 OK")

