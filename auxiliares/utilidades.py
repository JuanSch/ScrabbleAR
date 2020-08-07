import platform
import json
import PySimpleGUI as sg


def ruta():
    """
    Evalúa en qué sistema operativo se está ejecutando el programa
    y retorna el caracter que este emplea como separador de jerarquía
    en las rutas de archivos.
    """

    if platform.system() != "Windows":
        char = '/'
    else:
        char = '\\'
    return char


def reglas():
    try:
        with open(f'..{ruta()}archivos{ruta()}Reglas.txt', encoding='UTF-8') as f:
            reglas = f.read()
    except FileNotFoundError:
        reglas = "Ocurrió un error al cargar el archivo"
    try:
        with open(f'..{ruta()}archivos{ruta()}Configurar.txt', encoding='UTF-8') as f:
            configurar = f.read()
    except FileNotFoundError:
        configurar = "Ocurrió un error al cargar el archivo"
    try:
        with open(f'..{ruta()}README.md', encoding='UTF-8') as f:
            readme = f.read()
    except FileNotFoundError:
        readme = "Ocurrió un error al cargar el archivo"

    layout = [[sg.Text('Reglas de Scrabble AR')],
            [sg.Output(size=(35,10), key='-OUTPUT-')],
            [sg.Button('Reglas'),sg.Button('Como configurar'),sg.Button('Informacion adicional')],
            [sg.Button('Volver')]]
    window = sg.Window('', layout)

    while True:
        event, _ = window.read()
        if event in [None, 'Volver']:
            break
        if event in 'Reglas':
            window['-OUTPUT-'].update(reglas)
        if event in 'Como configurar':
            window['-OUTPUT-'].update(configurar)
        if event in 'Informacion adicional':
            window['-OUTPUT-'].Update(readme)
    window.close()


def top10(dificultad=None):
    """
    Genera una ventana que se actualiza con el top ten de mejores puntajes
    la ventana tiene 3 botones facil, medio, dificil, al precionarlo actualiza el output
    """
    try:
        with open(f'..{ruta()}archivos{ruta()}valores_puntajes.json', 'r', encoding='UTF-8') as f:
            dic = json.load(f)
            if dificultad is None:
                top = dic['top10']
            else:
                top = dic['top10'][dificultad]
    except FileNotFoundError:
        dic = crear_valores_puntajes()
        with open(f'..{ruta()}archivos{ruta()}valores_puntajes.json', 'w', encoding='UTF-8') as f:
            json.dump(dic, f, indent=4)
        if dificultad is None:
            top = dic['top10']
        else:
            top = dic['top10'][dificultad]

    if dificultad is None:
        texto_facil = ""
        texto_medio = ""
        texto_dificil = ""
        i = 1
        for elemento in top['Facil']:  # Forma el string por la dificultad
            if elemento[0] != "None":
                texto_facil += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1
        if texto_facil == "":
            texto_facil = 'No hay registro de puntajes'

        i = 1
        for elemento in top['Medio']:  # Forma el string por la dificultad
            if elemento[0] != "None":
                texto_medio += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1
        if texto_medio == "":
            texto_medio = 'No hay registro de puntajes'

        i = 1
        for elemento in top['Dificil']:  # Forma el string por la dificultad
            if elemento[0] != "None":
                texto_dificil += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1
        if texto_dificil == "":
            texto_dificil = 'No hay registro de puntajes'

        layout = [[sg.Text('TOP ten de puntajes')],
            [sg.Output(size=(35,10), key='-OUTPUT-')],
            [sg.Button('Facil'),sg.Button('Medio'),sg.Button('Dificil')],
            [sg.Button('Volver')]]
        window = sg.Window('', layout)

        while True:
            event, _ = window.read()
            if event in [None, 'Volver']:
                break
            if event in 'Facil':
                window['-OUTPUT-'].update(texto_facil)
            if event in 'Medio':
                window['-OUTPUT-'].update(texto_medio)
            if event in 'Dificil':
                window['-OUTPUT-'].update(texto_dificil)
        window.close()
    else:
        i = 1
        texto = ""
        for elemento in top['Dificil']:  # Forma el string por la dificultad
            if elemento[0] != "None":
                texto += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1
        if texto == "":
            texto = 'No hay registro de puntajes'

        layout = [[sg.Text('TOP ten de puntajes')],
                  [sg.Output(size=(35,10), key='-OUTPUT-')],
                  [sg.Button('Salir')]]
        window = sg.Window('', layout)
        condicion = True
        while True:
            event, _ = window.read(timeout=30)
            if event in [None, 'Salir']:
                break
            elif condicion:
                window['-OUTPUT-'].update(texto)
                condicion = False


