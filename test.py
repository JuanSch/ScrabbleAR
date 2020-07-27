def comentado():
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

######
# import json

# with open('valores_puntajes.json','r') as f:
#     valores_puntajes = json.load(f)
#     top_diez= valores_puntajes['top10']
#     print(top_diez)
#     top10 = {}
#     top10['Facil'] = top_diez
#     top10['Medio'] = top_diez
#     top10['Dificil'] = top_diez
#     valores_puntajes.pop('top10')
#     valores_puntajes['top10'] = top10
#     print('\n')
#     print(valores_puntajes)

# with open('valores_puntajes.json','w') as f:
#     json.dump(valores_puntajes, f, indent=4)

import pickle

with open('continuar_partida.pickle','w') as f:
    pass