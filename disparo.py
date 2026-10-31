import random 
import tablero as tb
import barcos as bc
import guardar as g
AGUA = "··"
BARCO = "##"
BARCO_TOCADO = "**"
BARCO_HUNDIDO ="!!"
AGUA_DISPARO ="++"
dimension = 10
def convertir_barcos_a_diccionarios(barcos:list)-> dict:
    barcos_convertidos = []
    for celdas in barcos:
        barco = {}
        barco["celdas"] = celdas
        barco["tocadas"] = []
        barco["hundido"] = False
        barcos_convertidos.append(barco)
    return barcos_convertidos

def crear_dic_tableros_barcos(tablero_barcos1:list[list],tablero_barcos2:list[list],jugador1:str,jugador2:str,barcos1:list,barcos2:list)->dict: 
    tableros = {}

    barcos1 = convertir_barcos_a_diccionarios(barcos1)
    barcos2 = convertir_barcos_a_diccionarios(barcos2)

    tablero_barcos1 = editar_tablero_barcos_con_estado(tablero_barcos1, barcos1)
    tablero_barcos2 = editar_tablero_barcos_con_estado(tablero_barcos2, barcos2)

    tableros[jugador1] = {}
    tableros[jugador1]["tab_barcos"] = tablero_barcos1
    tableros[jugador1]["tab_disparos"] = tb.crear_tablero_agua()
    tableros[jugador1]["barcos"] = barcos1
    tableros[jugador1]["celdas_disparo"] = []

    tableros[jugador2] = {}
    tableros[jugador2]["tab_barcos"] = tablero_barcos2
    tableros[jugador2]["tab_disparos"] = tb.crear_tablero_agua()
    tableros[jugador2]["barcos"] = barcos2
    tableros[jugador2]["celdas_disparo"] = []

    return tableros

def disparo_manual(tableros:dict)-> tuple[tuple,bool]:
    salir = False
    celda_disparo = (-1, -1)

    fila_input = input("Introduce la fila (0-9) que quieres disparar o 'salir': ").strip()

    if fila_input.lower() == "salir":
        nombre_fichero = "partida_guardada.txt"
        g.guardar_partida_minima(tableros, nombre_fichero)
        salir = True
    else:
        columna_input = input("Introduce la columna (0-9) que quieres disparar: ").strip()

        if fila_input.isdigit() and columna_input.isdigit():
            fila = int(fila_input)
            columna = int(columna_input)
            celda_disparo = (fila, columna)
        else:
            print("Fila y columna deben ser números.")

    return celda_disparo, salir

def disparo_auto()->tuple:
    fila_disparo = random.randint(0, dimension - 1)
    columna_disparo = random.randint(0, dimension - 1)
    celda_disparo = (fila_disparo, columna_disparo)
    return celda_disparo