def crear_valores_puntajes():
    valores_puntajes = {
        "puntos_letra": {
            "a": 1,
            "b": 3,
            "c": 3,
            "d": 2,
            "e": 1,
            "f": 4,
            "g": 2,
            "h": 4,
            "i": 1,
            "j": 8,
            "k": 8,
            "l": 1,
            "m": 3,
            "n": 1,
            "\u00f1": 8,
            "o": 1,
            "p": 3,
            "q": 5,
            "r": 1,
            "s": 1,
            "t": 1,
            "u": 1,
            "v": 4,
            "w": 10,
            "x": 8,
            "y": 4,
            "z": 1
        },
        "Facil": {
            "tablero": {
                "dimensiones": [
                    16,
                    16
                ],
                "2L": [
                    [
                        2,
                        0
                    ],
                    [
                        14,
                        0
                    ],
                    [
                        0,
                        1
                    ],
                    [
                        6,
                        1
                    ],
                    [
                        12,
                        1
                    ],
                    [
                        3,
                        2
                    ],
                    [
                        9,
                        2
                    ],
                    [
                        15,
                        2
                    ],
                    [
                        1,
                        3
                    ],
                    [
                        13,
                        3
                    ],
                    [
                        2,
                        6
                    ],
                    [
                        14,
                        6
                    ],
                    [
                        1,
                        9
                    ],
                    [
                        13,
                        9
                    ],
                    [
                        2,
                        12
                    ],
                    [
                        14,
                        12
                    ],
                    [
                        0,
                        13
                    ],
                    [
                        6,
                        13
                    ],
                    [
                        12,
                        13
                    ],
                    [
                        3,
                        14
                    ],
                    [
                        9,
                        14
                    ],
                    [
                        15,
                        14
                    ],
                    [
                        1,
                        15
                    ],
                    [
                        13,
                        15
                    ]
                ],
                "3L": [
                    [
                        7,
                        0
                    ],
                    [
                        8,
                        3
                    ],
                    [
                        3,
                        4
                    ],
                    [
                        9,
                        4
                    ],
                    [
                        15,
                        4
                    ],
                    [
                        7,
                        6
                    ],
                    [
                        3,
                        7
                    ],
                    [
                        9,
                        7
                    ],
                    [
                        15,
                        7
                    ],
                    [
                        0,
                        8
                    ],
                    [
                        6,
                        8
                    ],
                    [
                        12,
                        8
                    ],
                    [
                        8,
                        9
                    ],
                    [
                        0,
                        11
                    ],
                    [
                        7,
                        11
                    ],
                    [
                        12,
                        11
                    ],
                    [
                        7,
                        12
                    ],
                    [
                        8,
                        15
                    ]
                ],
                "2P": [
                    [
                        5,
                        0
                    ],
                    [
                        11,
                        0
                    ],
                    [
                        4,
                        3
                    ],
                    [
                        10,
                        3
                    ],
                    [
                        0,
                        4
                    ],
                    [
                        6,
                        4
                    ],
                    [
                        12,
                        4
                    ],
                    [
                        3,
                        5
                    ],
                    [
                        9,
                        5
                    ],
                    [
                        15,
                        5
                    ],
                    [
                        5,
                        6
                    ],
                    [
                        11,
                        6
                    ],
                    [
                        4,
                        9
                    ],
                    [
                        10,
                        9
                    ],
                    [
                        0,
                        10
                    ],
                    [
                        6,
                        10
                    ],
                    [
                        12,
                        10
                    ],
                    [
                        3,
                        11
                    ],
                    [
                        9,
                        11
                    ],
                    [
                        15,
                        11
                    ],
                    [
                        5,
                        12
                    ],
                    [
                        11,
                        12
                    ],
                    [
                        4,
                        15
                    ],
                    [
                        10,
                        15
                    ]
                ],
                "3P": [
                    [
                        1,
                        0
                    ],
                    [
                        8,
                        0
                    ],
                    [
                        7,
                        3
                    ],
                    [
                        14,
                        3
                    ],
                    [
                        1,
                        6
                    ],
                    [
                        8,
                        6
                    ],
                    [
                        0,
                        7
                    ],
                    [
                        6,
                        7
                    ],
                    [
                        12,
                        7
                    ],
                    [
                        3,
                        8
                    ],
                    [
                        9,
                        8
                    ],
                    [
                        15,
                        8
                    ],
                    [
                        7,
                        9
                    ],
                    [
                        14,
                        9
                    ],
                    [
                        1,
                        12
                    ],
                    [
                        8,
                        12
                    ],
                    [
                        7,
                        15
                    ],
                    [
                        14,
                        15
                    ]
                ],
                "-3": [
                    [
                        2,
                        2
                    ],
                    [
                        13,
                        2
                    ],
                    [
                        2,
                        13
                    ],
                    [
                        13,
                        13
                    ]
                ]
            },
            "bolsa": [
                [
                    "a",
                    12
                ],
                [
                    "e",
                    14
                ],
                [
                    "i",
                    6
                ],
                [
                    "l",
                    5
                ],
                [
                    "n",
                    7
                ],
                [
                    "o",
                    10
                ],
                [
                    "r",
                    6
                ],
                [
                    "s",
                    8
                ],
                [
                    "t",
                    4
                ],
                [
                    "u",
                    5
                ],
                [
                    "d",
                    5
                ],
                [
                    "g",
                    1
                ],
                [
                    "b",
                    2
                ],
                [
                    "c",
                    4
                ],
                [
                    "m",
                    2
                ],
                [
                    "p",
                    2
                ],
                [
                    "f",
                    1
                ],
                [
                    "h",
                    2
                ],
                [
                    "v",
                    1
                ],
                [
                    "y",
                    2
                ],
                [
                    "q",
                    2
                ],
                [
                    "j",
                    1
                ],
                [
                    "\u00f1",
                    1
                ],
                [
                    "x",
                    1
                ],
                [
                    "z",
                    1
                ]
            ]
        },
        "Medio": {
            "tablero": {
                "dimensiones": [
                    15,
                    15
                ],
                "2L": [
                    [
                        3,
                        0
                    ],
                    [
                        11,
                        0
                    ],
                    [
                        6,
                        2
                    ],
                    [
                        8,
                        2
                    ],
                    [
                        0,
                        3
                    ],
                    [
                        7,
                        3
                    ],
                    [
                        14,
                        3
                    ],
                    [
                        2,
                        6
                    ],
                    [
                        6,
                        6
                    ],
                    [
                        8,
                        6
                    ],
                    [
                        12,
                        6
                    ],
                    [
                        3,
                        7
                    ],
                    [
                        11,
                        7
                    ],
                    [
                        2,
                        8
                    ],
                    [
                        6,
                        8
                    ],
                    [
                        8,
                        8
                    ],
                    [
                        12,
                        8
                    ],
                    [
                        0,
                        11
                    ],
                    [
                        7,
                        11
                    ],
                    [
                        14,
                        11
                    ],
                    [
                        6,
                        12
                    ],
                    [
                        8,
                        12
                    ],
                    [
                        3,
                        14
                    ],
                    [
                        11,
                        14
                    ]
                ],
                "3L": [
                    [
                        5,
                        1
                    ],
                    [
                        9,
                        1
                    ],
                    [
                        1,
                        5
                    ],
                    [
                        5,
                        5
                    ],
                    [
                        9,
                        5
                    ],
                    [
                        13,
                        5
                    ],
                    [
                        13,
                        9
                    ],
                    [
                        1,
                        9
                    ],
                    [
                        5,
                        9
                    ],
                    [
                        9,
                        9
                    ],
                    [
                        5,
                        13
                    ],
                    [
                        9,
                        13
                    ]
                ],
                "2P": [
                    [
                        1,
                        1
                    ],
                    [
                        13,
                        1
                    ],
                    [
                        2,
                        2
                    ],
                    [
                        12,
                        2
                    ],
                    [
                        3,
                        3
                    ],
                    [
                        11,
                        3
                    ],
                    [
                        4,
                        4
                    ],
                    [
                        10,
                        4
                    ],
                    [
                        4,
                        10
                    ],
                    [
                        10,
                        10
                    ],
                    [
                        3,
                        11
                    ],
                    [
                        11,
                        11
                    ],
                    [
                        2,
                        12
                    ],
                    [
                        12,
                        12
                    ],
                    [
                        1,
                        13
                    ],
                    [
                        13,
                        13
                    ]
                ],
                "3P": [
                    [
                        0,
                        0
                    ],
                    [
                        7,
                        0
                    ],
                    [
                        14,
                        0
                    ],
                    [
                        0,
                        7
                    ],
                    [
                        14,
                        7
                    ],
                    [
                        0,
                        14
                    ],
                    [
                        7,
                        14
                    ],
                    [
                        14,
                        14
                    ]
                ],
                "-3": [
                    [
                        7,
                        1
                    ],
                    [
                        1,
                        7
                    ],
                    [
                        13,
                        7
                    ],
                    [
                        7,
                        13
                    ]
                ]
            },
            "bolsa": [
                [
                    "a",
                    9
                ],
                [
                    "e",
                    11
                ],
                [
                    "i",
                    4
                ],
                [
                    "l",
                    3
                ],
                [
                    "n",
                    3
                ],
                [
                    "o",
                    6
                ],
                [
                    "r",
                    3
                ],
                [
                    "s",
                    3
                ],
                [
                    "t",
                    3
                ],
                [
                    "u",
                    3
                ],
                [
                    "d",
                    3
                ],
                [
                    "g",
                    2
                ],
                [
                    "b",
                    2
                ],
                [
                    "c",
                    3
                ],
                [
                    "m",
                    1
                ],
                [
                    "p",
                    2
                ],
                [
                    "f",
                    1
                ],
                [
                    "h",
                    2
                ],
                [
                    "v",
                    1
                ],
                [
                    "y",
                    1
                ],
                [
                    "q",
                    1
                ],
                [
                    "j",
                    1
                ],
                [
                    "\u00f1",
                    1
                ],
                [
                    "x",
                    1
                ],
                [
                    "z",
                    1
                ]
            ]
        },
        "Dificil": {
            "tablero": {
                "dimensiones": [
                    17,
                    17
                ],
                "2L": [
                    [
                        3,
                        0
                    ],
                    [
                        13,
                        0
                    ],
                    [
                        4,
                        1
                    ],
                    [
                        0,
                        3
                    ],
                    [
                        16,
                        3
                    ],
                    [
                        1,
                        4
                    ],
                    [
                        7,
                        4
                    ],
                    [
                        8,
                        5
                    ],
                    [
                        4,
                        7
                    ],
                    [
                        5,
                        8
                    ],
                    [
                        11,
                        8
                    ],
                    [
                        12,
                        9
                    ],
                    [
                        8,
                        11
                    ],
                    [
                        9,
                        12
                    ],
                    [
                        15,
                        12
                    ],
                    [
                        0,
                        13
                    ],
                    [
                        16,
                        13
                    ],
                    [
                        12,
                        15
                    ],
                    [
                        3,
                        16
                    ],
                    [
                        13,
                        16
                    ]
                ],
                "3L": [
                    [
                        0,
                        1
                    ],
                    [
                        8,
                        1
                    ],
                    [
                        16,
                        1
                    ],
                    [
                        4,
                        3
                    ],
                    [
                        3,
                        4
                    ],
                    [
                        5,
                        4
                    ],
                    [
                        4,
                        5
                    ],
                    [
                        0,
                        7
                    ],
                    [
                        8,
                        7
                    ],
                    [
                        16,
                        7
                    ],
                    [
                        0,
                        9
                    ],
                    [
                        8,
                        9
                    ],
                    [
                        16,
                        9
                    ],
                    [
                        12,
                        11
                    ],
                    [
                        11,
                        12
                    ],
                    [
                        13,
                        12
                    ],
                    [
                        12,
                        13
                    ],
                    [
                        0,
                        15
                    ],
                    [
                        8,
                        15
                    ],
                    [
                        16,
                        15
                    ]
                ],
                "2P": [
                    [
                        5,
                        0
                    ],
                    [
                        11,
                        0
                    ],
                    [
                        12,
                        1
                    ],
                    [
                        8,
                        3
                    ],
                    [
                        9,
                        4
                    ],
                    [
                        15,
                        4
                    ],
                    [
                        16,
                        5
                    ],
                    [
                        12,
                        7
                    ],
                    [
                        3,
                        8
                    ],
                    [
                        13,
                        8
                    ],
                    [
                        4,
                        9
                    ],
                    [
                        0,
                        11
                    ],
                    [
                        16,
                        11
                    ],
                    [
                        1,
                        12
                    ],
                    [
                        7,
                        12
                    ],
                    [
                        8,
                        13
                    ],
                    [
                        4,
                        15
                    ],
                    [
                        5,
                        16
                    ],
                    [
                        11,
                        16
                    ]
                ],
                "3P": [
                    [
                        1,
                        0
                    ],
                    [
                        7,
                        0
                    ],
                    [
                        9,
                        0
                    ],
                    [
                        15,
                        0
                    ],
                    [
                        12,
                        3
                    ],
                    [
                        11,
                        4
                    ],
                    [
                        13,
                        4
                    ],
                    [
                        12,
                        5
                    ],
                    [
                        1,
                        8
                    ],
                    [
                        7,
                        8
                    ],
                    [
                        9,
                        8
                    ],
                    [
                        15,
                        8
                    ],
                    [
                        4,
                        11
                    ],
                    [
                        3,
                        12
                    ],
                    [
                        5,
                        12
                    ],
                    [
                        4,
                        13
                    ],
                    [
                        1,
                        16
                    ],
                    [
                        7,
                        16
                    ],
                    [
                        9,
                        16
                    ],
                    [
                        15,
                        16
                    ]
                ],
                "-3": [
                    [
                        0,
                        0
                    ],
                    [
                        4,
                        0
                    ],
                    [
                        8,
                        0
                    ],
                    [
                        12,
                        0
                    ],
                    [
                        16,
                        0
                    ],
                    [
                        0,
                        4
                    ],
                    [
                        4,
                        4
                    ],
                    [
                        8,
                        4
                    ],
                    [
                        12,
                        4
                    ],
                    [
                        16,
                        4
                    ],
                    [
                        0,
                        8
                    ],
                    [
                        4,
                        8
                    ],
                    [
                        8,
                        8
                    ],
                    [
                        12,
                        8
                    ],
                    [
                        16,
                        8
                    ],
                    [
                        0,
                        12
                    ],
                    [
                        4,
                        12
                    ],
                    [
                        8,
                        12
                    ],
                    [
                        12,
                        12
                    ],
                    [
                        16,
                        12
                    ],
                    [
                        0,
                        16
                    ],
                    [
                        4,
                        16
                    ],
                    [
                        8,
                        16
                    ],
                    [
                        12,
                        16
                    ],
                    [
                        16,
                        16
                    ]
                ]
            },
            "bolsa": [
                [
                    "a",
                    5
                ],
                [
                    "e",
                    5
                ],
                [
                    "i",
                    2
                ],
                [
                    "l",
                    2
                ],
                [
                    "n",
                    2
                ],
                [
                    "o",
                    4
                ],
                [
                    "r",
                    2
                ],
                [
                    "s",
                    2
                ],
                [
                    "t",
                    2
                ],
                [
                    "u",
                    2
                ],
                [
                    "d",
                    2
                ],
                [
                    "g",
                    1
                ],
                [
                    "b",
                    1
                ],
                [
                    "c",
                    2
                ],
                [
                    "m",
                    1
                ],
                [
                    "p",
                    1
                ],
                [
                    "f",
                    1
                ],
                [
                    "h",
                    2
                ],
                [
                    "v",
                    1
                ],
                [
                    "y",
                    1
                ],
                [
                    "q",
                    1
                ],
                [
                    "j",
                    1
                ],
                [
                    "\u00f1",
                    1
                ],
                [
                    "x",
                    1
                ],
                [
                    "z",
                    1
                ]
            ]
        },
        "Personalizada": {
            "bolsa": [
                [
                    "a",
                    12
                ],
                [
                    "b",
                    12
                ],
                [
                    "c",
                    12
                ],
                [
                    "d",
                    12
                ],
                [
                    "e",
                    8
                ],
                [
                    "f",
                    8
                ],
                [
                    "g",
                    12
                ],
                [
                    "h",
                    4
                ],
                [
                    "i",
                    1
                ],
                [
                    "j",
                    3
                ],
                [
                    "k",
                    8
                ],
                [
                    "l",
                    1
                ],
                [
                    "m",
                    5
                ],
                [
                    "n",
                    1
                ],
                [
                    "\u00f1",
                    5
                ],
                [
                    "o",
                    1
                ],
                [
                    "p",
                    3
                ],
                [
                    "q",
                    5
                ],
                [
                    "r",
                    1
                ],
                [
                    "s",
                    1
                ],
                [
                    "t",
                    1
                ],
                [
                    "u",
                    1
                ],
                [
                    "v",
                    12
                ],
                [
                    "w",
                    10
                ],
                [
                    "x",
                    8
                ],
                [
                    "y",
                    3
                ],
                [
                    "z",
                    1
                ]
            ],
            "dificultad_IA": "Medio",
            "dificultad_Tablero": "Medio",
            "puntos_letra": {
                "a": 12,
                "b": 3,
                "c": 3,
                "d": 2,
                "e": 1,
                "f": 4,
                "g": 2,
                "h": 4,
                "i": 1,
                "j": 8,
                "k": 8,
                "l": 1,
                "m": 3,
                "n": 1,
                "\u00f1": 8,
                "o": 1,
                "p": 3,
                "q": 5,
                "r": 1,
                "s": 1,
                "t": 1,
                "u": 1,
                "v": 4,
                "w": 10,
                "x": 8,
                "y": 4,
                "z": 1
            }
        },
        "top10": {
            "Facil": [
                [
                    "",
                    00
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ]
            ],
            "Medio": [
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ]
            ],
            "Dificil": [
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ]
            ]
        }
        }
    return valores_puntajes
