import barcos as bar
import guardar as g
import disparo as d
VERDE = "\033[1;42m"
DEFECTO = "\033[0m"
AMARILLO = "\033[1;43m"
if __name__ == "__main__":
    num_min_barcos = 2
    num_max_barcos = 5
    jugadores = True
    ganar = False
    guardar = False
    contador = 0
    nombre_fichero="partida_guardada.txt"
    formato = input("¿Quieres 'continuar una partida' o 'empezar una nueva'?")
    if formato == "empezar una nueva":
        while jugadores:
            num_jugadores = input("Introduce el número de jugadores (1 o 2):")
            num_jugadores_int = int(num_jugadores)
            if num_jugadores_int == 2: 
                cantidad = bar.cantidad_barcos(num_min_barcos,num_max_barcos)
                jugador1 = input("Nombre jugador 1:")
                tablero_barcos1,barcos1 = bar.barcos(num_min_barcos,num_max_barcos,jugador1,cantidad)
                jugador2 = input("Nombre jugador 2:")
                tablero_barcos2,barcos2 = bar.barcos(num_min_barcos,num_max_barcos,jugador2,cantidad)
                jugadores = False
                tableros = d.crear_dic_tableros_barcos(tablero_barcos1,tablero_barcos2,jugador1,jugador2,barcos1,barcos2)
            elif num_jugadores_int == 1: 
                cantidad = bar.cantidad_barcos(num_min_barcos,num_max_barcos)
                jugador1 = input("Nombre jugador 1:")
                tablero_barcos1,barcos1 = bar.barcos(num_min_barcos,num_max_barcos,jugador1,cantidad)
                jugador2= "maquina"
                tablero_barcos2,barcos2 = bar.barcos_maquina(cantidad)
                jugadores = False
                tableros = d.crear_dic_tableros_barcos(tablero_barcos1,tablero_barcos2,jugador1,jugador2,barcos1,barcos2)
            else: 
                jugadores = True
        print(f"{AMARILLO}¡¡¡INICIO DEL JUEGO!!!!{DEFECTO}")
    elif formato == "continuar una partida":
        tableros, jugadores = g.cargar_partida_guardada(nombre_fichero)
        jugador1 = jugadores[0]
        jugador2 = jugadores[1]
    else: 
        print("No has seleccionado ninguna de las dos opciones")
        jugadores = False
        ganar = True
        guardar = True
    

    while not ganar and not guardar:
        if contador == 0:
            jugador = jugador1
            oponente = jugador2
            contador = 1
        else:
            jugador = jugador2
            oponente = jugador1
            contador = 0
        print(f"{VERDE}ES EL TURNO DE {jugador} {DEFECTO}")
        tableros, guardar, ganar = d.disparo(jugador, oponente, tableros)

    
