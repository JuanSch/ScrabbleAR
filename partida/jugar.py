import PySimpleGUI as sg
from partida import control_ui
from layouts import partida as prt


def jugar(continuar=False):

    datos = control_ui.inicializar(continuar)
    if datos is str:
        string = ''
        if "pickle" in datos:
            string = '\nintenta cargar una nueva partida'
        sg.Popup(datos+string)

    # interfaz
    try:
        columna1 = prt.columna1_gui(datos)
    except TypeError:
        sg.Popup('Lo sentimos, hubo un error al tratar\n'
                 'de cargar el tablero de juego')
    else:
        columna2 = prt.columna2_gui(datos)
        layout = [[sg.Column(columna1), sg.Column(columna2)]]

        # inicializacion
        window = sg.Window('Ventana de juego').Layout(layout)

        # bucle
        fin, datos = control_ui.partida(window, datos)

        # control de fin de partida
        if fin:
            control_ui.fin_partida(continuar, datos)


if __name__ == '__main__':
    jugar()
