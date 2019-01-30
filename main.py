import pulp as pulp
from json import load
from itertools import product

# Lendo o arquivo json com as informações dos pacotes
jsonFile = "bd.json"
with open(jsonFile) as arq:
    bd = load(arq)

# Primeiro tipo de container
ct1 = bd["ct_20"]                           # Json com as informações do primeiro container
l1 = ct1["x"]                               # Lado do container no eixo x
c1 = ct1["y"]                               # Lado do container no eixo y

# Segundo tipo de container
ct2 = bd["ct_40"]                           # Json com as informações do primeiro container
l2 = ct2["x"]                               # Lado do container no eixo x
c2 = ct2["y"]                               # Lado do container no eixo y

# Primeiro tipo de pacote
pkg = bd["pkg1"]                            # Json com as informações do primeiro pacote
a = pkg["x"]                                # Lado do pacote no eixo x
b = pkg["y"]                                # Lado do pacote no eixo y


vetor_principal1 = [(0, 0), (l1, c1)]       # Vetor que determina o container
a_ct = l1 * c1                              # Área do container1
a_pkg = a * b                               # Área do pacote
areas = []                                  # Armazena as áreas finais criadas
areas_temp = []                             # Armazena temporariamente as áreas criadas


def verificaUtilidade(x, y, pkg_ladoa, pkg_ladob, lado_u, lado_n):
    utilidade = True
    if x > 0 and b > lado_n:
        utilidade = False
    if y > 0 and a > lado_n:
        utilidade = False
    return utilidade


def permutacao(qt_ladoa, qt_ladob):
    qt = qt_ladoa + qt_ladob
    a = qt_ladoa
    b = qt_ladob
    caracteres = []
    if qt_ladoa > 0:
        while qt_ladoa > 0:
            caracteres.append(0)
            qt_ladoa -= 1
    if qt_ladob > 0:
        while qt_ladob > 0:
            caracteres.append(1)
            qt_ladob -= 1
    # Aqui e onde tens de especificar o numero de chars que cada combinacao tenha
    genComb = product(caracteres, repeat=qt)
    permsList = []
    for subset in genComb:
        n = subset.count(0)
        m = subset.count(1)
        if subset not in permsList and n == a and m == b:
            permsList.append(subset)
    return permsList
def recorte():
    return ""


def main(a, b, vetor):

    l1 = vetor[1][0]
    c1 = vetor[1][1]
    # Variáveis da Função Objetivo
    x = pulp.LpVariable("x",  lowBound=0, cat='Integer')     # Variável para o cálculo da quantidade
    x1 = pulp.LpVariable("x1", lowBound=0, cat='Integer')    # Variável para o cálculo da quantidade do lado a no eixo x
    y1 = pulp.LpVariable("y1", lowBound=0, cat='Integer')    # Variável para o cálculo da quantidade do lado b no eixo x
    x2 = pulp.LpVariable("x2",  lowBound=0, cat='Integer')   # Variável para o cálculo da quantidade do lado a no eixo y
    y2 = pulp.LpVariable("y2",  lowBound=0, cat='Integer')   # Variável para o cálculo da quantidade do lado b no eixo y

    # Criando o problema
    resto1 = pulp.LpProblem("AxisX", pulp.LpMaximize)
    resto2 = pulp.LpProblem("AxisY", pulp.LpMaximize)
    qt = pulp.LpProblem("Quantidade", pulp.LpMaximize)

    # Função Objetivo
    resto1 += a*x1 + b*y1                       # x1 = quantidade do lado a, y1 = quantidade do lado b
    resto2 += a*x2 + b*y2                       # x2 = quantidade do lado a, y2 = quantidade do lado b
    qt += a*b*x                                 # x = quantidade de áreas de lados ab

    # Restrições
    # Quantidade multiplicada pelos lados do pacote não pode ser maior que o lado do container
    resto1 += a*x1 + b*y1 <= l1
    resto2 += a*x2 + b*y2 <= c1

    # Quantidade multiplicada pelas áreas não pode ser maior que a área do container
    qt += a*b*x <= l1*c1

    # Solucionando a função objetivo
    qt.solve()
    resto1.solve()
    resto2.solve()

    # Pegando os valores das variáveis atribuidas na função objetivo
    val_x1 = x1.value()
    val_y1 = y1.value()
    val_x2 = x2.value()
    val_y2 = y2.value()
    quantidade = x.value()

    print("Quantidade Possível para o pacote deitado no lado x do container: %i" % val_x1)
    print("Quantidade Possível para o pacote em pé no lado x do container: %i" % val_y1)
    print("Quantidade Máxima de pacotes no container: %i" % quantidade)
    print("-------------------------------------")
    print("Se o lado do container e o valor da função objetivo forem iguais, significa que foi ocupado o máximo possível")
    print("Lado x do container: %i" % l1)
    print("Valor da função objetivo: %i" % resto1.objective.value())
    print(resto1.sequentialSolve)
    print(resto2.sequentialSolve)

    # Esta parte ainda está em andamento
    # Por enquanto isso funciona como um teste onde ele pega os
    if val_x1 == 0 and val_y1 == 0:
        print("Não teve quantidades para ambos")
    else:
        origem_x = vetor[0][0]  # Pegando o ponto de origem do container em x
        origem_y = vetor[0][1]  # Pegando o ponto de origem do container em y
        soma = False
        x_x = val_x1 * a
        x_y = b
        y_x = a
        y_y = val_y1 * b
        if val_x1 != 0 and b <= c1:
            temp1 = [(origem_x, origem_y), (x_x, x_y)]
            origem_x = x_x
            areas_temp.append(temp1)
            soma = True
        if val_y1 != 0 and a <= c1:
            if soma:
                y_y += x_x
            temp2 = [(origem_x, origem_y), (y_y, y_x)]
            areas_temp.append(temp2)
        else:
            print("-------------------------------------")
            print("Erro: Não podem ser colocados os pacotes")
    print("-------------------------------------")
    utilidade1 = verificaUtilidade(val_x1, val_y1, a, b, l1, c1)
    utilidade2 = verificaUtilidade(val_x2, 2, a, b, c1, l1)
    if utilidade1:
        ordens = permutacao(int(val_x1), int(val_y1))
        print(ordens)
    if utilidade2:
        ordens = permutacao(int(val_x2), int(val_y2))
        print(ordens)
    else:
        print("Erro: Não podem ser colocados os pacotes")
    print("Áreas: " + str(areas_temp))

main(a, b, vetor_principal1)