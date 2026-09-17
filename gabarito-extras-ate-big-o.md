# SIN5013 — Gabarito dos exercícios extras até Big O

Consulte após tentar a lista `exercicios-extras-ate-big-o.md`. As constantes das provas abaixo são exemplos; outros pares corretos também valem. Todos os custos seguem exatamente as convenções da lista.

## 1. Fundamentos

a) Entrada: vetor A com n inteiros; saída: a soma dos elementos; tamanho: quantidade de elementos. Dobrar o valor de um elemento não muda n.

b) Índice e acumulador ocupam uma quantidade constante de palavras de memória: espaço auxiliar constante. Incluindo o vetor, o espaço total cresce linearmente com n, no modelo de palavras de tamanho fixo.

c) `log₂64 = 6`; `⌊log₂20⌋ = 4`; `⌈log₂20⌉ = 5`, pois `16 ≤ 20 < 32`. De 3 a n existem `n−3+1 = n−2` inteiros.

d) As somas são `n`, `n(n+1)/2` e `2^(m+1)−1`. Na primeira há n parcelas iguais a 1, não parcelas 1, 2, …, n. Na segunda, somar a sequência com sua versão invertida produz n pares de soma n+1. Na terceira, subtraia a soma S de 2S: sobram `2^(m+1)−1`.

## 2. Máquinas e crescimento

Os tempos são `tA(n) = 5·10⁻⁹ n²` segundos e `tB(n) = 4·10⁻⁶ n` segundos.

| n | A | B |
|---|---:|---:|
| 100 | 0,00005 s | 0,0004 s |
| 10.000 | 0,5 s | 0,04 s |

Para n positivo, igualar e dividir por n dá `5·10⁻⁹ n = 4·10⁻⁶`, ou `n = 800`. A é mais rápida para `1 ≤ n < 800`; B para `n > 800`.

A taxa da máquina é apenas um fator: o número de operações de A cresce quadraticamente e o de B, linearmente. Os tempos são estimativas sob as taxas fornecidas.

## 3. Máximo

a) Após comparar os elementos de índices 1 a 6, os candidatos são `6, 8, 8, 8, 10, 10`. Há 6 comparações e 2 atualizações; o resultado é 10.

b) Comparações: `n−1` em ambos os casos. Atualizações: mínimo 0 em vetor não crescente; máximo `n−1` em vetor estritamente crescente. Para n=1, ambas as contagens são 0.

c) Inicialmente maior é o máximo do prefixo com um elemento. A cada passo, comparar o próximo elemento com o máximo anterior produz o máximo do prefixo ampliado. Quando todos foram examinados, o candidato é o máximo de A.

d) Com valores distintos, cada elemento que não é máximo precisa perder uma comparação para ser eliminado como candidato. Cada comparação elimina no máximo um candidato novo. É preciso eliminar n−1 candidatos, exigindo pelo menos n−1 comparações no pior caso. A varredura atinge esse mínimo. Para n=1 não há candidato a eliminar.

## 4. Mínimo e máximo

| Valor lido | Primeiro teste | Segundo teste | Custo | (menor, maior) depois |
|---|---|---|---:|---|
| 9 | 9 > 5: verdadeiro | Não executado | 1 | (5, 9) |
| 2 | 2 > 9: falso | 2 < 5: verdadeiro | 2 | (2, 9) |
| 9 | 9 > 9: falso | 9 < 2: falso | 2 | (2, 9) |
| 1 | 1 > 9: falso | 1 < 2: verdadeiro | 2 | (1, 9) |
| 12 | 12 > 9: verdadeiro | Não executado | 1 | (1, 12) |

Total: 8 comparações, r=2.

Há r iterações com custo 1 e n−1−r com custo 2. Logo `C = r + 2(n−1−r) = 2(n−1)−r`.

Melhor: `n−1`, em vetor estritamente crescente. Pior: `2(n−1)`, por exemplo em vetor decrescente ou constante. Todos iguais realizam o pior caso porque nenhum elemento supera estritamente o máximo.

Com dois testes independentes, ambos executam em cada iteração: `2(n−1)`. A saída continua correta. Um novo máximo não é menor que o mínimo anterior; o teste adicional será falso nesse caso.

## 5. Busca e média

a) Índice k: `k+1` comparações. Ausência: n. Melhor: 1, no índice 0. Pior: n, na última posição ou ausência.