def disparo(jugador:str, oponente:str, tableros:dict)->tuple[dict,bool,bool]:
    tablero_disparo = tableros[jugador]["tab_disparos"]
    tablero_barcos_oponente = tableros[oponente]["tab_barcos"]
    tablero_barcos_jugador= tableros[jugador]["tab_barcos"]
    barcos_oponente = tableros[oponente]["barcos"]

    repetir = True
    guardar = False
    ganar = False
    salir = False

    while repetir and not guardar:
        if jugador != "maquina":
            print(f"Este es tu tablero de disparos: {jugador}")
            bc.imprimir_tablero(tablero_disparo)
            print(f"Este es tu tablero de barcos: {jugador}")
            bc.imprimir_tablero(tablero_barcos_jugador)

            celda_disparo, salir = disparo_manual(tableros)
            if salir:
                guardar = True
            if not guardar:
                fila_disparo = celda_disparo[0]
                columna_disparo = celda_disparo[1]
                if fila_disparo < 0 or fila_disparo >= dimension or columna_disparo < 0 or columna_disparo >= dimension:
                    print("Coordenadas fuera del tablero.")
                    repetir = True
                else:
                    if tablero_disparo[fila_disparo][columna_disparo] == AGUA:
                        if tablero_barcos_oponente[fila_disparo][columna_disparo] == BARCO:
                            resultado = comprobar_tocado_hundido(tablero_barcos_oponente, barcos_oponente, fila_disparo, columna_disparo)
                            if resultado == "hundido":
                                marcar_barco_hundido_en_tablero_disparo(tablero_disparo, barcos_oponente)
                                print("¡Hundido!")
                            else:
                                tablero_disparo[fila_disparo][columna_disparo] = BARCO_TOCADO
                                print("¡Tocado!")
                            ganar = comprobar_ganar(barcos_oponente)
                            if ganar:
                                print(f"\n¡Ha ganado {jugador}! Todos los barcos de {oponente} están hundidos.")
                        else:
                            tablero_disparo[fila_disparo][columna_disparo] = AGUA_DISPARO
                            print("Agua")

                        tableros[jugador]["celdas_disparo"].append((fila_disparo, columna_disparo))
                        repetir = False
                        print()
                        bc.imprimir_tablero(tablero_disparo)
                    else:
                        print("Ya has disparado a esa posición")
                        repetir = True
        else:
            celda_disparo = disparo_auto()
            if salir:
                guardar = True
            if not guardar:
                fila_disparo = celda_disparo[0]
                columna_disparo = celda_disparo[1]
                if fila_disparo < 0 or fila_disparo >= dimension or columna_disparo < 0 or columna_disparo >= dimension:
                    repetir = True
                else:
                    if tablero_disparo[fila_disparo][columna_disparo] == AGUA:
                        if tablero_barcos_oponente[fila_disparo][columna_disparo] == BARCO:
                            resultado = comprobar_tocado_hundido(tablero_barcos_oponente, barcos_oponente, fila_disparo, columna_disparo)
                            if resultado == "hundido":
                                marcar_barco_hundido_en_tablero_disparo(tablero_disparo, barcos_oponente)
                            else:
                                tablero_disparo[fila_disparo][columna_disparo] = BARCO_TOCADO
                            ganar = comprobar_ganar(barcos_oponente)
                            if ganar:
                                print(f"\n¡Ha ganado {jugador}! Todos los barcos de {oponente} están hundidos.")
                        else:
                            tablero_disparo[fila_disparo][columna_disparo] = AGUA_DISPARO

                        tableros[jugador]["celdas_disparo"].append((fila_disparo, columna_disparo))
                        repetir = False
                    else:
                        repetir = True
    return tableros, guardar, ganar

def comprobar_ganar(barcos_oponente:list)->bool:
    ganar = True
    i = 0
    while i < len(barcos_oponente) and ganar:
        if barcos_oponente[i]["hundido"] == False:
            ganar = False
        i += 1
    return ganar

def comprobar_tocado_hundido(tablero_barcos_oponente:list[list], barcos_oponente:list[list], fila_disparo:int, columna_disparo:int)->str:
    celda_disparo = (fila_disparo, columna_disparo)
    resultado = "tocado"

    indice_barco = -1
    i = 0
    while i < len(barcos_oponente) and indice_barco == -1:
        if celda_disparo in barcos_oponente[i]["celdas"]:
            indice_barco = i
        i += 1
    tablero_barcos_oponente[fila_disparo][columna_disparo] = BARCO_TOCADO

    if indice_barco != -1:
        barco = barcos_oponente[indice_barco]

        if celda_disparo not in barco["tocadas"]:
            barco["tocadas"].append(celda_disparo)

        hundido = True
        j = 0
        while j < len(barco["celdas"]) and hundido:
            if barco["celdas"][j] not in barco["tocadas"]:
                hundido = False
            j += 1

        if hundido:
            barco["hundido"] = True
            resultado = "hundido"
    editar_tablero_barcos_con_estado(tablero_barcos_oponente, barcos_oponente)

    return resultado

def editar_tablero_barcos_con_estado(tablero_barcos:list[list], barcos:dict)->list[list]:
    for fila in range(dimension):
        for columna in range(dimension):
            tablero_barcos[fila][columna] = AGUA
    for barco in barcos:
        for (fila, columna) in barco["celdas"]:
            tablero_barcos[fila][columna] = BARCO
    for barco in barcos:
        if barco["hundido"]:
            for (fila, columna) in barco["celdas"]:
                tablero_barcos[fila][columna] = BARCO_HUNDIDO
        else:
            for (fila, columna) in barco["tocadas"]:
                tablero_barcos[fila][columna] = BARCO_TOCADO

    return tablero_barcos

def marcar_barco_hundido_en_tablero_disparo(tablero_disparo:list[list], barcos_oponente:list[list]):
    for barco in barcos_oponente:
        if barco["hundido"]:
            for (fila, columna) in barco["celdas"]:
                tablero_disparo[fila][columna] = BARCO_HUNDIDO
