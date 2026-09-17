# SIN5013 — Exercícios extras até Big O

18 exercícios autorais, organizados a partir da preparação do caderno, da aula 02 e da aula 03 até a página 23. O recorte termina em Big O; as outras notações e recorrências ficam para outra lista.

**Como treinar:** resolva primeiro os enunciados. Consulte o arquivo `gabarito-extras-ate-big-o.md` depois de escrever suas contas e justificativas. Sugestão: faça os blocos 1–6, 7–11 e 12–18 em sessões separadas.

## Convenções

- `n` é inteiro e `n ≥ 1`, salvo indicação diferente. Vetores usam índices de `0` a `n−1`.
- `←` representa atribuição. `para i de a até b` inclui os dois extremos e não executa o corpo se `a > b`.
- Quando o exercício pede apenas comparações de valores ou deslocamentos, conte somente isso.
- **Modelo U**, quando solicitado: cada atribuição, cada avaliação de uma comparação e cada `retorne` custa 1. Uma atribuição como `s ← s + A[i]` custa 1 no total; acessos e aritmética dentro dela não têm custo adicional. Cada incremento também é uma atribuição. Não há cobrança separada por `se`, `senão` ou por voltar ao início do laço.
- No Modelo U, conte o último teste falso do `enquanto`. Na expressão `P e Q`, há curto-circuito: avalie `Q` somente se `P` for verdadeiro, cobrando cada comparação que realmente ocorrer.
- Nas provas, use a definição: **f ∈ O(g)** se existem constantes `c > 0` e inteiro `n₀ ≥ 1` tais que `0 ≤ f(n) ≤ c·g(n)` para todo inteiro `n ≥ n₀`. As constantes não podem depender de `n`.

Uma resposta de custo exato deve mostrar **frequências → soma → fórmula**. Uma prova de pertencimento deve mostrar **c e n₀ → desigualdade válida para todo n ≥ n₀ → conclusão**. Testar alguns números não substitui a prova.

## Bloco A — Fundamentos e análise de entradas

### 1. Tamanho, memória, logaritmos e somas · Aquecimento

Um algoritmo recebe um vetor com `n` inteiros de tamanho fixo e calcula sua soma usando apenas um índice e um acumulador.

a) Defina entrada, saída e tamanho da entrada. Se o maior elemento dobrar, `n` necessariamente dobra?

b) Como crescem o espaço auxiliar e o espaço total quando `n` aumenta?

c) Calcule `log₂64`, `⌊log₂20⌋`, `⌈log₂20⌉` e a quantidade de inteiros no intervalo de `3` a `n`, para `n ≥ 3`.

d) Obtenha formas fechadas para `Σ(i=1 até n) 1`, `Σ(i=1 até n) i` e `Σ(k=0 até m) 2ᵏ`, com `m ≥ 0`. Explique por que a primeira soma não vale `n(n+1)/2`.

### 2. Custo abstrato e tempo estimado · Aquecimento

O algoritmo A faz `3n²` operações em uma máquina que executa `6·10⁸` operações por segundo. B faz `80n` operações em uma máquina que executa `2·10⁷` operações por segundo. Considere essas taxas constantes.

a) Estime os tempos para `n = 100` e `n = 10.000`.

b) Ache o tamanho positivo em que os tempos se igualam e indique qual combinação é mais rápida antes e depois desse ponto.

c) Explique por que ter uma máquina mais rápida não garante o menor tempo para todos os tamanhos.

### 3. Máximo: rastreamento, custo e otimalidade · Essencial

```text
maior ← A[0]
para i de 1 até n−1:
    se A[i] > maior:
        maior ← A[i]
retorne maior
```

a) Execute em `[6, 2, 8, 8, 3, 10, 1]`. Anote o candidato após cada comparação, o número de comparações entre valores e o de atualizações de `maior`, excluindo a inicialização.

b) Dê o custo exato em comparações de valores no melhor e no pior caso. Faça o mesmo para as atualizações e dê exemplos de entradas.

c) Explique por que `maior` contém a resposta ao final.

d) Para valores distintos e algoritmos que descobrem a ordem apenas comparando pares, prove que encontrar o máximo exige pelo menos `n−1` comparações no pior caso. O algoritmo acima atinge esse mínimo?

### 4. Mínimo e máximo: o efeito do senão · Essencial

Conte apenas comparações entre valores.

```text
menor ← A[0]
maior ← A[0]
para i de 1 até n−1:
    se A[i] > maior:
        maior ← A[i]
    senão se A[i] < menor:
        menor ← A[i]
retorne (menor, maior)
```

a) Rastreie `[5, 9, 2, 9, 1, 12]`, anotando os testes executados em cada iteração.

