#!/usr/bin/env python3
"""Gera um caderno HTML autocontido a partir do conteúdo e do template do projeto."""
import argparse, base64, html, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE_MAP={}
def proof(value):
    parts=re.split(r'(prova-[a-z0-9]+)',value)
    return ''.join('<a href="'+esc(SOURCE_MAP[x]['path'])+'">'+esc(SOURCE_MAP[x]['title'])+'</a>' if x in SOURCE_MAP else esc(x) for x in parts)

def esc(value):return html.escape(str(value),quote=True)
def p(texts):return ''.join('<p>'+esc(x)+'</p>' for x in texts)
def code(value):return '<pre><code>'+esc(value)+'</code></pre>' if value else ''
def json_script(value):return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')

def validate(d):
    assert d['schema_version']==1, 'Versão de conteúdo desconhecida'
    assert d['storage_key'] and d['id'] and d['filename'].endswith('.html')
    ids=set();source_ids={s['id'] for s in d['sources']}
    assert len(source_ids)==len(d['sources']), 'Fonte duplicada'
    for s in d['sources']:
        assert (ROOT/s['path']).is_file(), f'Fonte ausente: {s["path"]}'
        assert all(1<=n<=s['pages'] for n in s['preview_pages'])
    for c in d['chapters']:
        assert c['id'] not in ids;ids.add(c['id'])
        for t in c['topics']:
            assert t['id'] not in ids;ids.add(t['id'])
            for key in ('title','objective','sections','example','invariant','cost','caution','sources','exercises'):
                assert t[key], f'Tópico {t["id"]} sem {key}'
            for r in t['sources']:assert r['source'] in source_ids
            assert len(t['exercises'])>=3
            for e in t['exercises']:
                assert e['id'] not in ids;ids.add(e['id'])
                assert e['title'] and e['prompt'] and e['hint'] and len(e['steps'])>=2
                assert e['chapter']==c['id'] and e['topic']==t['id']

