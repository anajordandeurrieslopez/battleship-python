import random
import tablero as tb
import excepciones as ex

BARCO = "##"
AGUA = "··"
dimension = 10
tamaño_max = 5
tamaño_min = 2

def cantidad_barcos(num_min_barcos: int,num_max_barcos: int)-> str| int:
    forma = input("¿Quieres introducir 'manualmente' o 'automáticamente' la cantidad de barcos?:")
    if forma == "manualmente":
        cantidad = input("¿Cuantos barcos quieres colocar?")
        if not cantidad.isdigit():
            raise ex.EntradaInvalidaError("La cantidad debe ser un número.")
        cantidad = int(cantidad)
        if cantidad < num_min_barcos or cantidad > num_max_barcos:
            raise ex.EntradaInvalidaError("Cantidad fuera de rango.")
    elif forma == "automáticamente" or forma == "automaticamente": 
        cantidad = random.randint(num_min_barcos,num_max_barcos)
    return cantidad

def barcos(num_min_barcos: int, num_max_barcos: int,jugador: str,cantidad: int)-> tuple[list[list],list]:
    barcos = []
    tablero = tb.crear_tablero_agua()
    forma = input("¿Quieres introducir 'manualmente' o 'automáticamente' la posición de los barcos?: ").strip().lower()

    if forma == "manualmente":
        barcos = colocar_barcos_manual(cantidad, tablero, barcos)
    elif forma == "automáticamente" or forma == "automaticamente":
        barcos = colocar_barcos_auto(cantidad, tablero, barcos)
    else:
        raise ex.EntradaInvalidaError("Debes escribir 'manualmente' o 'automáticamente'.")

    return tablero, barcos

def barcos_maquina(cantidad:int):
    barcos = []
    tablero = tb.crear_tablero_agua()
    barcos = colocar_barcos_auto(cantidad, tablero, barcos)
    return tablero, barcos

def colocar_barcos_auto(cantidad: int, tablero: list[list], barcos: list) ->list:
    largo_barco = elegir_longitud_barco_auto(tamaño_max,tamaño_min)
    while cantidad > 0:
        largo_barco = elegir_longitud_barco_auto(tamaño_max,tamaño_min)
        celdas = crear_barco_auto(largo_barco, tablero)
        if celdas != []:
            barcos.append(celdas)
            cantidad -= 1

    return barcos

def elegir_longitud_barco_auto(tamaño_max: int,tamaño_min: int):
    longitud = random.randint(tamaño_min, tamaño_max)
    return longitud

def elegir_longitud_barco(tamaño_max: int,tamaño_min: int):
    longitud_valida = False
    longitud = 0

    while not longitud_valida:
        entrada = input(f"Introduce la longitud del barco ({tamaño_min}-{tamaño_max}): ").strip()

        if entrada.isdigit():
            longitud = int(entrada)
            if longitud >= tamaño_min and longitud <= tamaño_max:
                longitud_valida = True
            else:
                print("La longitud está fuera del rango permitido.")
        else:
            print("Debes introducir un número.")

    return longitud

def colocar_barcos_manual(cantidad: int, tablero: list[list], barcos: list) -> list:
    while cantidad > 0:
        largo_barco = elegir_longitud_barco(tamaño_max,tamaño_min)
        celdas = crear_barco_manual(largo_barco, tablero)
        if celdas != []:
            barcos.append(celdas)
            cantidad -= 1

        imprimir_tablero(tablero)

    return barcos

def crear_barco_manual(largo_barco: int, tablero: list[list]) -> list:
    fila_str = input(f"Introduce la fila (0-9) para barco de largo {largo_barco}: ").strip()
    columna_str = input(f"Introduce la columna (0-9) para barco de largo {largo_barco}: ").strip()

    if (not fila_str.isdigit()) or (not columna_str.isdigit()):
        print("Fila y columna deben ser números.")
        return []

    fila = int(fila_str)
    columna = int(columna_str)
    inicio = (fila, columna)

    falso = True
    while falso:
        orientacion = input("Introduce la orientación ('horizontal' o 'vertical'): ").strip().lower()
        if orientacion == "horizontal":
            orientacion = 1
            falso = False
        elif orientacion == "vertical":
            orientacion = 2
            falso = False
        else:
            falso = True
            print("orientación no válida")

    celdas = celdas_barco(inicio, largo_barco, orientacion)

    if not cabe_tablero(inicio, largo_barco, orientacion):
        print("El barco no cabe en esa posición")
        return []

    try:
        solapa(inicio, largo_barco, orientacion, tablero)
        tablero = meter_en_tablero(tablero, celdas)
        return celdas
    except ex.SolapeBarcoError as error:
        print(error)
        return []

def crear_barco_auto(largo_barco: int, tablero: list[list])->list:
    fila = random.randint(0, dimension - 1)
    columna = random.randint(0, dimension - 1)
    inicio = (fila, columna)
    orientacion = random.randint(1, 2)

    celdas = celdas_barco(inicio, largo_barco, orientacion)
    cabe = cabe_tablero(inicio, largo_barco, orientacion)

    if not cabe:
        return []

    try:
        solapa(inicio, largo_barco, orientacion, tablero)
        tablero = meter_en_tablero(tablero, celdas)
        return celdas
    except ex.SolapeBarcoError:
        return []

def celdas_barco(inicio: tuple, largo_barco: int, orientacion: int) -> list:
    celdas = []
    for i in range(largo_barco):
        if orientacion == 1:
            celdas.append((inicio[0], inicio[1] + i))
        else:
            celdas.append((inicio[0] + i, inicio[1]))
    return celdas

def cabe_tablero(inicio: tuple, largo_barco:int, orientacion: int) ->bool:
    celdas = celdas_barco(inicio, largo_barco, orientacion)
    final = celdas[len(celdas) - 1]
    fila_final = final[0]
    columna_final = final[1]

    if 0 <= inicio[0] < dimension and 0 <= inicio[1] < dimension and fila_final < dimension and columna_final < dimension:
        cabe = True
    else:
        cabe = False

    return cabe

def solapa(inicio: tuple, largo_barco: int, orientacion: int, tablero: list[list]):
    for i in range(0, largo_barco):
        if orientacion == 1:
            fila = inicio[0]
            columna = inicio[1] + i
        else:
            fila = inicio[0] + i
            columna = inicio[1]
        if fila < 0 or fila >= dimension or columna < 0 or columna >= dimension:
            raise ex.CoordenadaFueraTableroError("Coordenadas fuera del tablero.")

        if tablero[fila][columna] == AGUA:
            pass
        else:
            raise ex.SolapeBarcoError("Este barco solapa con otro")

def meter_en_tablero(tablero: list[list], celdas: list) -> list[list]:
    for (fila, columna) in celdas:
        tablero[fila][columna] = BARCO
    return tablero

def imprimir_tablero(tablero:list[list]):
    for linea in tablero:
        for indice in range(0, len(linea)):
            print(linea[indice], end=" ")
        print(" ")

