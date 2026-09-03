#!/usr/bin/env python3
"""Patch idempotente do cardapio Beach Farol (public/app/index.html)."""
import re, json, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'public/app/index.html')
src = open(PATH, encoding='utf-8').read()

if '_converterArquivoParaDataURL' in src:
    print('ja aplicado'); sys.exit(0)

urls = {}
for f in glob.glob(os.path.join(ROOT, 'src/assets/*.asset.json')):
    k = os.path.basename(f).split('.')[0]
    urls[k] = json.load(open(f))['url']

def rep(old, new, count=1, label=''):
    global src
    n = src.count(old)
    assert n == count, f"FALHOU [{label}]: esperava {count}, achou {n}"
    src = src.replace(old, new); print('OK', label, f'({count}x)')

# 0) Desliga a sincronizacao Supabase herdada (offline-first puro)
rep('''  function _init() {
    try {
      if (typeof supabase === "undefined" || !supabase.createClient) return;''',
'''  function _init() {
    // BEACH FAROL: backend externo desativado — tudo roda 100% em localStorage.
    console.info("[Sync] desativado — modo localStorage");
    return;
    try {
      if (typeof supabase === "undefined" || !supabase.createClient) return;''', 1, '0-sync-off')

# 0b) bump da versao do cardapio local para carregar as novas imagens/precos
rep('var VER="gv_v11";', 'var VER="gv_v12_beachfarol";', 1, '0b-ver')

# A) upload local (sem rede)
rep('''async function _resolverFotoItem() {
  if (_arquivoImagemSelecionado) {
    var status = document.getElementById("edit-img-upload-status");
    if (status) status.textContent = "Enviando imagem…";
    try {
      var urlPublica = await _uploadImagemParaStorage(_arquivoImagemSelecionado);
      if (status) status.textContent = "✅ Enviada";
      return urlPublica;
    } catch (e) {
      toast("⚠️ Falha ao enviar a imagem: " + e.message);
      if (status) status.textContent = "❌ Falhou";
      throw e;
    }
  }''',
'''function _converterArquivoParaDataURL(file) {
  return new Promise(function(resolve, reject) {
    var reader = new FileReader();
    reader.onload = function(ev) {
      var im = new Image();
      im.onload = function() {
        var max = 900;
        var esc = Math.min(1, max / Math.max(im.width, im.height));
        var w = Math.max(1, Math.round(im.width * esc));
        var h = Math.max(1, Math.round(im.height * esc));
        var cv = document.createElement("canvas");
        cv.width = w; cv.height = h;
        cv.getContext("2d").drawImage(im, 0, 0, w, h);
        resolve(cv.toDataURL("image/jpeg", 0.82));
      };
      im.onerror = function(){ reject(new Error("imagem invalida")); };
      im.src = ev.target.result;
    };
    reader.onerror = function(){ reject(new Error("falha ao ler arquivo")); };
    reader.readAsDataURL(file);
  });
}

async function _resolverFotoItem() {
  if (_arquivoImagemSelecionado) {
    var status = document.getElementById("edit-img-upload-status");
    if (status) status.textContent = "Processando imagem…";
    try {
      var dataUrl = await _converterArquivoParaDataURL(_arquivoImagemSelecionado);
      if (status) status.textContent = "✅ Pronta";
      return dataUrl;
    } catch (e) {
      toast("⚠️ Nao foi possivel processar a imagem: " + e.message);
      if (status) status.textContent = "❌ Falhou";
      throw e;
    }
  }''', 1, 'A-upload-local')

# A2) ao editar sem trocar foto, manter a foto atual do item (nao voltar ao placeholder)
rep('''  return "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80"; // placeholder padrão do sistema
}''',
'''  var _idAtual = (document.getElementById("edit-item-id") || {}).value;
  if (_idAtual && typeof getItem === "function") {
    var _atual = getItem(_idAtual);
    if (_atual && _atual.img) return _atual.img; // mantem a foto atual
  }
  return "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80"; // placeholder padrão do sistema
}''', 1, 'A2-manter-foto')

