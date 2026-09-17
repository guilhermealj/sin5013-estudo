"""SIN5013 - implementações de referência e verificações.

Python 3, somente biblioteca padrão. Execute: python pratica.py
Tente escrever sua solução antes de consultar este arquivo.
Contadores explicitam sua unidade; não são tempos de CPU.
"""
from math import factorial, log2
from itertools import permutations

def maximo(a):
    if not a:
        raise ValueError('O vetor precisa conter pelo menos um elemento.')
    maior = a[0]
    comparacoes = atualizacoes = 0
    for i in range(1, len(a)):
        x = a[i]
        comparacoes += 1
        if x > maior:
            maior = x
            atualizacoes += 1
    return maior, comparacoes, atualizacoes

def minmax_else(a):
    if not a:
        raise ValueError('Vetor vazio.')
    menor = maior = a[0]
    comparacoes = 0
    # Índices evitam copiar a entrada.
    for i in range(1, len(a)):
        comparacoes += 1
        if a[i] > maior:
            maior = a[i]
        else:
            comparacoes += 1
            if a[i] < menor:
                menor = a[i]
    return (menor, maior), comparacoes

def insercao(entrada):
    # Esta cópia permite preservar a entrada na referência.
    # O algoritmo in-place em si usa apenas espaço auxiliar constante.
    a = list(entrada)
    deslocamentos = testes_j = testes_chave = 0
    for i in range(1, len(a)):
        aux, j = a[i], i
        while True:
            testes_j += 1
            if j <= 0:
                break
            testes_chave += 1
            if not aux < a[j - 1]:
                break
            a[j] = a[j - 1]
            deslocamentos += 1
            j -= 1
        a[j] = aux
    return a, dict(deslocamentos=deslocamentos,
                   testes_j=testes_j, testes_chave=testes_chave)

def inversoes(a):
    return sum(a[i] > a[j] for i in range(len(a))
               for j in range(i + 1, len(a)))

def fatorial_rec(n):
    if n < 0 or not isinstance(n, int):
        raise ValueError('n deve ser inteiro não negativo.')
    def rec(k):
        if k == 0:
            return 1, 0
        valor, multiplicacoes = rec(k - 1)
        return k * valor, multiplicacoes + 1
    return rec(n)

def fatorial_iter(n):
    if n < 0 or not isinstance(n, int):
        raise ValueError('n deve ser inteiro não negativo.')
    acc = 1
    for k in range(2, n + 1):
        acc *= k
    return acc

def busca_binaria(a, x):
    """Pré-condição: a ordenado; retorna índice e visitas a elementos."""
    def rec(ini, fim):
        if ini > fim:
            return -1, 0
        meio = ini + (fim - ini) // 2
        if a[meio] == x:
            return meio, 1
        if x < a[meio]:
            pos, visitas = rec(ini, meio - 1)
        else:
            pos, visitas = rec(meio + 1, fim)
        return pos, visitas + 1
    return rec(0, len(a) - 1)

