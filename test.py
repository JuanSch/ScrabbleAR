import PySimpleGUI as sg
import time as t

tiempo = 300
reloj = f'{divmod(tiempo,60)[0]:02}:{divmod(tiempo,60)[1]:02}'

layout = [[sg.T(reloj, key='-RELOJ-')],
          [sg.Button('Inicio', key='-INI/PAUSA-')],
          [sg.Button('Click')]
          ]

window = sg.Window('Reloj de prueba').Layout(layout)

clicks = 0
contando = False
FIN = False
while not FIN:
    event, values = window.Read(timeout=100)
    if contando:
        transcurrido = int(t.time())-inicio
        tiempo -= transcurrido
        reloj = f'{divmod(tiempo, 60)[0]:02}:{divmod(tiempo, 60)[1]:02}'
        window.FindElement('-RELOJ-').Update(reloj)
        if tiempo < 0:
            FIN = True
            sg.Popup('Se acabó el tiempo')

    if event is None:
        break

    elif event == 'Click':
        clicks += 1
        print(clicks)

    elif event == '-INI/PAUSA-':
        if not contando:
            inicio = int(t.time())
            contando = True
            window.FindElement('-INI/PAUSA-').Update('Pausa')
        else:
            contando = False
            window.FindElement('-INI/PAUSA-').Update('Inicio')

window.Close()

