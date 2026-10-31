ancho = 10
largo = 10
agua = "··"
def crear_tablero_agua()-> list[list]:
    matriz = []
    for i in range(0,largo):
        lista = []
        for columna in range(0,ancho):
            lista.append(agua)
        matriz.append(lista)
    return matriz


