# Padrão de cadernos HTML · SIN5013

Este padrão foi extraído de `SIN5013-estudo.html`, o caderno da primeira parte do semestre. A nova parte usa o mesmo sistema visual de fundo claro, verde escuro, tipografia serifada para a teoria, navegação lateral e prática com soluções recolhíveis. O caderno de análise de algoritmos permanece disponível em seu endereço original.

## Unidade editorial

Cada **unidade** agrupa tópicos que dependem uns dos outros; sua numeração não substitui a das aulas originais. Cada **tópico** deve conter, nesta ordem:

1. Um título que diga o que o aluno aprenderá a fazer e um objetivo verificável.
2. Conceitos necessários antes de símbolos ou código novos. Cada seção desenvolve uma ideia; não basta transcrever tópicos de um slide.
3. Um exemplo pequeno resolvido com estados intermediários, convenções e saída explícita.
4. Código de referência quando ajudar a entender a operação. Dizer a linguagem, os tipos necessários, a política de erro e as pré-condições. Não apresentar pseudocódigo como C compilável.
5. Invariante e custo, distinguindo busca, atualização, representação e espaço auxiliar.
6. Um erro frequente ou caso de fronteira explicado.
7. Fonte, páginas físicas do PDF e prévias selecionadas. Diferenciar o conteúdo da fonte de explicações e exercícios autorais.
8. No mínimo três exercícios: rastreamento; construção ou implementação; justificativa, contraexemplo ou depuração. A composição pode variar conforme o tópico.

Todo exercício tem identificador estável, enunciado autossuficiente, dica específica e solução em pelo menos dois passos. Exercícios de código devem fornecer código na solução quando o enunciado pede uma implementação. Evitar dicas genéricas como “releia o exemplo”. Não exigir uma técnica antes de ensiná-la.

## Como usar as provas

Mapear cada questão para uma **habilidade**, não para uma previsão de prova futura. Exemplos desta parte: rastrear indireção em C; retirar um nó sem perder ligações; calcular altura; escolher uma rotação; ler matriz e listas; contar vizinhos sem repetição; interpretar predecessores; separar AGM de caminhos mínimos.

Criar exercícios novos com dados completos. Marcar explicitamente a conexão com a questão usada como referência. Apresentar os simulados como autorais e a solução como autocorreção, sem alegar gabarito oficial. Nos grafos, fixar direção, pesos, origem, ordem dos vizinhos e desempates. Em árvores, fixar altura, fator AVL, duplicatas e predecessor/sucessor de remoção.

## Convenções de estruturas de dados

- Índices começam em zero. Uma posição física não é um valor armazenado nem a posição lógica de uma fila circular.
- C passa argumentos por valor. Alterar um objeto apontado e alterar o ponteiro do chamador são operações distintas.
- Altura: árvore vazia −1 e folha 0. Fator AVL = altura direita menos altura esquerda.
- ABB sem duplicatas, salvo declaração contrária. Remoção com dois filhos usa o maior à esquerda quando esse é o contrato do exercício.
- Grafos dirigidos: linha da matriz e índice da lista indicam origem. Ausência ponderada é ∞; zero pode ser peso válido.
- DFS/BFS: vizinhos e raízes em ordem crescente quando a resposta precisar ser única.
- Complexidade sempre informa a representação. Separar n elementos, V vértices, E arestas, altura h e capacidade C.

## Organização do projeto

| Caminho | Responsabilidade |
| --- | --- |
| `conteudo/estruturas-de-dados.json` | Fonte editável de teoria, exercícios, referências e metadados. |
| `templates/caderno.html`, `.css`, `.js` | Estrutura, identidade visual e comportamento reutilizável. |
| `templates/labs.html` | Interfaces dos quatro laboratórios desta parte. |
| `scripts/preparar_fontes.py` | Confere PDFs, registra hashes e renderiza as páginas selecionadas. |
| `scripts/gerar_caderno.py` | Valida o conteúdo e gera o HTML autocontido. |
| `assets/estruturas-de-dados/` | Prévias WebP dos PDFs, embutidas durante a geração. |
| `fontes/estruturas-de-dados/` | PDFs completos das aulas, apoios e provas. |
| `conteudo/fontes-estruturas-manifesto.json` | Origem, páginas e SHA-256 de cada PDF. |

