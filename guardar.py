import tablero as tb

AGUA = "··"
BARCO = "##"
BARCO_TOCADO = "**"
BARCO_HUNDIDO = "!!"
AGUA_DISPARO = "++"

def deshacer_lista_celdas(lista_celdas:list)->str:
    texto = ""
    for i in range(0,len(lista_celdas)):
        fila, columna = lista_celdas[i]
        texto += str(fila) + "," + str(columna)
        if i < len(lista_celdas) - 1:
            texto += ";"
    return texto

def guardar_partida_minima(tableros:dict, nombre_fichero="partida_guardada.txt"):
    with open(nombre_fichero, "w", encoding="utf-8") as f:
        for jugador in tableros:
            f.write("JUGADOR\n")
            f.write(jugador + "\n")

            f.write("BARCOS\n")
            for barco in tableros[jugador]["barcos"]:
                texto_celdas = deshacer_lista_celdas(barco["celdas"])
                texto_tocadas = deshacer_lista_celdas(barco["tocadas"])
                if barco["hundido"]:
                    texto_hundido = "1" 
                else: 
                    texto_hundido = "0"
                f.write("BARCO|" + texto_celdas + "|" + texto_tocadas + "|" + texto_hundido + "\n")

            f.write("CELDAS_DISPARO\n")
            f.write(deshacer_lista_celdas(tableros[jugador]["celdas_disparo"]) + "\n")

            f.write("----\n")

def rehacer_lista_celdas(texto:str):
    celdas = []
    texto = texto.strip()
    if texto == "":
        celdas = []
    pares = texto.split(";")
    for par in pares:
        if par != "":
            fila_columna = par.split(",")
            if len(fila_columna) == 2 and fila_columna[0].isdigit() and fila_columna[1].isdigit():
                celdas.append((int(fila_columna[0]), int(fila_columna[1])))
    return celdas

def _crear_barco_diccionario(celdas:list, tocadas:list, hundido:list):
    barco = {}
    barco["celdas"] = celdas
    barco["tocadas"] = tocadas
    barco["hundido"] = hundido
    return barco

def _reconstruir_tablero_barcos(barcos:list)->list[list]:
    tablero_barcos = tb.crear_tablero_agua()

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

def reconstruir_tablero_disparos(celdas_disparo:list, tablero_barcos_oponente:list[list])->list[list]:
    tablero_disparos = tb.crear_tablero_agua()

    for (fila, columna) in celdas_disparo:
        valor_objetivo = tablero_barcos_oponente[fila][columna]
        if valor_objetivo == BARCO_TOCADO or valor_objetivo == BARCO_HUNDIDO:
            tablero_disparos[fila][columna] = valor_objetivo
        else:
            tablero_disparos[fila][columna] = AGUA_DISPARO

    return tablero_disparos

def cargar_partida_guardada(nombre_fichero:str)->tuple[dict,list]:
    with open(nombre_fichero, "r", encoding="utf-8") as fichero:
        lineas = []
        for linea in fichero:
            lineas.append(linea.strip())

    tableros = {}
    posicion = 0
    jugadores = []

    while posicion < len(lineas):
        if lineas[posicion] == "JUGADOR":
            nombre_jugador = lineas[posicion + 1]
            jugadores.append(nombre_jugador)

            tableros[nombre_jugador] = {}
            tableros[nombre_jugador]["barcos"] = []
            tableros[nombre_jugador]["celdas_disparo"] = []
            posicion = posicion + 2

            if posicion < len(lineas) and lineas[posicion] == "BARCOS":
                posicion += 1
                leyendo_barcos = True

                while leyendo_barcos and posicion < len(lineas):
                    linea = lineas[posicion]

                    if linea == "CELDAS_DISPARO":
                        leyendo_barcos = False
                    else:
                        partes = linea.split("|")
                        if partes[0] == "BARCO":
                            texto_celdas = ""
                            texto_tocadas = ""
                            texto_hundido = "0"

                            if len(partes) > 1:
                                texto_celdas = partes[1]
                            if len(partes) > 2:
                                texto_tocadas = partes[2]
                            if len(partes) > 3:
                                texto_hundido = partes[3]

                            celdas = rehacer_lista_celdas(texto_celdas)
                            tocadas = rehacer_lista_celdas(texto_tocadas)

                            hundido = False
                            if texto_hundido == "1":
                                hundido = True

                            barco = _crear_barco_diccionario(celdas, tocadas, hundido)
                            tableros[nombre_jugador]["barcos"].append(barco)

                        posicion = posicion + 1

            if posicion < len(lineas) and lineas[posicion] == "CELDAS_DISPARO":
                texto_disparos = ""
                if posicion + 1 < len(lineas):
                    texto_disparos = lineas[posicion + 1]
                tableros[nombre_jugador]["celdas_disparo"] = rehacer_lista_celdas(texto_disparos)
                posicion += 2

            if posicion < len(lineas) and lineas[posicion] == "----":
                posicion += 1
        else:
            posicion += 1

    for jugador in tableros:
        tableros[jugador]["tab_barcos"] = _reconstruir_tablero_barcos(tableros[jugador]["barcos"])

    if len(jugadores) == 2:
        jugador1 = jugadores[0]
        jugador2 = jugadores[1]

        tableros[jugador1]["tab_disparos"] = reconstruir_tablero_disparos(tableros[jugador1]["celdas_disparo"],tableros[jugador2]["tab_barcos"])
        tableros[jugador2]["tab_disparos"] = reconstruir_tablero_disparos(tableros[jugador2]["celdas_disparo"],tableros[jugador1]["tab_barcos"])

    return tableros, jugadores