b) Seja `r` o número de novos máximos estritos após o primeiro elemento. Derive o custo em função de `n` e `r`.

c) Dê melhor e pior custo, com entradas que os realizem. Qual é o custo se todos os valores forem iguais?

d) Se o segundo teste fosse um `se` independente, qual seria a contagem? A saída continuaria correta?

### 5. Busca sequencial: caso médio de verdade · Essencial

Uma busca examina um vetor de comprimento `n`, da esquerda para a direita, e retorna no primeiro acerto. Conte apenas testes `A[i] = x`. Quando presente, o alvo aparece exatamente uma vez.

a) Dê os custos de encontrar o alvo na posição de índice `k`, de não encontrá-lo, do melhor e do pior caso.

b) Para `n = 6`, o alvo está ausente com probabilidade `1/3`. Condicionado à presença, as seis posições são equiprováveis. Calcule o custo médio exato.

c) Em outra distribuição, sem ausências, as probabilidades dos índices `0`, `1` e `5` são `1/2`, `1/3` e `1/6`. Calcule a média.

d) Generalize o item b para tamanho `n` e probabilidade de ausência `q`. Explique por que a média dos custos mínimo e máximo não resolve todo problema de caso médio.

### 6. Inserção: deslocamentos e contagem selecionada · Essencial

Use este algoritmo nos exercícios 6 e 7:

```text
i ← 1
enquanto i < n:
    aux ← A[i]
    j ← i
    enquanto j > 0 e aux < A[j−1]:
        A[j] ← A[j−1]
        j ← j−1
    A[j] ← aux
    i ← i+1
retorne A
```

a) Execute em `[7, 3, 5, 2, 6]`. Mostre o vetor após cada iteração externa e conte os deslocamentos `A[j] ← A[j−1]`.

b) Neste exercício, cobre 1 apenas por cada execução de `aux ← A[i]`, `j ← i`, `A[j] ← A[j−1]`, `j ← j−1` e `A[j] ← aux`. Expresse esse custo usando `n` e o total `S` de deslocamentos. Calcule-o para o vetor do item a.

c) Derive o custo exato dessa contagem selecionada para vetores não decrescentes e para vetores estritamente decrescentes. Avalie ambos para `n = 5`.

d) Justifique por que o prefixo fica ordenado e indique o espaço auxiliar.

## Bloco B — Custo exato com controle dos laços

### 7. Inserção: agora conte todos os testes · Desafio

Use o algoritmo do exercício 6, agora com o **Modelo U** completo.

a) Em uma entrada não decrescente, monte uma tabela com a frequência de cada atribuição, comparação e retorno. Derive `Tmelhor(n)`.

b) Repita para uma entrada estritamente decrescente, obtendo `Tpior(n)`. Conte separadamente `j > 0` e `aux < A[j−1]`.

c) Confira as fórmulas para `n = 1` e `n = 2` por execução manual.

d) Explique por que a fórmula de custo do exercício 6 não deve ser reutilizada como o total deste exercício.

### 8. Laço simples: o teste final · Essencial

No **Modelo U**, analise:

```text
s ← 0
i ← 0
enquanto i < n:
    s ← s + A[i]
    i ← i+1
retorne s
```

a) Faça a tabela de frequências e derive o custo exato `T(n)`.

b) Confira para `n = 1` e `n = 4`.

c) Prove `T ∈ O(n)` com constantes explícitas.

### 9. Dois laços consecutivos · Essencial

No **Modelo U**, analise:

```text
s ← 0
i ← 1
enquanto i ≤ n:
    s ← s+1
    i ← i+1
j ← 1
enquanto j ≤ n:
    s ← s+1
    j ← j+1
retorne s
```

a) Qual é o valor retornado? Qual é o custo exato?

b) Prove que o custo pertence a `O(n)`.

c) Avalie a afirmação: “Há dois laços de tamanho n, portanto o custo é quadrático”.

### 10. Laços dependentes: região triangular · Essencial

No **Modelo U**, analise:

```text
s ← 0
i ← 1
enquanto i ≤ n:
    j ← 1
    enquanto j ≤ i:
        s ← s+1
        j ← j+1
    i ← i+1
retorne s
```

a) Para `n = 4`, liste quantas vezes o corpo interno executa em cada iteração externa e determine a saída.

b) Dê o total de testes `j ≤ i`, incluindo os falsos.

c) Monte a soma de todos os custos e simplifique `T(n)`.

d) Prove `T ∈ O(n²)`.

### 11. Dobrando o índice · Desafio

No **Modelo U**, analise:

