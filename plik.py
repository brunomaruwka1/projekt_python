lista = [[1,1],[2,2],[3,3]]
lista2 = []

for i in lista:
    lista2.insert((*lista[i]))

print(lista2)