# B) salvarItem com mascara
rep('  const novo   = document.getElementById("edit-novo-tog").classList.contains("on");',
    '  const novo   = document.getElementById("edit-novo-tog").classList.contains("on");\n  const _mt = document.getElementById("edit-mascara-tog");\n  const mascara = !!(_mt && _mt.classList.contains("on"));', 1, 'B1')
rep('cat.itens.push({id: itemId, nome, desc, preco, porcao, tempo, novo, img});',
    'cat.itens.push({id: itemId, nome, desc, preco, porcao, tempo, novo, img, mascaraPreco: mascara});', 1, 'B2')
rep('cat.itens.push({id: genId(), nome, desc, preco, porcao, tempo, novo, img});',
    'cat.itens.push({id: genId(), nome, desc, preco, porcao, tempo, novo, img, mascaraPreco: mascara});', 1, 'B3')

# C) modal sync
rep('document.getElementById("edit-novo-tog").classList.remove("on");',
    'document.getElementById("edit-novo-tog").classList.remove("on");\n  { const t=document.getElementById("edit-mascara-tog"); if(t) t.classList.remove("on"); }', 1, 'C1')
rep('document.getElementById("edit-novo-tog").classList.toggle("on", !!item.novo);',
    'document.getElementById("edit-novo-tog").classList.toggle("on", !!item.novo);\n  { const t=document.getElementById("edit-mascara-tog"); if(t) t.classList.toggle("on", !!item.mascaraPreco); }', 1, 'C2')

# D) campo no modal
rep('''<div class="mt-2 hidden" id="edit-img-preview-wrap">
<img class="w-20 h-20 object-cover rounded-lg border border-gray-200" id="edit-img-preview">
</div>
</div>
</div>''',
'''<div class="mt-2 hidden" id="edit-img-preview-wrap">
<img class="w-20 h-20 object-cover rounded-lg border border-gray-200" id="edit-img-preview">
</div>
</div>
<div>
<label class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 block">Foto com preco carimbado?</label>
<label class="flex items-center gap-2 cursor-pointer">
<div class="tog" id="edit-mascara-tog" onclick="this.classList.toggle(&#39;on&#39;)"><div class="knob"></div></div>
<span class="text-sm font-semibold text-gray-600">Cobrir o preco antigo da arte e mostrar o preco digital</span>
</label>
</div>
</div>''', 1, 'D-modal')

# E) mascara nos cards (render base + override)
rep('''            onerror="this.src='https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80';this.onerror=null"/>
          <span class="b-cat">''',
'''            onerror="this.src='https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80';this.onerror=null"/>
          ${item.mascaraPreco ? `<span class="cc-mascara-preco">${fmtBRL(item.preco)}</span>` : ""}
          <span class="b-cat">''', 2, 'E-mascara-card')

# F) CSS no final do documento
CSS = '''<style>
/* BEACH FAROL - grid 2 colunas travado + mascara de preco */
#items-wrap .cc-grade-premium, #items-wrap .grid{grid-template-columns:repeat(2,minmax(0,1fr)) !important}
#items-wrap .img-box{aspect-ratio:1/1 !important;width:100% !important;height:auto !important;overflow:hidden !important;position:relative !important;flex:none !important}
#items-wrap .img-box img.card-img{width:100% !important;height:100% !important;object-fit:cover !important;display:block !important}
.cc-mascara-preco{position:absolute;left:8%;right:8%;bottom:9%;z-index:5;background:#1d4ed8;color:#fff;border-radius:10px;padding:5px 8px;font-weight:900;text-align:center;font-size:clamp(.85rem,4vw,1.05rem);box-shadow:0 4px 14px rgba(15,35,64,.4);pointer-events:none}
</style>
'''
i = src.rfind('</body>'); assert i > 0
src = src[:i] + CSS + src[i:]; print('OK F-css')