```text
i ← 1
q ← 0
enquanto i ≤ n:
    q ← q+1
    i ← 2*i
retorne q
```

a) Liste os valores de `i` testados para `n = 13`, incluindo o teste falso. Qual é a saída?

b) Obtenha o número exato de iterações usando piso e logaritmo. Derive `T(n)` e confira para `n = 1`, `8` e `13`.

c) Prove `T ∈ O(log₂ n)`. Escolha cuidadosamente `n₀`, pois `log₂1 = 0`.

## Bloco C — Provas formais e revisão integrada

### 12. Pertencimento de polinômios · Essencial

Prove pela definição, indicando um par válido `(c, n₀)` em cada item:

a) `9n + 14 ∈ O(n)`.

b) `4n² + 7n + 9 ∈ O(n²)`.

c) `3n³ + 2n² + 20 ∈ O(n³)`.

d) `4n² + 7n + 9 ∈ O(n³)`.

Explique por que b e d podem ser verdadeiros simultaneamente e qual limite informa mais sobre essa função.

### 13. Termos negativos e limiar · Essencial

a) Prove `5n² − 12n + 4 ∈ O(n²)`. Verifique tanto a não negatividade quanto o limite superior no intervalo escolhido.

b) Prove `7n − 30 ∈ O(n)`.

c) Para o item a, a escolha `(c, n₀) = (5, 1)` satisfaz a definição adotada nesta lista? Justifique.

### 14. Quando c já foi escolhido · Desafio

Para `f(n) = 6n + 25`, queremos provar `f ∈ O(n)`.

a) Fixando `c = 7`, encontre o menor inteiro `n₀ ≥ 1` que funciona.

b) Repita com `c = 11`.

c) Existe algum `n₀` que funcione com `c = 6`? E com `c = 5`?

d) Falhar com um valor particular de `c` basta para provar não pertencimento?

### 15. Corrija três provas · Essencial

Identifique o erro e corrija a conclusão ou a demonstração:

a) “`n² ∈ O(n)`, pois basta escolher `c = n` e `n₀ = 1`.”

b) “Verifiquei `8n + 3 ≤ 11n` para `n = 1, 2, 3`. Logo `8n + 3 ∈ O(n)`.”

c) “O melhor caso de uma busca sequencial custa 1. Portanto qualquer execução dessa busca custa `O(1)`.”

### 16. Não pertencimento pela definição · Desafio

a) Prove `n² ∉ O(n)`. Parta de constantes arbitrárias `c > 0` e `n₀ ≥ 1` e construa um inteiro `n ≥ n₀` que viole a desigualdade.

b) Faça o mesmo para `3n² + n ∉ O(n)`.

c) Prove `log₂ n ∉ O(1)` escolhendo uma potência de 2 suficientemente grande.

### 17. Propriedades que você deve conseguir demonstrar · Desafio

Considere funções não negativas no domínio e constantes positivas.

a) Se `f ∈ O(g)` e `g ∈ O(h)`, prove `f ∈ O(h)`, construindo a constante e o limiar a partir das duas hipóteses.

b) Se `f ∈ O(h)` e `g ∈ O(h)`, prove `f + g ∈ O(h)`.

c) Use b, ou uma desigualdade direta, para provar `n² + 5n + 8 ∈ O(n²)`.

### 18. Revisão integrada: entrada, custo exato e Big O · Desafio

No **Modelo U**, analise:

```text
s ← 0
i ← 0
enquanto i < n:
    se A[i] > 0:
        j ← 0
        enquanto j ≤ i:
            s ← s+1
            j ← j+1
    i ← i+1
retorne s
```

a) Rastreie `A = [2, −1, 4, 0]`. Dê a saída e o custo exato total.

b) Seja `P` o conjunto dos índices com `A[i] > 0`. Derive `T(A)` usando um somatório sobre `P`.

c) Dê entradas que realizem melhor e pior caso para tamanho `n`. Derive as duas funções exatas.

d) Prove que o melhor caso pertence a `O(n)` e o pior a `O(n²)`. A classificação do melhor caso permite concluir que todas as entradas têm custo `O(n)`?

e) Se cada posição for positiva com probabilidade `1/2`, calcule o custo médio. Use a média ponderada do custo adicional de cada posição.

## Antes de conferir

- Você declarou o que contou?
- Incluiu os testes falsos e respeitou o curto-circuito?
- Distinguiu somar laços consecutivos de somar as execuções dos laços aninhados?
- No caso médio, usou as probabilidades fornecidas?
- Em cada pertencimento, exibiu constantes e uma desigualdade para todos os tamanhos após o limiar?
- Em cada não pertencimento, mostrou por que qualquer escolha de constantes falha?
