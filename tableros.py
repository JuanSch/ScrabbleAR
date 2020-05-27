import PySimpleGUI as sg

class Tablero:
    def __init__(self, x, y, margen, boton):
        self.columnas = x
        self.filas = y
        self.margen = margen
        self.boton = boton
        self.imagen = None
        self.max_xy = (ancho_tablero - margen, alto_tablero - margen)
        self.min_xy = (-margen, -margen)

    def dimensiones(self):
        b = columnas * (margen + boton) + margen
        h = filas * (margen + boton) + margen
        return (b, h)

def calcular_click(coord, boton, margen):
    linea = divmod(coord, (boton+margen))[0]
    pos = linea*(boton+margen)
    ok = coord < pos+boton
    return (ok, pos)

#configuración de medidas
margen = 10
boton = 50
columnas = 10
filas = 10
ancho_tablero = columnas*(margen+boton)+margen
alto_tablero = filas*(margen+boton)+margen
alto_fichas = boton+2*margen
margen_fichas = (ancho_tablero-(boton+margen)*7-margen)/2
max_x_fichas = (boton+margen)*7-margen+margen

tablero = Tablero(columnas, filas, margen, boton)

#diseño del tablero
layout = [[sg.Graph(key='-TABLERO-', canvas_size=(tablero.dimensiones()),
                    graph_bottom_left=(tablero.min_xy),
                    graph_top_right=(tablero.max_xy),
                    background_color='white', enable_events=True)],
          [sg.Graph(key='-FICHAS-', canvas_size=(ancho_tablero,alto_fichas),
                    graph_bottom_left=(-margen_fichas,-margen),
                    graph_top_right=(boton+margen,max_x_fichas),
                    background_color='white', enable_events=True)]]

#inicialización de la ventana
window = sg.Window('Tablero').Layout(layout).Finalize()

tablero = window.FindElement('-TABLERO-')
fichas = window.FindElement('-FICHAS-')

casillas = {}

for x in range(0, ancho_tablero-margen, margen+boton):
    for y in range(0, alto_tablero-margen, margen+boton):
        casilla = (x, y)
        casillas[casilla] = [tablero.DrawRectangle((x, y), (x+boton, y+boton),
                              line_color='#CFCFCF', fill_color='#CFCFCF'),
                             False]

while True:
    event, values = window.Read()
    if event is None:
        break
    elif event == '-TABLERO-':
        x = values[event][0]
        y = values[event][1]
        if None not in (x, y):
            x_ref = calcular_click(x, boton, margen)
            y_ref = calcular_click(y, boton, margen)
            if x_ref[0] and y_ref[0]:
                casilla = (x_ref[1], y_ref[1])
                if casillas[casilla][1] == False:
                    tablero.TKCanvas.itemconfig(casillas[casilla][0],
                                                fill='Blue')
                    casillas[casilla][1] = True
                else:
                    tablero.TKCanvas.itemconfig(casillas[casilla][0],
                                                fill='#CFCFCF')
                    casillas[casilla][1] = False


#cerrar ventana
window.Close()