import heapq,itertools,json,subprocess
from collections import deque
from pathlib import Path

repo=Path(__file__).resolve().parents[1]
data=json.loads((repo/'conteudo/estruturas-de-dados.json').read_text())
topics=[t for c in data['chapters'] for t in c['topics']]
exs=[e for t in topics for e in t['exercises']]

def dfs(adj):
    d=[-1]*len(adj);f=d.copy();parent=d.copy();clock=0
    def visit(u):
        nonlocal clock
        clock+=1;d[u]=clock
        for v in sorted(adj[u]):
            if d[v]<0:parent[v]=u;visit(v)
        clock+=1;f[u]=clock
    for u in range(len(adj)):
        if d[u]<0:visit(u)
    return d,f,parent
assert dfs([[1,2],[0,3],[0,3],[1,2],[]])==([1,2,4,3,9],[8,7,5,6,10],[-1,0,3,1,-1])
assert dfs([[1,2],[3],[],[]])[:2]==([1,2,6,3],[8,5,7,4])

def bfs(adj,s):
    d=[-1]*len(adj);pred=d.copy();d[s]=0;q=deque([s]);order=[]
    while q:
        u=q.popleft();order.append(u)
        for v in sorted(adj[u]):
            if d[v]<0:d[v]=d[u]+1;pred[v]=u;q.append(v)
    return order,d,pred
assert bfs([[1,2],[3],[3],[4],[]],0)[1:]==([0,1,1,2,3],[-1,0,0,1,3])

def floyd(n,edges):
    d=[[0 if i==j else float('inf') for j in range(n)] for i in range(n)]
    for u,v,w in edges:d[u][v]=min(d[u][v],w)
    for k in range(n):
        for i in range(n):
            for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    return d
assert floyd(3,[(0,1,4),(1,2,2),(0,2,10),(2,0,3)])==[[0,4,6],[5,0,2],[3,7,0]]
assert floyd(4,[(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5)])[0]==[0,3,1,4]
assert floyd(4,[(0,1,7),(0,2,2),(2,1,1),(1,3,3),(2,3,9)])[0]==[0,3,2,6]

def exhaustive_mst(n,edges):
    costs=[]
    for chosen in itertools.combinations(edges,n-1):
        adj=[[] for _ in range(n)]
        for u,v,w in chosen:adj[u].append(v);adj[v].append(u)
        if all(x>=0 for x in bfs(adj,0)[1]):costs.append(sum(w for u,v,w in chosen))
    return min(costs)
assert exhaustive_mst(4,[(0,1,5),(0,2,12),(1,2,9),(1,3,10),(2,3,4)])==18
assert exhaustive_mst(4,[(0,1,2),(0,2,6),(1,2,3),(1,3,5),(2,3,1)])==6
assert exhaustive_mst(5,[(0,1,2),(0,2,6),(1,2,3),(1,3,5),(2,3,1),(2,4,7),(3,4,4)])==10

a=[2,4,3,9,7,8];assert heapq.heappop(a)==2 and a==[3,4,8,9,7]
C=4;i=3;n=2;A=[8,None,None,6];out=[]
for action,value in [('in',9),('out',None),('in',5),('in',7),('out',None)]:
    if action=='in':A[(i+n)%C]=value;n+=1
    else:out.append(A[i]);i=(i+1)%C;n-=1
assert out==[6,8] and i==1 and n==3 and [A[(i+k)%C] for k in range(n)]==[9,5,7]

# Compile every C answer using the types explicitly described by its question.
base='''#include <stdlib.h>\n#include <stdbool.h>\n#include <stddef.h>\n#define MAX 50\ntypedef struct { int chave; } REGISTRO;\ntypedef struct no { int chave; REGISTRO reg; struct no *prox,*ant,*esq,*dir; } NO;\ntypedef NO ELEMENTO;\ntypedef struct { NO *cabeca; } LISTAY;\ntypedef struct { NO *topo; } PILHA;\ntypedef struct elem { int vertice; float peso; struct elem *prox; } ElemLista;\ntypedef struct { int origem,destino; float peso; } Aresta;\ntypedef struct { int numVertices,numArestas; ElemLista **A; } Grafo;\nELEMENTO *buscaSeq(LISTAY *l, int ch);\n'''
import tempfile
_tmp = tempfile.TemporaryDirectory(prefix='sin5013-verificacao-')
tmp = Path(_tmp.name)
compiled=0
for e in exs:
    snippet=e['answer_code']
    if not snippet:continue
    fila='typedef struct { int inicio,numElementos; REGISTRO A[MAX]; } FILA;\n' if e['id']=='ED-021' else 'typedef struct { NO *inicio,*fim; } FILA;\n'
    file=tmp/(e['id']+'.c');file.write_text(base+fila+snippet+'\n')
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsyntax-only',str(file)],check=True,capture_output=True)
    compiled+=1

# Compile and execute representative boundary cases, including all three BST removal cases.
snips={e['id']:e['answer_code'] for e in exs if e['answer_code']}
bst=snips['ED-036']
runtime=base+'#include <assert.h>\n'+bst+'''
static NO *node(int k,NO *l,NO *r){ NO *n=calloc(1,sizeof *n);assert(n);n->chave=k;n->esq=l;n->dir=r;return n; }
int main(void){
 NO *r=NULL; assert(!excluiABB(&r,1));
 r=node(10,NULL,NULL);assert(excluiABB(&r,10)&&!r);
 r=node(10,node(8,node(6,NULL,NULL),NULL),node(15,NULL,NULL));
 assert(excluiABB(&r,10)&&r->chave==8&&r->esq->chave==6);
 assert(excluiABB(&r,8)&&r->chave==6);assert(excluiABB(&r,6)&&r->chave==15);assert(excluiABB(&r,15)&&!r);
 r=node(40,node(20,NULL,node(30,node(25,NULL,NULL),NULL)),node(80,NULL,NULL));
 assert(excluiABB(&r,40)&&r->chave==30&&r->esq->dir->chave==25);
 assert(excluiABB(&r,20)); assert(excluiABB(&r,25));assert(excluiABB(&r,30));assert(excluiABB(&r,80));assert(!r);
 return 0;
}
'''
file=tmp/'boundaries.c';file.write_text(runtime);binary=tmp/'boundaries'
subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(file),'-o',str(binary)],check=True,capture_output=True)
subprocess.run([str(binary)],check=True,capture_output=True)
print(f'Rastreamentos de DFS/BFS, fila, heap, caminhos e AGM conferidos; {compiled} respostas C compiladas; exclusão ABB validada em vazio, folha, raiz e predecessor com filho.')
_tmp.cleanup()