O HTML gerado é um resultado de compilação editorial. Faça as edições no JSON ou nos templates, depois regenere; editar só o HTML perde as alterações na próxima geração. Nenhum conteúdo é buscado na internet para abrir o caderno.

## Contrato do JSON

Na raiz: `schema_version`, `id`, `title`, `subtitle`, `storage_key`, `filename`, `reference_notebook`, `reference_url`, `course_url`, `chapters`, `sources`. Cada unidade tem `id`, `title`, `intro`, `topics`.

Cada tópico tem `id`, `title`, `objective`, `sections` (pares título/lista de parágrafos), `example` (título/lista de passos), `invariant`, `cost`, `caution`, `code`, `code_language` (quando houver código), `sources`, `exercises` e `exam`. Uma referência de tópico tem `source`, `pages` (intervalo legível) e `preview` (números físicos a incorporar).

Cada exercício tem `id`, `chapter`, `topic`, `title`, `kind`, `prompt`, `hint`, `steps`, `answer_code` e `exam`. Cada fonte tem `id`, `title`, `path`, `url`, `pages`, `author`, `kind` e `preview_pages`. As prévias da fonte são a união das páginas selecionadas pelos tópicos.

IDs não podem se repetir nem mudar depois de publicados: eles conectam links e progresso. Conteúdos novos precisam de `id` e `storage_key` próprios. Não reaproveitar a chave de armazenamento da parte 1. O formato exportado também identifica o caderno para impedir importações no material errado.

## Produzir outra parte ou ampliar esta

1. Copiar os PDFs completos, registrar as URLs de origem e ler as páginas relevantes, incluindo figuras e código.
2. Fazer a matriz aula → tópico → habilidade → exercício antes de redigir. Identificar lacunas, materiais opcionais e convenções divergentes.
3. Escrever no JSON seguindo a unidade editorial. Acrescentar IDs novos sem renumerar os antigos. Atualizar as páginas de prévia nas fontes.
4. Renderizar as prévias e gerar o HTML pelos comandos abaixo. Python 3; a geração usa apenas a biblioteca padrão. A preparação das imagens precisa de Poppler, Pillow e pypdf. A verificação dos trechos C usa um compilador `cc` com C11 e sanitizadores.

```bash
python3 scripts/preparar_fontes.py
python3 scripts/gerar_caderno.py
python3 scripts/verificar_material.py
```

Os scripts também recebem o caminho de outro JSON como primeiro argumento. Ao criar outro caderno, adaptar os laboratórios e os metadados do template ao assunto. Isso é uma estrutura editorial reutilizável; o conteúdo e os laboratórios não são produzidos automaticamente a partir de qualquer PDF.

## Critérios de entrega

- Objetivos, exemplos e exercícios cobrem os tópicos declarados; cada referência aponta para o PDF e a posição física correta.
- Soluções numéricas e rastreamentos são conferidos de forma independente; códigos recebem os casos vazio, um elemento, ausente, cheio e transição de raiz/cabeça relevantes.
- HTML tem IDs e labels únicos, nenhum arquivo visual externo obrigatório e nenhuma dependência de servidor.
- Busca usa teoria e enunciados, nunca dicas/soluções. Dicas e soluções começam fechadas.
- Anotações e autoavaliação persistem; exportação e importação identificam o caderno. Armazenamento bloqueado gera aviso e mantém a sessão utilizável.
- Conferir a página em tela larga e estreita, navegação por teclado, tabelas, impressão e laboratórios. Prévias devem estar legíveis e abrir ampliadas.
- O mapa mostra exatamente a cobertura implementada. Publicação no GitHub Pages deve preservar os endereços antigos.