# G) merge preservando edicoes do Admin
rep('''      itens: defCat.itens.map(defIt => {
        const savedIt = savedCat && savedCat.itens ? savedCat.itens.find(s=>s.id===defIt.id) : null;
        return savedIt ? {...defIt, preco: savedIt.preco||defIt.preco, ativo: savedIt.ativo!==false} : defIt;
      })''',
'''      itens: (function(){
        const savedItens = (savedCat && savedCat.itens) ? savedCat.itens : [];
        const mesclados = defCat.itens.map(defIt => {
          const savedIt = savedItens.find(s=>s.id===defIt.id);
          if(!savedIt) return defIt;
          return {
            ...defIt,
            nome: savedIt.nome || defIt.nome,
            desc: savedIt.desc || defIt.desc,
            porcao: savedIt.porcao || defIt.porcao,
            tempo: savedIt.tempo || defIt.tempo,
            preco: savedIt.preco || defIt.preco,
            preco_praia: savedIt.preco_praia, preco_restaurante: savedIt.preco_restaurante,
            ativo: savedIt.ativo !== false,
            mascaraPreco: (savedIt.mascaraPreco !== undefined) ? savedIt.mascaraPreco : !!defIt.mascaraPreco,
            img: (savedIt.img && String(savedIt.img).indexOf("photo-1555939594") === -1) ? savedIt.img : defIt.img
          };
        });
        savedItens.forEach(sit => { if(!defCat.itens.some(d=>d.id===sit.id)) mesclados.push(sit); });
        return mesclados;
      })()''', 1, 'G-merge')

# H) mapa de imagens -> ids
G = urls['balde-generico']
MAPA = {
 'bebidas_combo_5_amstel': (urls['balde-amstel-criativo'], False),
 'bebidas_combo_5_antarctica_original': (urls['balde-antarctica'], False),
 'bebidas_combo_5_heineken': (urls['balde-heineken'], False),
 'bebidas_combo_5_heineken_s_alcool': (urls['longneck-heineken'], False),
 'bebidas_combo_5_itaipava': (urls['balde-itaipava'], False),
 'bebidas_combo_5_stella_artois': (urls['balde-stella'], False),
 'bebidas_combo_5_stella_s_gluten': (urls['balde-stella'], False),
 'bebidas_combo_5_budweiser': (urls['balde-budweiser'], False),
 'bebidas_combo_5_imperio_lager': (G, False),
 'bebidas_combo_5_imperio_ultra': (G, False),
 'bebidas_combo_5_corona': (G, False),
 'bebidas_combo_5_corona_s_alcool': (G, False),
 'bebidas_combo_5_coronita': (G, False),
 'bebidas_combo_5_51_ice': (G, False),
 'bebidas_combo_5_ice_leev': (G, False),
 'bebidas_combo_5_smirnoff_ice': (G, False),
 'bebidas_mojito': (urls['drink-mojito'], True),
 'bebidas_bob_marley': (urls['drink-bob-marley'], True),
 'bebidas_aperol_spritz': (urls['drink-aperol-spritz'], True),
 'bebidas_gin_tonica': (urls['drink-gin-tonica'], True),
 'bebidas_sangria': (urls['drink-sangria'], True),
 'bebidas_sex_on_the_beach': (urls['drink-sex-on-the-beach'], True),
 'bebidas_margarita_frozen': (urls['drink-margarita-frozen'], True),
 'bebidas_blue_lagoon': (urls['drink-blue-lagoon'], True),
 'bebidas_moscow_mule': (urls['drink-moscow-mule'], True),
 'bebidas_absolut_garrafa': (urls['vodka-absolut'], False),
 'bebidas_chivas_regal_garrafa': (urls['whisky-chivas'], False),
 'bebidas_combo_whisky_buchanan_s': (urls['whisky-buchanans'], False),
 'bebidas_gold_label': (urls['whisky-gold-label'], False),
 'bebidas_old_parr': (urls['whisky-old-parr'], False),
 'bebidas_red_label': (urls['whisky-red-label'], False),
 'bebidas_gelo_de_coco': (urls['gelo-de-coco'], True),
 'bebidas_coco_verde_suco_limao': (urls['bebidas-coco'], False),
 'bebidas_43_sensacoes': (urls['bebidas-caipirinhas'], False),
 'bebidas_beach_farol_drink': (urls['drinks-caipirinhas-2'], False),
 'pratos_bife_a_cavalo': (urls['prato-bife-a-cavalo'], False),
 'pratos_file_de_carne_a_parmegiana': (urls['prato-file-parmegiana'], False),
 'pratos_file_de_frango_a_parmegiana': (urls['prato-parmegiana-2'], False),
 'pratos_posta_de_peixe_grelhada': (urls['prato-posta-peixe'], False),
 'pratos_strogonoff_de_frango': (urls['prato-strogonoff-frango'], False),
 'pratos_strogonoff_de_camarao': (urls['prato-strogonoff-2'], False),
 'pratos_corvina_frita_inteira': (urls['prato-peixe-chapa'], False),
}
PRECOS = {'bebidas_absolut_garrafa':220,'bebidas_chivas_regal_garrafa':300,'bebidas_gold_label':470,
          'bebidas_old_parr':380,'bebidas_red_label':200,'bebidas_combo_whisky_buchanan_s':400}

