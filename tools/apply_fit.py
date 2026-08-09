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

print("[Ascension v0.20] RAM configurável + ícone novo + NeoForge lifecycle-safe OK")