b) Condicionado à presença, a média é `(1+2+3+4+5+6)/6 = 7/2`. Assim, `E[C] = (1/3)·6 + (2/3)·(7/2) = 13/3` comparações.

c) `E[C] = (1/2)·1 + (1/3)·2 + (1/6)·6 = 13/6`.

d) `E[C] = qn + (1−q)(n+1)/2`. A média dos extremos só coincide com a esperança em distribuições específicas. As probabilidades de cada custo precisam ser consideradas; a esperança pode ser fracionária embora cada execução use um número inteiro de comparações.

## 6. Inserção e custo selecionado

| Iteração i | Vetor após a inserção | Deslocamentos |
|---|---|---:|
| 1 | [3, 7, 5, 2, 6] | 1 |
| 2 | [3, 5, 7, 2, 6] | 1 |
| 3 | [2, 3, 5, 7, 6] | 3 |
| 4 | [2, 3, 5, 6, 7] | 1 |

Total S=6. As três atribuições fora do corpo interno executam n−1 vezes cada. As duas do corpo interno executam S vezes cada. Portanto `C = 3(n−1) + 2S`, que vale `12+12 = 24` no exemplo.

Não decrescente: S=0, portanto `Cmelhor = 3(n−1)`; para n=5, 12.

Estritamente decrescente: na iteração i, todos os i elementos anteriores são deslocados. Logo `S = Σ(i=1 até n−1)i = n(n−1)/2` e `Cpior = 3(n−1)+n(n−1) = n²+2n−3`; para n=5, 32.

Antes de cada inserção, o prefixo anterior está ordenado. Deslocar seus elementos maiores que aux abre a posição correta para aux e preserva a ordem dos demais. Inserir aux produz um prefixo ordenado com um elemento a mais. Ao final, todo o vetor está ordenado. Só i, j e aux são necessários: espaço auxiliar constante.

## 7. Inserção no Modelo U completo

Defina `S = n(n−1)/2` para a coluna de ordem inversa.

| Operação | Não decrescente | Estritamente decrescente |
|---|---:|---:|
| i ← 1 | 1 | 1 |
| i < n | n | n |
| aux ← A[i] | n−1 | n−1 |
| j ← i | n−1 | n−1 |
| j > 0 | n−1 | S+n−1 |
| aux < A[j−1] | n−1 | S |
| A[j] ← A[j−1] | 0 | S |
| j ← j−1 | 0 | S |
| A[j] ← aux | n−1 | n−1 |
| i ← i+1 | n−1 | n−1 |
| retorne A | 1 | 1 |

Não decrescente: o teste j>0 é verdadeiro, mas a comparação de valores falha imediatamente em cada iteração externa. Somando a coluna, `Tmelhor(n) = 1+n+6(n−1)+1 = 7n−4`.

Ordem inversa: na iteração i, j>0 é testado i+1 vezes; a comparação de valores é feita i vezes. Quando j=0, o curto-circuito evita um acesso ao índice −1. Somando: `Tpior(n) = 1+n+5(n−1)+4S+1 = 2n²+4n−3`.

Conferência: n=1 custa 3 em ambos (inicialização, teste externo falso, retorno). Para n=2, o caso ordenado custa 10. O inverso custa 13: inicialização externa 1, testes externos 2, aux/j/inserção/incremento externo 4, testes j>0 2, comparação de valores 1, deslocamento e decremento 2, retorno 1.

O exercício 6 exclui controle externo, testes internos e retorno. São duas medidas legítimas, mas diferentes: uma fórmula só representa as operações que sua definição inclui.

## 8. Laço simples

| Operação | Frequência |
|---|---:|
| s ← 0 | 1 |
| i ← 0 | 1 |
| i < n | n+1 |
| s ← s + A[i] | n |
| i ← i+1 | n |
| retorne s | 1 |

`T(n) = 1+1+(n+1)+n+n+1 = 3n+4`. Para n=1: 7; para n=4: 16.

Para todo n≥1, `0 ≤ 3n+4 ≤ 3n+4n = 7n`. Escolha c=7, n₀=1. Logo `T ∈ O(n)`.

## 9. Laços consecutivos

A saída é 2n. As três inicializações custam 3; os dois laços somam `2(n+1)` testes e `4n` atribuições no corpo; o retorno custa 1.

