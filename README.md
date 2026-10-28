# SIN5013 · Caderno de estudo

Caderno interativo de estudo de SIN5013 (Análise de Algoritmos e Estruturas de Dados),
publicado em **https://guilhermealj.github.io/sin5013-estudo/**

## Conteúdo

| Arquivo | Descrição |
| --- | --- |
| `SIN5013-estruturas-de-dados.html` | Parte 2: 10 unidades, 30 tópicos, 94 desafios com solução, dois simulados e quatro laboratórios. HTML autocontido com páginas selecionadas dos PDFs. |
| `docs/PADRAO-CADERNOS.md` | Padrão editorial e técnico para produzir e ampliar os cadernos. |
| `conteudo/estruturas-de-dados.json` | Conteúdo editável e mapa de fontes da parte 2. |
| `SIN5013-estudo.html` | Caderno completo: teoria, demonstrações, 113 desafios resolvidos, laboratórios interativos e as 274 páginas originais embutidas. Arquivo único e autocontido (~22 MB), sem dependências externas. |
| `SIN5013-caderno-pratico-v2.html` | Caderno prático: 49 exercícios com resolução passo a passo, dois simulados e plano de estudo, com modo escuro. Arquivo único (~0,9 MB). Publicado em https://guilhermealj.github.io/sin5013-estudo/SIN5013-caderno-pratico-v2.html |
| `pratica.py` | Implementações de referência com verificações. Python 3, sem dependências. Execute com `python pratica.py`. |
| `exercicios-extras-ate-big-o.md` | Exercícios adicionais até notação assintótica. |
| `gabarito-extras-ate-big-o.md` | Gabarito dos exercícios adicionais. |
| `fontes/` | PDFs originais das aulas (cópias opcionais). |
| `LEIA-ME.txt` | Instruções de uso offline. |

## Uso offline

Baixe `SIN5013-estudo.html` e abra no navegador. Não requer instalação, servidor ou internet:
imagens, estilos e scripts estão embutidos no próprio arquivo.

O progresso e as anotações ficam no armazenamento local do navegador. Use **Exportar progresso**
para guardar uma cópia JSON e **Importar** para restaurá-la em outro navegador ou máquina.

## Fontes

Aulas 02, 03, 04, 05, 06, 07, 09 e 10 de Norton T. Roman e Luciano A. Digiampietri (2023) —
274 páginas. As explicações, exercícios adicionais, resoluções e ferramentas interativas foram
elaboradas para este caderno.

## Parte 2: estruturas de dados

A página inicial oferece os dois cadernos. O endereço da primeira parte permanece igual. A nova parte cobre memória e ponteiros, listas sequenciais e ligadas, listas circulares, pilhas, filas, árvores binárias, ABB, AVL, grafos, matrizes e listas de adjacências, DFS, BFS, componentes, topologia, heaps, Prim, Kruskal, relaxamento, Dijkstra, Bellman-Ford e Floyd-Warshall.

As 18 aulas principais, quatro materiais de apoio e quatro exemplos de prova estão em `fontes/estruturas-de-dados/`. O mapa de cobertura associa os tópicos às páginas físicas dos PDFs e às habilidades das questões. Os exercícios e simulados são autorais; não são gabaritos oficiais nem previsão da prova.

O HTML isolado contém estilos, scripts, conteúdo e prévias selecionadas. Para consultar os PDFs integrais offline, baixe também a pasta `fontes`; as fontes online continuam indicadas. O progresso da parte 2 usa armazenamento próprio e não sobrescreve o da parte 1.

## Padrão e manutenção

Leia [o padrão de cadernos](docs/PADRAO-CADERNOS.md). Edite o JSON e os templates, depois regenere:

```bash
python3 scripts/preparar_fontes.py
python3 scripts/gerar_caderno.py
python3 scripts/verificar_material.py
```

A geração usa apenas Python padrão. Preparar novas prévias exige Poppler (`pdftoppm`), Pillow e pypdf; prévias já existentes estão versionadas. O manifesto registra URL, número de páginas e SHA-256 dos PDFs completos.

A verificação independente cobre rastreamentos de DFS/BFS, fila circular e heap, custos de AGM por enumeração de árvores, caminhos por Floyd-Warshall e compilação dos 18 trechos de respostas C. Os casos de remoção em ABB também são executados com sanitizadores de memória e comportamento indefinido. Esse comando precisa de `cc` (C11).
