#!/usr/bin/env python3
"""Renderiza somente as páginas selecionadas no manifesto, sem alterar os PDFs."""
import argparse, hashlib, json, shutil, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('conteudo',nargs='?',default='conteudo/estruturas-de-dados.json');args=parser.parse_args()
    data=json.loads((ROOT/args.conteudo).read_text())
    if not shutil.which('pdftoppm'):raise SystemExit('Instale Poppler (pdftoppm) para renderizar as fontes.')
    output=ROOT/'assets/estruturas-de-dados';output.mkdir(parents=True,exist_ok=True)
    jobs=[];manifest=[]
    for s in data['sources']:
        path=ROOT/s['path'];reader=PdfReader(path)
        assert len(reader.pages)==s['pages'],f'Contagem de páginas mudou: {path}'
        manifest.append({'id':s['id'],'path':s['path'],'url':s['url'],'pages':len(reader.pages),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        for n in s['preview_pages']:jobs.append((s,n,path))
    def render(job):
        s,n,path=job;target=output/f'{s["id"]}-{n:03}.webp'
        if target.is_file():return
        with tempfile.TemporaryDirectory() as tmp:
            prefix=Path(tmp)/'page'
            subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1500','-png',str(path),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            with Image.open(str(prefix)+'.png') as im:im.convert('RGB').save(target,'WEBP',lossless=True,method=4)
    with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(render,jobs))
    (ROOT/'conteudo/fontes-estruturas-manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(jobs)} prévias preparadas; {len(manifest)} PDFs conferidos.')
if __name__=='__main__':main()