`T(n) = 3+2(n+1)+4n+1 = 6n+6`.

Para n≥1, `0 ≤ 6n+6 ≤ 12n`: c=12 e n₀=1 provam pertencimento a O(n). Laços consecutivos somam seus custos. A existência de dois laços não implica n² execuções.

## 10. Triângulo

a) As repetições internas são 1, 2, 3, 4. Saída: 10.

b) Defina `S = n(n+1)/2`. Para cada i, o teste interno ocorre i+1 vezes. Total: `Σ(i=1 até n)(i+1) = S+n`.

c) Inicializações s e i: 2; testes externos: n+1; inicializações j: n; testes internos: S+n; incrementos s e j: 2S; incrementos i: n; retorno: 1.

`T(n) = 2+(n+1)+n+(S+n)+2S+n+1 = 3S+4n+4 = (3n²+11n+8)/2`.

Para n=4, o custo é 50. Para todo n≥1, substitua n e 1 por limites superiores n²: `0 ≤ T(n) ≤ (3+11+8)n²/2 = 11n²`. Servem c=11 e n₀=1.

## 11. Dobrando o índice

a) Valores testados: 1, 2, 4, 8, 16. O último falha. São 4 iterações, e q=4.

b) Na iteração de número k+1, começando k=0, temos i=2ᵏ. O corpo executa enquanto `2ᵏ ≤ n`, ou `k ≤ log₂ n`. Há `L = ⌊log₂ n⌋+1` iterações.

Duas inicializações, L+1 testes, 2L atribuições internas e um retorno: `T(n) = 3L+4 = 3⌊log₂ n⌋+7`.

Para n=1: L=1, T=7; n=8: L=4, T=16; n=13: L=4, T=16.

c) Para n≥2, log₂n≥1. Portanto `0 ≤ T(n) ≤ 3log₂n+7 ≤ 10log₂n`. Escolha c=10, n₀=2. Isso prova `T ∈ O(log₂ n)` sem exigir que a desigualdade valha em n=1.

## 12. Polinômios

Em todos os itens, use n₀=1. As funções são não negativas nesse domínio.

a) `9n+14 ≤ 9n+14n = 23n`: c=23.

b) `4n²+7n+9 ≤ 4n²+7n²+9n² = 20n²`: c=20.

c) `3n³+2n²+20 ≤ 3n³+2n³+20n³ = 25n³`: c=25.

d) Pelo item b e por n²≤n³, `4n²+7n+9 ≤ 20n³`: c=20.

Big O expressa um limite superior, que pode ser folgado. Uma função pode pertencer a várias dessas classes. O limite quadrático informa mais aqui que o cúbico, pois restringe mais seu crescimento.

## 13. Termos negativos

a) Para n≥3, `5n²−12n+4 = n(5n−12)+4 ≥ 0`. Além disso, `−12n+4 ≤ 0`, de modo que `5n²−12n+4 ≤ 5n²`. Servem c=5 e n₀=3.

b) Para n≥5, `0 ≤ 7n−30 ≤ 7n`. Servem c=7 e n₀=5.

c) Não. Em n=1 a função do item a vale −3, violando a não negatividade exigida; em n=2 ela vale 0. O par (5,2) também funciona: `5n²−12n+4 = (n−2)(5n−2) ≥ 0` para n≥2. Não é necessário achar o menor limiar para demonstrar pertencimento.

## 14. Constante fixada

A desigualdade é `6n+25 ≤ cn`, ou `25 ≤ (c−6)n`.

a) c=7 exige n≥25. Menor n₀: 25.

b) c=11 exige n≥5. Menor n₀: 5.

c) c=6 exigiria 25≤0; c=5 exigiria 25≤−n. Nenhum limiar funciona em qualquer desses casos.

d) Não. Pertencer exige que exista algum par válido. Os pares dos itens a e b já provam pertencimento, apesar de outras escolhas falharem.

## 15. Provas com falhas

a) c precisa ser constante em relação a n. Usar c=n não atende à definição. A conclusão é falsa; a prova de não pertencimento está no exercício 16.

b) A conclusão é verdadeira, mas três exemplos não provam uma afirmação para todos os inteiros após o limiar. Corrija com `0 ≤ 8n+3 ≤ 8n+3n = 11n` para todo n≥1. Logo c=11, n₀=1.

