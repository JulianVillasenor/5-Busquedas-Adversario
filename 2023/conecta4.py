from anterior.busquedas_adversarios import JuegoSumaCeros2T
from anterior.busquedas_adversarios import minimax, alpha_beta

class conecta4(JuegoSumaCeros2T):
    def __init__(self):
        """
        Inicializa el estado inicial del juego y el jugador
        que comienza (típicamente el primero)
        
        El estado se representa como una lista, y el estado inicial (x0) 
        de preferencia se representa con una tupla
        
        El jugador puede ser 1 y -1 en este caso

        """
        self.rows = 6
        self.cols = 7
        self.estado_inicial = self.rows * self.cols * [0]
        self.estado = self.rows * self.cols * [0]
        self.jugador = 1
        

    def jugadas_legales(self):
        """ 
        Devuelve un iterable con las jugadas legales del jugador actual
        
        """
        posiciones = []
        for col in range(self.cols):
            for row in range(self.rows):
                if self.estado[col + row * self.cols] == 0:
                    posiciones.append((col, row))
                    break
        return posiciones

    def es_terminal(self):
        """ 
        Devuelve True si el juago está en una posición terminal
        
        """
        x = self.estado
        cols, rows = self.cols, self.rows
        # Comproba horizontalmente
        for col in range(cols - 3):
            for row in range(rows):
                if (x[col + row * cols] != 0 and
                    x[col + row * cols] == x[col + 1 + row * cols] and
                    x[col + row * cols] == x[col + 2 + row * cols] and
                    x[col + row * cols] == x[col + 3 + row * cols] 
                ):
                    return True
        # Comprueba verticalmente
        for row in range(rows - 3):
            for col in range(cols):
                if (x[col + row * cols] != 0 and
                    x[col + row * cols] == x[col + (1 + row) * cols] and
                    x[col + row * cols] == x[col + (2 + row) * cols] and
                    x[col + row * cols] == x[col + (3 + row) * cols] 
                ):
                    return True
        # Comprueba diagonales a la derecha e izquierda
        for col in range(cols - 3):
            for row in range(rows - 3):
                if (x[col + row * cols] != 0 and
                    x[col + row * cols] == x[col + 1 + (row + 1) * cols] and
                    x[col + row * cols] == x[col + 2 + (row + 2) * cols] and
                    x[col + row * cols] == x[col + 3 + (row + 3) * cols] 
                ):
                    return True
                col0 = cols - col
                if (x[col0 + row * cols] != 0 and
                    x[col0 + row * cols] == x[col0 + 1 + (row - 1) * cols] and
                    x[col0 + row * cols] == x[col0 + 2 + (row - 2) * cols] and
                    x[col0 + row * cols] == x[col0 + 3 + (row - 3) * cols]
                ):
                    return True
        if 0 not in x:
           return True
        return False                
    
    def utilidad(self):
        """ 
        Devuelve la utilidad (final) del juador 1

        """
        x = self.estado
        cols, rows = self.cols, self.rows
        # Comproba horizontalmente
        for col in range(cols - 3):
            for row in range(rows):
                if (x[col + row * cols] != 0 and
                    x[col + row * cols] == x[col + 1 + row * cols] and
                    x[col + row * cols] == x[col + 2 + row * cols] and
                    x[col + row * cols] == x[col + 3 + row * cols] 
                ):
                    return x[col + row * cols]
        # Comprueba verticalmente
        for row in range(rows - 3):
            for col in range(cols):
                if (x[col + row * cols] != 0 and
                    x[col + row * cols] == x[col + (1 + row) * cols] and
                    x[col + row * cols] == x[col + (2 + row) * cols] and
                    x[col + row * cols] == x[col + (3 + row) * cols] 
                ):
                    return x[col + row * cols]
        # Comprueba diagonales a la derecha e izquierda
        for col in range(cols - 3):
            for row in range(rows - 3):
                if (x[col + row * cols] != 0 and
                    x[col + row * cols] == x[col + 1 + (row + 1) * cols] and
                    x[col + row * cols] == x[col + 2 + (row + 2) * cols] and
                    x[col + row * cols] == x[col + 3 + (row + 3) * cols] 
                ):
                    return x[col + row * cols]
                col0 = cols - col
                if (x[col0 + row * cols] != 0 and
                    x[col0 + row * cols] == x[col0 + 1 + (row - 1) * cols] and
                    x[col0 + row * cols] == x[col0 + 2 + (row - 2) * cols] and
                    x[col0 + row * cols] == x[col0 + 3 + (row - 3) * cols]
                ):
                    return x[col0 + row * cols]
        if 0 not in x:
           return 0
        return 0                

    def hacer_jugada(self, jugada):
        """ 
        Realiza la juagada, cambia self.estado y self.jugador, devuelve None
        
        Recuerda que el estado es una lista, para poder hacer cambios
        por referencia y ahorrar un poco de tiempo en cada nodo
        
        """
        col, row = jugada
        self.estado[col + row * self.cols] = self.jugador
        self.jugador *= -1
        
    def __str__(self):
        """ 
        Para imprimir el gato de forma bonita
        
        """
        x = self.estado
        cadena = "\n"
        for row in range(self.rows):
            linea = "|".join([
                " @@ " if x[pos] == 1 else
                " XX " if x[pos] == -1 else
                f"{pos:^4}"
                for pos in range(row * self.cols, (1 + row) * self.cols)
            ])
            cadena = '\n' + linea + cadena
        return cadena

def h_dummy(juego):
    return juego.utilidad()

def juega_c4(jugador=1, dmax=5):

    if jugador not in [-1, 1]:
        raise ValueError("El jugador solo puede ser 1 o -1")
    juego = conecta4()

    print("El juego del conecta 4".center(60))
    print(f"las ' @@' siempre empiezan, y tu juegas con {jugador}".center(60))

    if jugador == 1:
        jugada = alpha_beta(juego, dmax=dmax, heuristica=h_dummy)
        juego.hacer_jugada(jugada)

    while True:
        print(juego)
        print("Escoge tu jugada (uno de los números que quedan en el gato)")
        try:
            jn = int(input(f"Jugador {jugador}: "))
            jugada = (jn % juego.cols, jn // juego.cols)
            print(jugada)
        except:
            print("¡No seas macana y pon un número!")
            continue
        if jugada not in juego.jugadas_legales():
            print("¡No seas macana, pon un número válido!")
            continue

        juego.hacer_jugada(jugada)

        if juego.es_terminal():
            break
        else:
            jugada = alpha_beta(juego, dmax=dmax, heuristica=h_dummy)
            juego.hacer_jugada(jugada)
            if juego.es_terminal():
                break
    print(juego)
    ganador = juego.utilidad()
    if ganador == 0:
        print("UN ASQUEROSO EMPATE".center(60))
    elif (ganador > 0 and jugador == 1) or (ganador < 0 and jugador == -1):
        print("¡Gané! ¡Juar, juar, juar!, ¿Quieres jugar otra vez?".center(60))
    else:
        print("Ganaste, bye.")
    print("\n\nFin del juego")

if __name__ == '__main__':
    juega_c4(dmax=10)