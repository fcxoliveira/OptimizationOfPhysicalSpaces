from pulp import *
from json import load

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

# Variáveis da Função Objetivo
x = LpVariable("x",  lowBound=0, cat='Integer')     # Variável para o cálculo da quantidade
x1 = LpVariable("x1", lowBound=0, cat='Integer')    # Variável para o cálculo da quantidade do lado a no eixo x
y1 = LpVariable("y1", lowBound=0, cat='Integer')    # Variável para o cálculo da quantidade do lado b no eixo x
x2 = LpVariable("x2",  lowBound=0, cat='Integer')   # Variável para o cálculo da quantidade do lado a no eixo y
y2 = LpVariable("y2",  lowBound=0, cat='Integer')   # Variável para o cálculo da quantidade do lado b no eixo y

# Criando o problema
resto1 = LpProblem("AxisX", LpMaximize)
resto2 = LpProblem("AxisY", LpMaximize)
qt = LpProblem("Quantidade", LpMaximize)

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
val_x1 = value(x1)
val_y1 = value(y1)
quantidade = value(x)

print("Quantidade Possível para o pacote deitado no lado x do container: %i" % val_x1)
print("Quantidade Possível para o pacote em pé no lado x do container: %i" % val_y1)
print("Quantidade Máxima de pacotes no container: %i" % quantidade)
print("-------------------------------------")
print("Se o lado do container e o valor da função objetivo forem iguais, significa que foi ocupado o máximo possível")
print("Lado x do container: %i" % l1)
print("Valor da função objetivo: %i" % value(resto1.objective))

# Esta parte ainda está em andamento
# Por enquanto isso funciona como um teste onde ele pega os
if val_x1 == 0 and val_y1 == 0:
    print("Não teve quantidades para ambos")
else:
    origem_x = vetor_principal1[0][0]  # Pegando o ponto de origem do container em x
    origem_y = vetor_principal1[0][1]  # Pegando o ponto de origem do container em y
    x_x = val_x1 * a
    x_y = b
    y_x = a
    y_y = x_x + (val_y1 * b)
    if val_x1 != 0 and b <= c1:
        temp1 = [(origem_x, origem_y), (x_x, x_y)]
        origem_x = x_x
        areas_temp.append(temp1)
    if val_y1 != 0 and a <= c1:
        temp2 = [(origem_x, origem_y), (y_y, y_x)]
        areas_temp.append(temp2)
    else:
        print("-------------------------------------")
        print("Erro: Não podem ser colocados os pacotes")
print("-------------------------------------")
print("Áreas: " + str(areas_temp))
