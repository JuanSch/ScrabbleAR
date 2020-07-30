import PySimpleGUI as sg
import gui


def jugar(continuar=False):

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
        fin = gui.partida(window, datos)

        # control de fin de partida
        if fin:
            gui.fin_partida(continuar, datos)


if __name__ == '__main__':
    jugar()