def potencia(a, n):
    """Implementação da aula: quadrado inclusive em n=1."""
    if not isinstance(n, int) or n < 0:
        raise ValueError('Expoente inteiro não negativo exigido.')
    if n == 0:
        return 1, 0
    q, mult = potencia(a, n // 2)
    q *= q
    mult += 1
    if n % 2:
        q *= a
        mult += 1
    return q, mult

def polinomio_rec(a, x):
    if not a:
        raise ValueError('Informe ao menos um coeficiente.')
    def rec(n):
        if n == 0:
            return a[0]
        return a[n] * x ** n + rec(n - 1)
    return rec(len(a) - 1)

def horner(a, x):
    if not a:
        raise ValueError('Informe ao menos um coeficiente.')
    p = a[-1]
    for i in range(len(a) - 2, -1, -1):
        p = p * x + a[i]
    return p

def selos(n):
    if not isinstance(n, int) or n < 8:
        raise ValueError('Domínio: inteiros n >= 8.')
    bases = {8: (1, 1), 9: (3, 0), 10: (0, 2)}
    if n in bases:
        return bases[n]
    a, b = selos(n - 3)
    return a + 1, b

def fatores(n):
    if not isinstance(n, int) or n < 2:
        raise ValueError('Domínio: inteiros n >= 2.')
    d = 2
    while d * d <= n:
        if n % d == 0:
            return fatores(d) + fatores(n // d)
        d += 1
    return [n]

def hanoi(n, origem='O', destino='D', auxiliar='A'):
    """Gerador: não mantém a lista inteira de movimentos na memória."""
    if not isinstance(n, int) or n < 0:
        raise ValueError('n deve ser inteiro não negativo.')
    if n == 0:
        return
    if n == 1:
        yield origem, destino
        return
    yield from hanoi(n - 1, origem, auxiliar, destino)
    yield origem, destino
    yield from hanoi(n - 1, auxiliar, destino, origem)

def verifica_hanoi(n, movimentos):
    pilhas = {'O': list(range(n, 0, -1)), 'D': [], 'A': []}
    contagem = 0
    for ori, dst in movimentos:
        assert ori in pilhas and dst in pilhas and ori != dst
        assert pilhas[ori], 'Origem vazia'
        disco = pilhas[ori].pop()
        assert not pilhas[dst] or pilhas[dst][-1] > disco, 'Movimento ilegal'
        pilhas[dst].append(disco)
        contagem += 1
    assert not pilhas['O'] and not pilhas['A']
    assert pilhas['D'] == list(range(n, 0, -1))
    return contagem

def minmax_divisao(a, usar_base2=True):
    if not a:
        raise ValueError('Vetor vazio.')
    def rec(ini, fim):
        if ini == fim:
            return a[ini], a[ini], 0
        if usar_base2 and fim - ini == 1:
            if a[ini] > a[fim]:
                return a[fim], a[ini], 1
            return a[ini], a[fim], 1
        meio = ini + (fim - ini) // 2
        m1, M1, c1 = rec(ini, meio)
        m2, M2, c2 = rec(meio + 1, fim)
        return min(m1, m2), max(M1, M2), c1 + c2 + 2
    return rec(0, len(a) - 1)

def verificacoes():
    for n in range(1, 40):
        asc = list(range(n))
        desc = asc[::-1]
        assert maximo(asc) == (n - 1, n - 1, n - 1)
        assert maximo(desc) == (n - 1, n - 1, 0)
        ordenado, cont = insercao(desc)
        s = n * (n - 1) // 2
        assert ordenado == asc
        assert cont == dict(deslocamentos=s, testes_j=s+n-1, testes_chave=s)
        assert minmax_divisao(desc, False) == (0, n-1, 2*n-2)
        if n >= 2 and n & (n - 1) == 0:
            assert minmax_divisao(desc)[2] == 3*n//2-2
    assert sum(minmax_else(p)[1] for p in permutations([1, 2, 3])) == 19
    for p in permutations([1, 2, 3, 4]):
        ordenado, cont = insercao(p)
        assert cont['deslocamentos'] == inversoes(p)
        assert ordenado == [1, 2, 3, 4]
    for n in range(101):
        assert fatorial_rec(n) == (factorial(n), n)
        assert fatorial_iter(n) == factorial(n)
        for a in (-2, 0, 1, 3):
            resultado, mult = potencia(a, n)
            assert resultado == a ** n
            assert mult == (n.bit_length() + bin(n).count('1') if n else 0)
    for a in ([], [5], [1, 1, 2, 7], [2, 5, 8, 12, 16, 23, 38]):
        for x in range(-1, 41):
            pos, visitas = busca_binaria(a, x)
            assert (pos == -1) == (x not in a)
            if pos != -1:
                assert a[pos] == x
    for n in range(8, 151):
        a, b = selos(n)
        assert 3*a+5*b == n and min(a, b) >= 0
    for n in range(2, 101):
        produto = 1
        for p in fatores(n):
            assert all(p % d for d in range(2, int(p ** 0.5) + 1))
            produto *= p
        assert produto == n
    for n in range(8):
        assert verifica_hanoi(n, hanoi(n)) == 2**n-1
    assert polinomio_rec([2, -3, 4], 2) == horner([2, -3, 4], 2) == 12
    assert polinomio_rec([5], 7) == horner([5], 7) == 5
    assert minmax_divisao([1.2, -3.8, 7.1])[:2] == (-3.8, 7.1)
    assert minmax_divisao(list(range(7)))[2] == 9
    print('Todas as verificações passaram: algoritmos, contagens, bases e movimentos legais.')

if __name__ == '__main__':
    verificacoes()
