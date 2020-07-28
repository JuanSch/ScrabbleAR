import PySimpleGUI as sg
from os import remove
import logica as lg
import gui


def jugar(continuar = False):

    datos = gui.inicializar(continuar)

    # interfaz
    try:
        columna1 = gui.columna1_gui(datos)
    except TypeError:
        sg.Popup(datos)
    else:
        columna2 = [[sg.Button('COMENZAR', key='-INI/PAUSA-', size=(12, 2))],
                    [sg.T('')],
                    [sg.T('TIEMPO', font=('Arial', '11'))],
                    [sg.T(datos['reloj'], key='-RELOJ-', font=('Arial', '18'))],
                    [sg.T('')],
                    [sg.T('JUEGA:', font=('Arial', '11'))],
                    [sg.T('-', size=(10, 1), key='-TURNO-', font=('Arial', '14'))],
                    [sg.T('')],
                    [sg.T('PUNTAJES', font=('Arial', '11'))],
                    [sg.T('JUGADOR:', size=(15, 1), key='-PJUGADOR-',
                          font=('Arial', '14'))],
                    [sg.T('IA:', size=(15, 1), key='-PIA-', font=('Arial', '14'))],
                    [sg.T('')],
                    [sg.T('BOLSA', font=('Arial', '11'))],
                    [sg.T(f'QUEDAN {len(datos["bolsa"].fichas)} FICHAS',
                          key='-BOLSA-', font=('Arial', '14'))]
                    ]

        layout = [[sg.Column(columna1), sg.Column(columna2)]]

        # inicializacion
        window = sg.Window('Ventana de juego').Layout(layout)

        # bucle
        gui.partida(window, datos)

        #$% yo creo que la funcion actualizar puntajes va dentro de logica en vez de la IA
        if datos['fin']:
            if continuar:
                    remove("continuar_partida.pickle") #Como terminó la partida borramos la partida guardada
            if puntos_jugador > puntos_ia: #evalua quien gana
                if gui.actualizar_puntajes([nombre, puntos_jugador], dificultad): #evalua si entra en el top10 (si entra se agrega)
                    sg.Popup('¡Ganaste y entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
                    lg.top10()
                else:
                    sg.Popup('¡Ganaste! \n Tu puntiacion es: ' + str(puntos_jugador))
                #ganaste
            elif puntos_jugador == puntos_ia:
                if gui.actualizar_puntajes([nombre, puntos_jugador], dificultad):
                    sg.Popup('¡Empataste y entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
                    lg.top10()
                else:
                    sg.Popup('¡Empataste! La proxima ganarás \n Tu puntiacion es: ' + str(puntos_jugador))
            else:
                if gui.actualizar_puntajes([nombre, puntos_jugador], dificultad):
                    sg.Popup('¡Perdiste pero entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
                    lg.top10()
                else:
                    sg.Popup('!Perdiste suerte la próxima! \n Tu puntiacion es: ' + str(puntos_jugador))


if __name__ == '__main__':
    jugar()