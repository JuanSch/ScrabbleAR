from pattern.es import lexicon, spelling, parse
from pattern.web import Wiktionary
import concurrent.futures
import json


def validar_palabra(palabra):
    """
    Comprueba que el string que se pasa como palabra sea una palabra valida
    retorna True si lo es. Caso contrario retorna False
    """
    palabra = parse(palabra).split('/')
    if palabra[1] in ('AO','JJ','AQ','DI','DT','VAG','VBG','VAI','VAN','MD',
                      'VAS','VMG','VMI','VB','VMM','VMN','VMP','VBN','VMS',
                      'VSG','VSI','VSN','VSP','VSS'):  # VB:verbo, JJ:adjetivo
        if palabra[0] not in (lexicon.keys() or spelling.keys()):
            # si es adj o verbo y no esta en el lexicon
            # ni el spelling comprueba con wiktionary
            w = Wiktionary(language="es")
            article = w.search(palabra[0])
            if article is not None:
                return True
            else:
                return False
        else:
            return True
    elif palabra[1] in ('NC','NN','NCS','NCP','NNS','NP','NNP','W'):
        # sustantivo comprueba con wiktionary
        w = Wiktionary(language="es")
        article = w.search(palabra[0])
        if article is not None:
            return True
        else:
            return False


def calcular_puntaje(palabra):
    """
    Funcion que calcula el puntaje de la palabra ingresada 
    """
    puntaje = 0
    with open('valores_puntajes.json') as f: # Abro el archivo
        puntajes = json.load(f)
    for char in palabra:
        puntaje += puntajes['puntos_letra'][char] # por cada caracter evaluo cuanto vale y lo sumo al total
    return puntaje


def elegir_palabra(fichas, dificultad, long_maxima=7):

    def elegir_palabra_dos(fichas, dificultad, long_maxima):
        """
        Esta funcion elige la palabra mas adecuada para la IA
        (la que le permita ganar la mayor cantidad de puntos)
        primero se fija que palabras puede armar con sus letras
        y depues evalua cual es la palabra que más puntaje da
        """
        def sirve(lista_uno, lista_dos):
            """
            Creo un diccionario con key = letra & value = cantidad
            de apariciones de la key en la lista.
            Si el diccionario dos tiene las mismas keys que el uno
            y el valor del dic_dos en la key es mayor o igual
            a la del dic_uno en cada key entonces puedo armar una palabra
            """
            dic_uno = {}
            dic_dos = {}

            for key in lista_uno:  # Genero un diccionario con key = letra y value = cantidad de apariciones
                if key in dic_uno:
                    dic_uno[key] = dic_uno[key] + 1
                else:
                    dic_uno[key] = 1 

            for key in lista_dos:  # Genero un diccionario con key = letra y value = cantidad de apariciones
                if key in dic_dos:
                    dic_dos[key] = dic_dos[key] + 1
                else:
                    dic_dos[key] = 1

            # si el diccionario dos tiene las mismas letras que el diccionario uno
            cumple_valor = all([key in list(dic_uno.keys())
                                for key in list(dic_dos.keys())])
            if cumple_valor:
                # si las apariciones de cada letra en el diccionario dos
                # es menor o iugal a las del diccionario uno
                cumple_cant = all([dic_uno[key] >= dic_dos[key]
                                   for key in dic_dos.keys()])
                if cumple_cant:
                    return True
            return False

        def calcular_puntaje_IA(palabra, puntos):
            puntaje = 0
            for char in palabra:
                puntaje += puntos[char]
            return puntaje

        def por_dificulad(palabras_utiles, dificultad, puntaje_letra):
            """
            Segun la dificultad elige una u otra palaba
            """
            def ordenar_puntos(palabras, puntaje_letra):
                palabra_puntos = [(p, calcular_puntaje_IA(p, puntaje_letra))
                                  for p in palabras]
                palabra_puntos.sort(key=lambda x: x[1])
                return palabra_puntos

            seleccion = {'Facil': lambda x: x[0][0],
                         'Medio': lambda x: x[len(x)//2][0],
                         'Dificil': lambda x: x[-1][0]}
            palabras_puntos = ordenar_puntos(palabras_utiles, puntaje_letra)
            print(palabras_puntos)
            return seleccion[dificultad](palabras_puntos)

        letras = [v.letra for _k, v in fichas.items()]
        puntaje_letra = {v.letra: v.valor for _k, v in fichas.items()}
        letras.sort()   # Genero la lista de letras
        
        palabras_posibles = []
        for palabra in lexicon.keys():
            if 2 <= len(palabra) <= long_maxima:  # elimina las palabras de menos de 2 y mas de (max) caracteres
                if palabra in spelling.keys():  # por cada palabra que tiene pattern
                    palabra_deletreada = [char for char in palabra]  # la separamos por caracteres,
                    palabra_deletreada.sort()
                    # generamos una lista y la ordenamos
                    if sirve(letras, palabra_deletreada): # Comparamos ambas listas y si me sirve
                        palabras_posibles.append(palabra)  # agregamos la palabra a nuestra lista de palabras utiles

        if len(palabras_posibles) == 0:
            return None

        palabras_utiles = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = []
            for palabra in palabras_posibles:  # Creo una lista de threads
                results.append(executor.submit(validar_palabra, palabra))
        
            resultados = []
            for f in concurrent.futures.as_completed(results):  # genero un iterador
                resultados.append(f.result())  # f es un objeto que tiene método result que te da el return de "cada thread"
        
        for i in range(len(resultados)):  # si la palabra existe la agrego a la lista de palabras utiles
            if resultados[i] is True:
                palabras_utiles.append(palabras_posibles[i])

        if len(palabras_utiles) == 1:
            return palabras_utiles
        elif len(palabras_utiles) > 1:
            return por_dificulad(palabras_utiles, dificultad, puntaje_letra)
        else:
            return None

    # A veces ocurre algun error por parte de wiktionary ajeno
    # al codigo escrito por los aulumnos; cuando sucede
    # solo volvemos a ejecutar el codigo
    try: 
        try:
            return elegir_palabra_dos(fichas, dificultad, long_maxima)
        except:
            return elegir_palabra_dos(fichas, dificultad, long_maxima)
    except:
        return elegir_palabra_dos(fichas, dificultad, long_maxima)


if __name__ == '__main__':
    # dificultad = 'dificil'
    # ejemplo = ['a','p','q','d','t','z','n','a','o','o','a']
    # res= elegir_palabra(ejemplo, dificultad)   
    # print(res, calcular_puntaje(res))
    # palabras = ['humanidad','humano','persona','gente','hombre','mujer','niño','niña','adolescente','adulto','adulta','anciano','ancaina','zapo','pho','albol']
    # for palabra in palabras:
    #     print(validar_palabra(palabra))
    #$%Comprobar espacio en tablero para la palabra
    pass
