(() => {
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => [...document.querySelectorAll(s)];
  const android = window.AscensionAndroid || null;
  let state = {nick:'',engineReady:true,minecraftInstalled:false,neoforgeInstalled:false,prepared:false,busy:false};
  let toastTimer;

  function call(name, ...args){
    try { if (android && typeof android[name] === 'function') return android[name](...args); }
    catch(e) { toast('Falha na ponte Android: '+e.message, 'error'); }
  }
  function parse(v){ try { return typeof v === 'string' ? JSON.parse(v) : v; } catch { return {}; } }
  function toast(msg, kind=''){
    const el=$('#toast'); if(!el) return;
    el.textContent=msg; el.className='toast '+kind; el.hidden=false;
    clearTimeout(toastTimer); toastTimer=setTimeout(()=>el.hidden=true,3200);
  }

  // Stable tap binding. Let WebView produce the normal click.
  // A native Android fallback is used only if that click never arrives.
  let clickGeneration = 0;
  document.addEventListener('click', () => { clickGeneration++; }, true);

  function bindTap(el, handler){
    if(!el) return;
    el.style.touchAction = 'manipulation';
    el.addEventListener('click', handler);
  }

  function render(){
    const nick=state.nick||'';
    $('#nickDisplay').textContent=nick||'Escolher Nick';
    $('#nickInput').value=nick;
    $('#dockHint').textContent=nick ? `Treinador: ${nick}` : 'Escolha seu Nick para começar.';
    const stages=[];
    stages.push(state.minecraftInstalled?'Minecraft ✓':'Minecraft 1.21.1');
    stages.push(state.neoforgeInstalled?'NeoForge ✓':'NeoForge 21.1.200');
    stages.push(state.prepared?'Modpack ✓':'Modpack');
    $('#playSubtitle').textContent=!nick?'Escolha seu Nick':(state.busy?'Preparando...':stages.join(' · '));
    $('#playButton').disabled=!!state.busy;
    $('#prepareButton').disabled=!!state.busy;
    $('#serverStatus').textContent='Online';
  }
  function refresh(){ const raw=call('getState'); if(raw){ state={...state,...parse(raw)}; render(); } }
  function openNick(){ $('#nickMessage').hidden=true; $('#nickModal').hidden=false; setTimeout(()=>$('#nickInput').focus(),60); }
  function closeNick(){ $('#nickModal').hidden=true; }
  function saveNick(){
    const nick=$('#nickInput').value.trim();
    if(!/^[A-Za-z0-9_]{3,16}$/.test(nick)){ $('#nickMessage').textContent='Use de 3 a 16 caracteres: letras, números ou _.'; $('#nickMessage').hidden=false; return; }
    call('saveNick',nick); state.nick=nick; render(); closeNick(); toast('Nick salvo: '+nick,'success');
  }
  function setProgress(message,p){
    $('#progressWrap').hidden=false; $('#progressLabel').textContent=message||'Preparando...';
    if(typeof p==='number'){ const x=Math.max(0,Math.min(100,p)); $('#progressPercent').textContent=x+'%'; $('#progressBar').style.width=x+'%'; }
    $('#footerText').textContent=message||'Preparando...';
  }

  let lastNativeTap = 0;
  function nativeTap(cssX, cssY){
    const now = Date.now();
    if(now - lastNativeTap < 120) return;
    lastNativeTap = now;

    let el = document.elementFromPoint(cssX, cssY);
    if(!el) return;

    const target = el.closest && el.closest('button,input,a,[data-action],[data-tab]');
    if(target) el = target;

    // Capture the target NOW. Do not query elementFromPoint again later,
    // because a modal may have appeared over the same coordinates.
    const captured = el;
    const generationAtUp = clickGeneration;

    setTimeout(() => {
      // Normal WebView click already arrived: do absolutely nothing.
      if(clickGeneration !== generationAtUp) return;
      if(!captured || !document.documentElement.contains(captured)) return;

      if(captured.tagName === 'INPUT'){
        captured.focus();
        return;
      }

      if(typeof captured.click === 'function'){
        captured.click();
      }
    }, 110);
  }

  window.AscensionMobile={
    nativeTap(cssX,cssY){ nativeTap(cssX,cssY); },
    onState(raw){ state={...state,...parse(raw)}; render(); },
    onEvent(raw){
      const e=parse(raw);
      if(e.type==='progress'){ state.busy=true; setProgress(e.message,e.progress); render(); }
      else if(e.type==='done'){ setProgress(e.message,100); state.prepared=true; state.busy=false; render(); toast(e.message,'success'); setTimeout(()=>$('#progressWrap').hidden=true,1800); }
      else if(e.type==='error'){ state.busy=false; $('#footerText').textContent=e.message; render(); toast(e.message,'error'); }
      else if(e.type==='needNick'){ state.busy=false; openNick(); toast(e.message,'error'); }
      else if(e.type==='nick'){ state.nick=e.message; render(); }
      else { if(e.message) toast(e.message); }
    },
    onServer(){ $('#serverStatus').textContent='Online'; }
  };

  $$('.rail-button').forEach(btn=>bindTap(btn,()=>{ 
    $$('.rail-button').forEach(x=>x.classList.remove('active'));
    btn.classList.add('active');
    $$('.page').forEach(x=>x.classList.remove('active'));
    $('#page-'+btn.dataset.tab).classList.add('active');
  }));
  $$('[data-action="site"]').forEach(x=>bindTap(x,()=>call('openWebsite')));
  $$('[data-action="discord"]').forEach(x=>bindTap(x,()=>call('openDiscord')));
  bindTap($('#nickChip'),openNick);
  bindTap($('#closeNick'),closeNick);
  bindTap($('#saveNick'),saveNick);
  $('#nickInput').addEventListener('keydown',e=>{if(e.key==='Enter')saveNick()});
  $('#nickModal').addEventListener('click',e=>{if(e.target===$('#nickModal'))closeNick()});
  bindTap($('#prepareButton'),()=>call('prepare'));
  bindTap($('#playButton'),()=>{ if(!state.nick) openNick(); else call('play'); });
  bindTap($('#repairButton'),()=>call('repair'));
  bindTap($('#checkServerButton'),()=>{ $('#serverStatus').textContent='Online'; toast('Servidor Ascension Pixelmon: Online','success'); });

  document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh()});
  document.addEventListener('contextmenu',e=>e.preventDefault());
  refresh();
  $('#serverStatus').textContent='Online';
})();