linhas = src.splitlines(); aplic = set(); vistos = set(); out = []
for l in linhas:
    m = re.search(r'\{ id: "([a-z0-9_]+)"', l)
    if not m: out.append(l); continue
    iid = m.group(1)
    if iid in vistos and 'img:' in l:
        print('removido duplicado', iid); continue
    vistos.add(iid)
    novo = l
    if iid in MAPA and 'img:' in l:
        img, mask = MAPA[iid]
        novo = re.sub(r'img: [^,}]+', f'img: "{img}"', novo, count=1)
        if mask and 'mascaraPreco' not in novo:
            novo = re.sub(r'\s*\}(\s*,?)\s*$', r', mascaraPreco: true }\1', novo)
        aplic.add(iid)
    if iid in PRECOS:
        novo = re.sub(r'preco: [\d.]+', f'preco: {PRECOS[iid]}', novo, count=1)
    out.append(novo)
print('mapeados:', len(aplic), '| faltam:', sorted(set(MAPA) - aplic) or 'nenhum')
src = '\n'.join(out)

# I) novos combos de gin
if 'bebidas_combo_gin_tanqueray' not in src:
    m = re.search(r'^(\s*)(\{ id: "bebidas_gelo_de_coco".*)$', src, re.M); assert m
    ind = m.group(1)
    novos = (f'{ind}{{ id: "bebidas_combo_gin_tanqueray", nome: "Combo Gin Tanqueray", preco: 260, desc: "Gin Tanqueray + aguas tonicas", porcao: "garrafa 750ml", tempo: 5, sub: "Doses, Garrafas & Nao Alcoolicos", ativo: true, novo: true, img: "{urls["combo-gin-tanqueray"]}", mascaraPreco: true }},\n'
             f'{ind}{{ id: "bebidas_combo_gin_beefeater", nome: "Combo Gin Beefeater", preco: 230, desc: "Gin Beefeater + aguas tonicas", porcao: "garrafa 750ml", tempo: 5, sub: "Doses, Garrafas & Nao Alcoolicos", ativo: true, novo: true, img: "{urls["combo-gin-beefeater"]}", mascaraPreco: true }},\n')
    src = src[:m.start()] + novos + src[m.start():]
    print('OK I-combos-gin')

open(PATH, 'w', encoding='utf-8').write(src)
print('SALVO', len(src) // 1024, 'KB')