def exercise(e,prefix='study'):
    id=e['id'];uid=prefix+'-'+id
    choices=[('new','Ainda não tentei'),('attempted','Tentei'),('review','Revisar'),('mastered','Resolvi sem ajuda')]
    return f'''<article class="exercise" id="{uid}" data-ex="{id}" data-current-state="new">
<div class="eyebrow">{id}<span>{esc(e['kind'])}</span></div><h4>{esc(e['title'])}</h4><p>{esc(e['prompt'])}</p>
{('<p class="exam-link">Habilidade de prova: '+proof(e['exam'])+'</p>') if e['exam'] else ''}
<details class="hint"><summary>Uma dica, se precisar</summary><p>{esc(e['hint'])}</p></details>
<details class="solution"><summary>Conferir solução passo a passo</summary><ol>{''.join('<li>'+esc(x)+'</li>' for x in e['steps'])}</ol>{code(e['answer_code'])}<p class="rubric">Refaça sem abrir esta solução antes de marcar “Resolvi sem ajuda”.</p></details>
<div class="self-check"><label for="{uid}-state">Minha autoavaliação</label><select id="{uid}-state" data-state="{id}">{''.join('<option value="'+v+'">'+esc(label)+'</option>' for v,label in choices)}</select><span data-date="{id}" class="review-date"></span></div>
<details class="notes"><summary>Registrar raciocínio ou dúvida</summary><label class="sr-only" for="{uid}-note">Anotações de {id}</label><textarea id="{uid}-note" data-note="{id}" maxlength="20000" rows="4" placeholder="Minha tentativa, desenho, justificativa ou dúvida…"></textarea></details></article>'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('conteudo',nargs='?',default='conteudo/estruturas-de-dados.json');args=parser.parse_args()
    d=json.loads((ROOT/args.conteudo).read_text());validate(d)
    sources={s['id']:s for s in d['sources']}
    SOURCE_MAP.clear(); SOURCE_MAP.update(sources)
    topics=[t for c in d['chapters'] for t in c['topics']]
    exercises=[e for t in topics for e in t['exercises']]
    slides={}
    for s in d['sources']:
        for n in s['preview_pages']:
            path=ROOT/'assets/estruturas-de-dados'/f'{s["id"]}-{n:03}.webp'
            if not path.is_file():raise ValueError(f'Prévia ausente: {path}. Execute preparar_fontes.py.')
            slides[f'{s["id"]}-{n}']={'image':'data:image/webp;base64,'+base64.b64encode(path.read_bytes()).decode(),'label':f'{s["title"]} · página física {n} do PDF'}
    def references(t):
        body=''
        for r in t['sources']:
            s=sources[r['source']]
            body+=f'<p><strong>{esc(s["title"])}</strong> · páginas físicas {esc(r["pages"])}. <a href="{esc(s["path"])}#page={r["preview"][0] if r["preview"] else 1}">PDF integral no projeto</a> · <a href="{esc(s["url"])}">Fonte online</a></p>'
            for n in r['preview']:
                key=f'{s["id"]}-{n}'
                body+=f'<figure class="source-figure"><button class="slide-zoom" data-zoom="{key}" aria-label="Ampliar {esc(slides[key]["label"])}"><img data-slide="{key}" alt="{esc(slides[key]["label"])}" loading="lazy"></button><figcaption>{esc(slides[key]["label"])}</figcaption></figure>'
        return '<details class="source-pages"><summary>Consultar as páginas originais deste tópico</summary><p class="small-note">Prévias selecionadas incorporadas ao HTML. O PDF integral acompanha o projeto; as referências usam a posição física da página, incluindo capas e animações.</p>'+body+'</details>'
    sidebar='<button data-go="home">Visão geral</button><div class="side-label">PERCURSO DE ESTUDO</div>'
    for c in d['chapters']:sidebar+=f'<button class="chapter-link" data-go="{c["id"]}"><span>{c["id"]}</span>{esc(c["title"])}</button>'
    for id,title in [('bank','Banco de exercícios'),('coverage','Mapa de cobertura'),('labs','Laboratórios interativos'),('sources','Fontes e convenções')]:sidebar+=f'<button data-go="{id}">{title}</button>'
    sidebar+=f'<div class="side-footer"><a href="{esc(d["reference_notebook"])}">← Parte 1 · Análise de algoritmos</a><progress id="side-meter" max="{len(exercises)}" value="0"></progress><span id="side-progress"></span></div>'
    home=f'''<section class="page" id="page-home"><div class="hero"><div><div class="eyebrow">SIN5013 · PARTE 2 · CADERNO DE ESTUDO</div><h1>Representar.<br>Preservar.<br><em>Resolver.</em></h1><p>Das ligações de uma lista aos caminhos de um grafo. Entenda o estado, tente os exercícios e justifique cada transformação.</p><div class="button-row"><button class="primary" data-go="00">Começar pela preparação →</button><button data-go="coverage">Ver mapa de cobertura</button></div></div><div class="hero-art" aria-hidden="true"><div class="orbit"></div><div class="orbit two"></div><div class="formula">O que muda?</div><div class="art-caption">ESTADO · INVARIANTE<br>ALGORITMO · CUSTO</div></div></div>
