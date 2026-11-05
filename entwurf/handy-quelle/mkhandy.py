# Erzeugt entwurf/handy.html aus entwurf/index.html (Handy-Fassung)
import sys,re
D='/home/claude/lgf-homepage/entwurf/'
s=open(D+'index.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    assert c==n,(a[:60],c)
    s=s.replace(a,b)
rep('<title>Lenggrieser Gleitschirmflieger Entwurf</title>','<title>Lenggrieser Gleitschirmflieger Handy</title>')
# Weiterleitung zur Handyseite nicht in der Handyseite selbst
s=re.sub(r'<script id="toMobile">.*?</script>\n','',s,flags=re.S)
rep('<span><b>Entwurf</b> der neuen Vereinsseite · Windwerte von Brauneck Berg echt vom 04.11., sonst Beispieldaten</span><span>Umsetzbar mit WordPress + Elementor</span>',
    '<span><b>Entwurf Handy</b> · Beispieldaten</span><a href="index.html?desktop">Desktop-Ansicht</a>')
# Windmodell: Überschrift über das Bild
rep('''    <div class="wi-frame"><iframe''','''    <div class="wi-head"><span class="eyebrow">Brauneck in 3D</span><h2 style="margin-top:10px">So weht der Wind <em>am Berg</em></h2></div>
    <div class="wi-frame"><iframe''')
rep('''      <span class="eyebrow">Brauneck in 3D</span>
      <h2 style="margin-top:12px">So weht der Wind <em>am Berg</em></h2>
''','')
rep('<a href="wind-stationen.html?nord" target="_blank" rel="noopener">Im Vollbild öffnen</a>','<a href="wind-stationen.html?nord" target="_blank" rel="noopener">Vollbild öffnen</a>')
# Stationen: Tabellen zugeklappt, Wisch-Hinweis + Punkte
rep("'<details class=\"hist\" open>","'<details class=\"hist\">")
rep('<div class="stations" id="stations"></div>','<div class="st-mob" id="stations"><div class="tiles" id="tiles"></div><p class="tile-hint">Station antippen für Verlauf und Tabelle</p><div id="stDetail"></div></div>')
rep("""  function renderStations(){
    var box=document.getElementById('stations');
    box.innerHTML=stations.map(card).join('');
    box.querySelectorAll('.tbl-wrap').forEach(function(w){w.scrollLeft=w.scrollWidth});
  }""","""  var sel=0;
  function tile(s,i){var st=status(s);
    return '<button type="button" class="tile'+(i===sel?' on':'')+'" data-i="'+i+'" aria-pressed="'+(i===sel)+'"><span class="t-top"><b>'+s.name.replace('Brauneck ','')+'</b><span class="pill '+st.c+'">'+st.t+'</span></span>'+compass(s)+
      '<span class="t-v num"><b>'+Math.round(s.mean)+'</b><i>/</i><b class="g">'+Math.round(s.gust)+'</b><small>km/h</small></span><span class="t-d">'+dirName(s.dir)+' · '+fmt(s.temp)+' °C</span></button>';}
  function showDetail(i,scroll){sel=i;var t=document.getElementById('tiles');t.innerHTML=stations.map(tile).join('');
    var d=document.getElementById('stDetail');d.innerHTML=card(stations[i]);d.querySelectorAll('.tbl-wrap').forEach(function(w){w.scrollLeft=w.scrollWidth});
    if(scroll)d.scrollIntoView({behavior:'smooth',block:'start'});}
  function renderStations(){showDetail(sel)}""")
rep("  renderNow();renderStations();","""  renderNow();renderStations();
  document.getElementById('tiles').addEventListener('click',function(e){var b=e.target.closest('.tile');if(b)showDetail(+b.dataset.i,true)});
  document.getElementById('nowRows').addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;e.preventDefault();
    var id=+a.getAttribute('href').replace('#st-',''),i=stations.findIndex(function(s){return s.id===id});showDetail(i);
    document.getElementById('stations').scrollIntoView({behavior:'smooth',block:'start'})});""")
# Handy-CSS am Ende des Style-Blocks
css=open('/tmp/claude-0/-home-claude/c072efd7-ea6e-5d19-99b5-89faadf538a4/scratchpad/handy/handy.css',encoding='utf-8').read()
i=s.index('</style>');s=s[:i]+css+s[i:]
s='<!doctype html>\n<html lang="de">\n'+s
open(D+'handy.html','w',encoding='utf-8').write(s)
print('ok',len(s))
