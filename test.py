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
import json

with open('configuraciones.json','r', encoding='UTF-8') as f:
    configs = json.load(f)
    personalizada = configs['Personalizada']
    bolsa = []
    for key in personalizada:
        value = personalizada[key]
        bolsa.append([key,value])
    print(bolsa)
    with open('valores_puntajes.json', 'r', encoding='UTF-8') as v:
        valores = json.load(v)
        dic = {}
        dic['bolsa'] = bolsa
        dic['dificultad_IA'] = 'Facil'
        dic['dificultad_Tablero'] = 'Facil'
        valores['Personalizada'] = dic
    print(valores)
    with open('valores_puntajes.json', 'w', encoding='UTF-8') as v:
        json.dump(valores, v, indent= 4)
print('fin')