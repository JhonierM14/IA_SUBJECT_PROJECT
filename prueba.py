def test(cola):
    menor = float('inf')
    for i in range(len(cola)):
        if cola[i] < menor:
            menor = cola[i]
            indice = i
    return cola[indice]

cola=[1,2,3,4,5,0]
print(test(cola))