c) A função de melhor caso é constante, mas não descreve todas as entradas. Em uma busca sem sucesso há n comparações, número que ultrapassa qualquer constante fixa para n suficientemente grande. O pior caso é n e pertence a O(n), com c=1, n₀=1.

## 16. Não pertencimento

a) Sejam c>0 e inteiro n₀≥1 quaisquer. Escolha `n = max(n₀, ⌊c⌋+1)`. Então n>c e n≥n₀, de modo que `n² > cn`. Toda tentativa de escolher constantes falha. Logo `n² ∉ O(n)`.

b) Escolha `n = max(n₀, ⌊c/3⌋+1)`. Temos 3n>c e, multiplicando por n>0, `3n² > cn`. Assim `3n²+n > cn`, o que viola o limite. Logo `3n²+n ∉ O(n)`.

c) Dadas c>0 e n₀≥1, tome inteiro `k = max(⌊c⌋+1, ⌈log₂n₀⌉)` e n=2ᵏ. Então n≥n₀ e `log₂n = k > c = c·1`. Logo `log₂ n ∉ O(1)`.

A ordem lógica é essencial: dadas quaisquer constantes candidatas, encontramos uma entrada posterior ao limiar que as derrota.

## 17. Propriedades

a) Das hipóteses, existem a,b>0 e limiares N₁,N₂ tais que `0 ≤ f(n) ≤ a·g(n)` após N₁ e `0 ≤ g(n) ≤ b·h(n)` após N₂. Para `n ≥ max(N₁,N₂)`, temos `0 ≤ f(n) ≤ a·g(n) ≤ ab·h(n)`. Escolha c=ab e n₀=max(N₁,N₂).

b) Existem a,b>0 e limiares N₁,N₂ com `f(n) ≤ a·h(n)` e `g(n) ≤ b·h(n)`. Após o maior limiar, some: `0 ≤ f(n)+g(n) ≤ (a+b)h(n)`. Escolha c=a+b e n₀=max(N₁,N₂).

c) Para n≥1, `0 ≤ n²+5n+8 ≤ n²+5n²+8n² = 14n²`. Logo c=14, n₀=1.

## 18. Revisão integrada

Separe primeiro o custo que acontece mesmo quando nenhuma posição é positiva. Há 2 inicializações, n+1 testes externos, n testes A[i]>0, n incrementos i e 1 retorno: `4+3n`.

Quando o índice i é positivo, o bloco adicional tem 1 inicialização j, i+2 testes internos e 2(i+1) atribuições internas. Custo adicional: `1+(i+2)+2(i+1) = 3i+5`.

a) P={0,2}. O índice 0 acrescenta 1 à soma; o índice 2 acrescenta 3. Saída: 4. Custo: `4+3·4+(3·0+5)+(3·2+5) = 16+5+11 = 32`.

b) `T(A) = 3n+4 + Σ(i ∈ P)(3i+5)`. A saída, que é uma medida diferente, vale `Σ(i ∈ P)(i+1)`.

c) Cada parcela adicional é positiva. Melhor caso: nenhum elemento positivo, como um vetor de zeros. `Tmelhor(n) = 3n+4`.

Pior caso: todos positivos, como um vetor de uns. Use `Σ(i=0 até n−1)i = n(n−1)/2`:

`Tpior(n) = 3n+4+3n(n−1)/2+5n = (3n²+13n+8)/2`.

d) Para n≥1, `0 ≤ Tmelhor(n) ≤ 7n`: c=7, n₀=1. Também `0 ≤ Tpior(n) ≤ (3+13+8)n²/2 = 12n²`: c=12, n₀=1.

Não se pode estender o limite linear do melhor caso a todas as entradas. No vetor de uns o custo é pelo menos `(3/2)n²`, que excede cn quando n>2c/3, qualquer que seja a constante c.

e) Cada parcela 3i+5 aparece com probabilidade 1/2. Pela soma das contribuições médias:

`E[T] = 3n+4 + (1/2)Σ(i=0 até n−1)(3i+5)`

`E[T] = 3n+4 + 3n(n−1)/4 + 5n/2 = (3n²+19n+16)/4`.

A independência entre posições não é necessária para somar essas esperanças; bastam as probabilidades marginais especificadas. Neste exemplo particular a média coincide com a média dos extremos porque cada contribuição adicional tem probabilidade 1/2. Isso não é uma regra geral para caso médio.