<div class="stats"><div class="stat"><strong>{len(d['chapters']):02}</strong><span>unidades de estudo</span></div><div class="stat"><strong>{len(topics)}</strong><span>tópicos</span></div><div class="stat"><strong>{len(exercises)}</strong><span>desafios com solução</span></div><div class="stat"><strong>{len(slides)}</strong><span>páginas selecionadas</span></div></div>
<div class="section-intro"><h2>Seu percurso de estudo</h2><span>Leia → tente → confira → refaça</span></div><div class="module-grid">'''
    for c in d['chapters']:
        n=sum(len(t['exercises']) for t in c['topics'])
        home+=f'<button class="module-card" data-go="{c["id"]}"><span class="eyebrow">UNIDADE {c["id"]} · {n} DESAFIOS</span><h3>{esc(c["title"])}</h3><p>{esc(c["intro"])}</p></button>'
    home+='</div><div class="caution"><strong>COMO ESTUDAR</strong><p>Primeiro faça o exemplo à mão. Resolva os exercícios sem abrir a solução, registre a dúvida e volte ao PDF quando necessário. Os simulados praticam habilidades dos exemplos de prova; são material autoral, sem caráter de gabarito oficial.</p></div></section>'
    pages=home
    for i,c in enumerate(d['chapters']):
        body=f'<section class="page" id="page-{c["id"]}" hidden><div class="page-heading"><div class="eyebrow">UNIDADE {c["id"]} · SIN5013</div><h2>{esc(c["title"])}</h2><p>{esc(c["intro"])}</p></div><div class="topic-links">'
        body+=''.join(f'<button data-topic-link="{t["id"]}">{esc(t["title"])}</button>' for t in c['topics'])+'</div>'
        for t in c['topics']:
            body+=f'<article class="topic" id="topic-{t["id"]}"><h3>{esc(t["title"])}</h3><p class="objective">{esc(t["objective"])}</p><div class="theory">'
            for title,texts in t['sections']:body+='<h4>'+esc(title)+'</h4>'+p(texts)
            body+=f'<div class="worked-example"><h4>{esc(t["example"][0])}</h4>'+p(t['example'][1])+'</div></div>'
            body+=('<p class="eyebrow">'+esc(t.get("code_language","Código de referência"))+'</p>'+code(t["code"]) if t["code"] else "")+f'<div class="contract"><p><strong>Invariante.</strong> {esc(t["invariant"])}</p><p><strong>Custo.</strong> {esc(t["cost"])}</p></div>'
            body+=f'<div class="caution"><strong>ATENÇÃO AO CONTRATO</strong><p>{esc(t["caution"])}</p></div>'
            if t['exam']:body+='<p class="exam-link">Conexão com a prova: '+proof(t['exam'])+'</p>'
            body+=references(t)+'<h3 class="practice-heading">Agora, tente resolver</h3>'+''.join(exercise(e) for e in t['exercises'])+'</article>'
        body+='<div class="end-chapter button-row">'
        if i:body+=f'<button data-go="{d["chapters"][i-1]["id"]}">← Unidade anterior</button>'
        if i+1<len(d['chapters']):body+=f'<button class="primary" data-go="{d["chapters"][i+1]["id"]}">Próxima unidade →</button>'
        body+='</div></section>';pages+=body
    options=''.join(f'<option value="{c["id"]}">{c["id"]} · {esc(c["title"])}</option>' for c in d['chapters'])
    kinds=''.join(f'<option>{esc(k)}</option>' for k in sorted({e['kind'] for e in exercises}))
    pages+=f'''<section class="page" id="page-bank" hidden><div class="page-heading"><div class="eyebrow">TENTAR · CONFERIR · REFAZER</div><h2>Banco de exercícios</h2><p>Busque pelo enunciado ou filtre sua revisão. As soluções ficam fora da busca.</p></div><div class="filter-bar"><label>Unidade<select id="filter-chapter"><option value="all">Todas</option>{options}</select></label><label>Tipo<select id="filter-kind"><option value="all">Todos</option>{kinds}</select></label><label>Autoavaliação<select id="filter-state"><option value="all">Todas</option><option value="new">Ainda não tentei</option><option value="attempted">Tentei</option><option value="review">Revisar</option><option value="mastered">Resolvi sem ajuda</option></select></label><label>Enunciado<input id="filter-text" type="search" placeholder="Chave, ponteiro, DFS…"></label></div><p id="bank-count" role="status"></p><div class="button-row"><button id="random-exercise">Sortear entre os filtrados</button></div><p id="bank-empty" hidden>Nenhum exercício neste filtro.</p><div id="exercise-bank">{''.join(exercise(e,'bank') for e in exercises)}</div></section>'''
    rows=''
    for t in topics:
        refs='; '.join(sources[r['source']]['title']+' · p. '+r['pages'] for r in t['sources'])
        exams='; '.join(dict.fromkeys(e['exam'] for e in t['exercises'] if e['exam'])) or t['exam'] or 'Base conceitual para as questões seguintes'
        rows+=f'<tr><td><button data-topic-link="{t["id"]}">{esc(t["title"])}</button></td><td>{esc(refs)}</td><td>{proof(exams)}</td><td data-topic-state="{t["id"]}"></td></tr>'
    pages+=f'<section class="page" id="page-coverage" hidden><div class="page-heading"><h2>Mapa de cobertura</h2><p>As unidades são agrupamentos didáticos; os números das aulas originais aparecem nas fontes.</p></div><p id="coverage-progress"></p><progress id="coverage-meter" max="{len(exercises)}" value="0"></progress><div class="table-scroll"><table><thead><tr><th>Tópico</th><th>PDF e páginas físicas</th><th>Habilidade de prova</th><th>Autoavaliação</th></tr></thead><tbody>{rows}</tbody></table></div></section>'
    pages+=(ROOT/'templates/labs.html').read_text()
    pages+='<section class="page" id="page-sources" hidden><div class="page-heading"><h2>Fontes e convenções</h2><p>Teoria e exercícios são explicações autorais baseadas nas aulas. Os PDFs preservam a autoria e o conteúdo originais.</p></div><h3>Convenções deste caderno</h3><ul><li>Altura em arestas: vazio −1, folha 0; fator AVL = direita − esquerda.</li><li>ABB sem duplicatas, exceto quando o enunciado disser o contrário.</li><li>Grafos: identificadores a partir de zero; vizinhos e raízes em ordem crescente.</li><li>Ausência de aresta ponderada = ∞; peso zero pode ser válido.</li><li>Páginas citadas são físicas do PDF, incluindo animações repetidas e capas.</li></ul><h3>Como revisar</h3><p>Reveja primeiro os itens marcados como “Revisar”. Refaça um rastreamento, uma implementação e uma justificativa de cada unidade antes dos simulados. Use os laboratórios para conferir uma hipótese depois de tentar no papel.</p><h3>PDFs completos</h3><p>As prévias selecionadas funcionam no HTML isolado. Para abrir os PDFs completos offline, mantenha a pasta fontes ao lado do caderno. Cada fonte tem também um endereço online.</p><div class="source-list">'
    for s in d['sources']:pages+=f'<article class="source-card"><span class="eyebrow">{esc(s["kind"])} · {s["pages"]} páginas</span><h4>{esc(s["title"])}</h4><p>{esc(s["author"])}</p><a href="{esc(s["path"])}">PDF no projeto</a> · <a href="{esc(s["url"])}">Original online</a></article>'
    pages+='</div><p class="small-note">Os exemplos de prova orientam as habilidades praticadas; não definem uma previsão de conteúdo da avaliação. A apostila complementar usa convenções que podem diferir das dos slides principais.</p></section><section class="page" id="page-search" hidden><div class="page-heading"><h2>Resultados da busca</h2><p id="search-count" role="status"></p></div><div id="search-results"></div></section>'
    substitutions={'TITLE':esc(d['title']),'SUBTITLE':esc(d['subtitle']),'CSS':(ROOT/'templates/caderno.css').read_text(),'SIDEBAR':sidebar,'MAIN':pages,'DATA':json_script(d),'SLIDES':json_script(slides),'JS':(ROOT/'templates/caderno.js').read_text()}
    out=(ROOT/'templates/caderno.html').read_text()
    for key,value in substitutions.items():out=out.replace('@@'+key+'@@',value)
    assert '@@' not in out, 'Marcador de template não resolvido'
    target=ROOT/d['filename'];target.write_text(out)
    print(f'{target.name}: {len(topics)} tópicos, {len(exercises)} exercícios, {len(slides)} páginas; {target.stat().st_size:,} bytes')
if __name__=='__main__':main()
