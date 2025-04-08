from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from juegos_simplificado import minimax
from minimax import jugador_negamax


class UltimateGato(ModeloJuegoZT2):
    def inicializa(self):
        # Representamos el estado como una tupla:
        # (tableros_pequenos, tablero_grande, turno, siguiente_tablero)
        # - tableros_pequenos: lista de 9 tuplas (cada uno es un tablero chico 3x3)
        # - tablero_grande: tupla de 9 enteros que indica si se ganó cada tablero chico (0: no ganado, 1: X, -1: O, 2: empate)
        # - turno: 1 para X, -1 para O
        # - siguiente_tablero: índice del tablero donde debe jugarse (0-8), o -1 si el jugador puede elegir
        estado = (tuple([tuple([0]*9) for _ in range(9)]), tuple([0]*9), 1, -1) 
        return estado, 1
    

    def jugadas_legales(self, s, j):
        tableros, grandes, turno, sig = s
        jugadas = []
        if sig == -1: #si se puede jugar en cualquier tablero
            for i in range(9):
                if grandes[i] == 0:
                    for jdx, val in enumerate(tableros[i]): #enumera un tablero a la vez y revisa si esta libre para colocar una jugada (0,-1)
                        if val == 0:
                            jugadas.append((i, jdx)) #si no hay jugada puesta se añade a jugadas legales
        else:
            if grandes[sig] == 0: #si tenemos que jugar en el tablero i
                for jdx, val in enumerate(tableros[sig]): #se hacen appends tambien de las posiciones donde el valor es 0
                    if val == 0:
                        jugadas.append((sig, jdx))
        return jugadas

    def transicion(self, s, a, j):
        tableros, grandes, turno, sig = s
        i, jdx = a #(i= tablero chico, jdx=posicion)
        nuevo_tablero = list(tableros[i])
        nuevo_tablero[jdx] = turno #{1,-1}
        nuevos_tableros = list(tableros)
        nuevos_tableros[i] = tuple(nuevo_tablero) #se actualiza la posicion de la tabla mini

        nuevo_grandes = list(grandes) #copia de grandes
        if self.terminal_tablero(nuevo_tablero): #si el tablero esta terminado
            ganador = self.ganador_tablero(nuevo_tablero) #jugador ganador
            if ganador == 0 and 0 not in nuevo_tablero:
                nuevo_grandes[i] = 2  # empate
            else:
                nuevo_grandes[i] = ganador #{1,-1}

        # El siguiente tablero está determinado por jdx
        siguiente = jdx if nuevo_grandes[jdx] == 0 else -1 #Se puede seguir jugando en el mini?
        return (tuple(nuevos_tableros), tuple(nuevo_grandes), -turno, siguiente) #regresa el nuevo estado con el jugador siguiente y el siguiente mini

    def terminal(self, s):
        _, grandes, _, _ = s
        return self.terminal_tablero(grandes)

    def ganancia(self, s):
        _, grandes, _, _ = s
        return self.ganador_tablero(grandes)

    def terminal_tablero(self, t):
        # t puede ser un tablero chico o el grande
        if t[0] == t[4] == t[8] != 0: return True #revisar diagonal abajo ->
        if t[2] == t[4] == t[6] != 0: return True #revisar diagonal <- abajo
        for i in range(3): 
            if t[3*i] == t[3*i+1] == t[3*i+2] != 0: return True #filas
            if t[i] == t[i+3] == t[i+6] != 0: return True #columnas
        return all(x != 0 for x in t) #Gano el gato

    def ganador_tablero(self, t):
        if t[0] == t[4] == t[8] != 0: return t[0]
        if t[2] == t[4] == t[6] != 0: return t[2]
        for i in range(3):
            if t[3*i] == t[3*i+1] == t[3*i+2] != 0: return t[3*i]
            if t[i] == t[i+3] == t[i+6] != 0: return t[i]
        return 0

# Puedes desarrollar pprint_ultimate, jugador_manual_ultimate y una funcion juega_ultimate
# similar a juega_gato para probar este juego interactivamente.
def pprint_ultimate(s):
    """
    Imprime el estado del juego de Ultimate Gato de manera legible.
    """
    tableros, grandes, turno, sig = s
    def simbolo(x, i): 
        return ' X ' if x == 1 else ' O ' if x == -1 else str(i).center(3)
    
    filas = []
    for bloque_fila in range(3):
        bloque = ["", "", ""]
        for bloque_col in range(3):
            tablero_idx = bloque_fila * 3 + bloque_col
            tablero = tableros[tablero_idx]
            linea = [simbolo(tablero[i], i) for i in range(9)]
            bloque[0] += '|'.join(linea[0:3]) + ' || '
            bloque[1] += '|'.join(linea[3:6]) + ' || '
            bloque[2] += '|'.join(linea[6:9]) + ' || '
        filas.extend(bloque)
        filas.append('-'*35)
    for linea in filas:
        print(linea)


        
def jugador_manual_ultimate(juego, s, j):
    """
    Jugador manual para Ultimate Gato
    """
    pprint_ultimate(s)
    print("Jugador:", 'X' if j == 1 else 'O')
    jugadas = juego.jugadas_legales(s, j)
    print("Jugadas legales:", jugadas)
    
    while True:
        try:
            entrada = input("Elige tu jugada como 'tablero,posicion': ")
            i, jdx = map(int, entrada.strip().split(','))
            if (i, jdx) in jugadas:
                return (i, jdx)
            else:
                print("Jugada no válida. Intenta de nuevo.")
        except Exception:
            print("Entrada inválida. Usa el formato: tablero,posicion (ej. 4,7)")

def jugador_minimax_ultimate(juego, s, j):
    """
    Jugador minimax para Ultimate Gato (puedes usar negamax también)
    """
    return minimax(juego, s, j)
    # o return jugador_negamax(juego, s, j)
def evalua_dummy(estado):
    return 0

def juega_ultimate(jugador='X'):
    """
    Ejecuta una partida de Ultimate Gato entre humano y AI
    """
    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    
    juego = UltimateGato()
    print("ULTIMATE GATO")
    print(f"Las 'X' siempre empiezan y tú juegas con '{jugador}'")
    
    if jugador == 'X':
        g, s = juega_dos_jugadores(
            juego,
            jugador_manual_ultimate,
            lambda j, e, ju: jugador_negamax(j, e , ju, d=3, evalua= evalua_dummy))
    else:
        g, s = juega_dos_jugadores(juego,
                                    lambda j, e, ju: jugador_negamax(j, e, ju, d=3, evalua=evalua_dummy),
                                      jugador_manual_ultimate)
    
    print("\nSE ACABÓ EL JUEGO\n")
    pprint_ultimate(s)
    
    if g == 0:
        print("\nEmpate, qué triste.")
    elif (g == 1 and jugador == 'X') or (g == -1 and jugador == 'O'):
        print("\nGanaste, debe ser pura suerte.")
    else:
        print("\nPerdiste, la máquina manda.")

if __name__ == '__main__':
    juega_ultimate('X')  # Empieza jugando X
