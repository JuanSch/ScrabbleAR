import PySimpleGUI as sg
import json
from tableros import jugar

class TimeOutException(Exception):
    def __init__(self):
        sg.popup('Juego terminado')
        pass
    def __str__(self):
        error = 'Tiempo de juego terminado'
        return(error)

def config_nuevo_juego(configuracion):
    def timeout():
        print('Juego terminado')
    
    def temporizador(time,timeout):
        from threading import Timer as timer
        t = timer(time*6, timeout)
        t.start()
    
    s = []
    for i in range(1,61):
        s.append(str(i))

    layout = [
        [sg.T("Nuevo juego", size=(17,1), justification = "center",
              font=("Georgia", 17))],
        [sg.T("Dificultad: "),
         sg.DropDown(('Facil','Medio','Dificil','Personalizada'),
                     default_value=(configuracion['dificultad']),size=(10,1))],
        [sg.T("Tiempo de juego (en minutos): ", size=(22, 1)),
         sg.InputCombo((s),size=(5,1),default_value=(configuracion['tiempo']))],
        [sg.B("Jugar", size=(12, 1), key="-jugar-"),sg.B("Personalizar",size=(12,1), key="-personalizar-")]
        ]

    window = sg.Window("ScrabbleAR - Nuevo juego", layout)

    while True:
        event, value = window.read()
        if event == "-jugar-":
            configuracion['dificultad'] = value[0]
            configuracion['tiempo'] = value[1]
            break
        elif event == "-personalizar-":
            configurar(configuracion)
        else:
            break

    temporizador(float(configuracion['tiempo']), timeout)

    window.close()
    if event == "-jugar-":
        return(configuracion,True)
    else:
        return(configuracion,False)

def configurar(dic):
    letras = dic['personalizada']
    lista_letras= []
    lista_valores = []
    for key in letras:
        lista_letras.append(key)
    for y in range(13):
        lista_valores.append(y)
    df_vl = letras['a']
    layout=[
        [sg.T("Perfil personalizado", size=(17,1), justification = "center",
              font=("Georgia", 17))],
        [sg.T("Letra",font=("Georgia", 12)), sg.Combo(lista_letras, size=(8,1), default_value= 'a'),
         sg.T("Cantidad:", font=("Georgia", 12),),sg.Combo(lista_valores,size=(8,1), default_value=df_vl)],
        [sg.B("Guardar", size=(12, 1), key="-guardar-")]
        ]

    window = sg.Window("ScrabbleAR - Configurar", layout)

    while True:
        event, value = window.read()
        if event == None:
            break
        elif event == '-guardar-':
            df_vl = letras[value[0]] = value[1]
            dic['personalizada'] = letras
            with open('configuraciones.json','w') as f:
                json.dump(dic, f, indent= 4)
    window.close()
    
def pantalla_inicial():

    layout = [
        [sg.T("Scrabble AR", size=(17, 1), justification="center",
              font=("Georgia", 17))],
        [sg.T(' '),sg.B('Nueva partida', size=(25, 2), key="-nueva-")],
        [sg.T(' '),sg.B('Continuar partida', size=(25, 2), key="-continuar-")],
        [sg.T(' '),sg.B('Configuración', size=(25, 2), key="-configuracion-")],
        [sg.T(' '),sg.B('Mejores puntajes', size=(25, 2), key="-puntajes-")],
        [sg.T(' '),sg.B('Salir', size=(25, 2), key="-salir-")],
        [sg.T(' '),sg.T("  ", size=(17, 1), justification="center",)]
        ]

    window = sg.Window("ScrabbleAR - Menu", layout)
    
    while True:
        event, _value = window.read()
        #pylint: disable=unused-argument
        if event in ("-salir-", None):
            break

        elif event in "-nueva-":
            with open('configuraciones.json','r') as f:
                configs =json.load(f)
                configs, condicion = config_nuevo_juego(configs)
            with open('configuraciones.json','w') as f:
                json.dump(configs, f, indent= 4)
                if condicion:
                    jugar() #pasar configs para que tenga la configuracion 
            break

        elif event in "-continuar-":
            pass

        elif event in "-configuracion-":
            with open('configuraciones.json') as f:
                configs = json.load(f)
            configurar(configs)

        elif event in "-puntajes-":
            pass
        
    window.close()


    

if __name__ == "__main__":
    #configuracion= {'dificultad': 'Facil', 'tiempo': 30}
    #config(configuracion)
    pantalla_inicial()
    #temporizador(2)
    # with open('configuraciones.json','r') as f:
    #     configs =json.load(f)
    #     configurar(configs)