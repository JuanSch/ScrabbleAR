import PySimpleGUI as sg
import json

def confign_nuevo_juego(configuracion):
    s = []
    for i in range(1,61):
        s.append(str(i))
    layout = [

        [sg.T("Configuraciones", size=(17,1), justification = "center", font=("Georgia", 17))],
        [sg.T("Dificultad: "),sg.DropDown(('Facil','Medio','Dificil'),default_value=(configuracion['dificultad']),size=(10,1))],
        [sg.T("Tiempo de juego (en minutos): ", size=(22, 1)),sg.InputCombo((s),size=(5,1),default_value=(configuracion['tiempo']))],
        [sg.B("Jugar", size=(17, 1), key="-jugar-")]
    ]
    window = sg.Window("ScrabbleAR - Configuracion", layout)
    while True:
        event, value = window.read()
        print(event,value)
        if event == "-jugar-":
            configuracion['dificultad'] = value[0]
            configuracion['tiempo'] = value[1]
            print('estamos jugando')
            break
        else:
            break
    window.close()
    return(configuracion)

def pantalla_inicial():
    layout = [
        [sg.T("Scrabble AR", size=(17, 1), justification="center", font=("Georgia", 17))],
        [sg.T(' '),sg.B('Nueva partida', size=(25, 2), key="-nueva-")],
        [sg.T(' '),sg.B('Continuar partida', size=(25, 2), key="-continuar-")],
        [sg.T(' '),sg.B('Configuración', size=(25, 2), key="-configuracion-")],
        [sg.T(' '),sg.B('Mejores puntajes', size=(25, 2), key="-puntajes-")],
        [sg.T(' '),sg.B('Salir', size=(25, 2), key="-salir-")],
        [sg.T(' '),sg.T("  ", size=(17, 1), justification="center",)]
        ]
    window = sg.Window("ScrabbleAR - Menu", layout)
    
    while True:
        event, value = window.read()
        if event in ("-salir-", None):
            break
        elif event in "-nueva-":
            with open('configuraciones.json','r') as f:
                configs =json.load(f)
                configs = confign_nuevo_juego(configs)
            with open('configuraciones.json','w') as f:
                json.dump(configs, f, indent= 4)
        elif event in "-continuar-":
            None
        elif event in "-configuracion-":
            None
        elif event in "-puntajes-":
            None
        
    window.close()



if __name__ == "__main__":
    configuracion= {'dificultad': 'Facil', 'tiempo': 30}
    #config(configuracion)
    pantalla_inicial()
    