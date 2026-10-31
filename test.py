import tablero as tb
import disparo as d
import barcos as b 

BARCO_TOCADO = "**"
BARCO_HUNDIDO = "!!"




print("Test comprobar_ganar")

try:
    barcos = []

    barco1 = {
        "celdas": [(0, 0), (0, 1)],
        "tocadas": [(0, 0), (0, 1)],
        "hundido": True
    }

    barco2 = {
        "celdas": [(2, 2)],
        "tocadas": [(2, 2)],
        "hundido": True
    }

    barcos.append(barco1)
    barcos.append(barco2)

    resultado = d.comprobar_ganar(barcos)

    if resultado == True:
        print("Test comprobar_ganar CORRECTO")
    else:
        print("Test comprobar_ganar FALLIDO")

except Exception as error:
    print("✘ Test comprobar_ganar ERROR")
    print(error)






print("Test cabe_tablero")

try:
    resultado1 = b.cabe_tablero((0, 0), 4, 1)
    if resultado1 == True:
        print("Barco dentro del tablero CORRECTO")
    else:
        print("Barco dentro del tablero NO CORRECTO")

    resultado2 = b.cabe_tablero((0, 8), 4, 1)
    if resultado2 == False:
        print("Barco dentro del tablero CORRECTO")
    else:
        print("Barco dentro del tablero NO CORRECTO")

    resultado3 = b.cabe_tablero((6, 3), 3, 2)
    if resultado3 == True:
        print("Barco dentro del tablero CORRECTO")
    else:
        print("Barco dentro del tablero NO CORRECTO")

    resultado4 = b.cabe_tablero((8, 3), 4, 2)
    if resultado4 == False:
        print("Barco dentro del tablero CORRECTO")
    else:
        print("Barco dentro del tablero NO CORRECTO")

except Exception as error:
    print("ERROR")
    print(error)
