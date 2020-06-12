from pattern.es import lexicon, spelling, parse
from pattern.web import Wiktionary
import json

def elegir_palabra(letras, dificultad):
    """
    Esta funcion Elige la palabra mas adecuada para nuestra IA y así ganar la mayor cantidad de puntos 
    primero se fija que palabras puede armar con sus letras y depues evalua cual es la palabra que más puntaje da
    """
    def sirve(lista_uno,lista_dos):
        """
        Creo un diccionario con key = letra & value = cantidad de apariciones de la key en la lista
        si el diccionario dos tiene las miscas keys que el uno yu el valor del dic_dos en la key es mayor o igual a la del dic_uno, en cada key 
            entonces puedo armar una palabra 
        """
        dic_uno = {}
        dic_dos = {}

        for key in lista_uno:
            if key in dic_uno:
                dic_uno[key] = dic_uno[key] + 1
            else:
                dic_uno[key] = 1

        for key in lista_dos:
            if key in dic_dos:
                dic_dos[key] = dic_dos[key] + 1
            else:
                dic_dos[key] = 1
        
        dic_uno_keys  = []
        for key in dic_uno:
            dic_uno_keys.append(key)

        cumple = False
        for key in dic_dos:
            if key in dic_uno_keys:
                cumple = True
            else:
                cumple = False
                break
        condicion = False
        if cumple:
            for key in dic_dos:
                if dic_uno[key] >= dic_dos[key]:
                    condicion = True
                else:
                    condicion = False
                    break
        return(condicion)
    def por_dificulad(palabras_utilies, dificultad):
    
        def dificil(palabras):
            """
            cargo los puntajes y me fijo cual es la palabra que mayor puntaje da 
            """
            max = 0
            palabra_elegida = str
            with open('valores_puntajes.json') as f:
                puntajes = json.load(f)
                
            for palabra in palabras:
                puntaje_palabra_actual = 0
                for char in palabra:
                    puntaje_palabra_actual += puntajes['puntos_letra'][char]
                if puntaje_palabra_actual > max:
                    max = puntaje_palabra_actual
                    palabra_elegida = palabra
                    
            return(palabra_elegida)

        def medio(palabras):
            with open('valores_puntajes.json') as f:
                puntajes = json.load(f)

            palabra_elegida = ''
            palabras_posibles = []
            for palabra in palabras:
                puntaje_palabra_actual = 0
                for char in palabra:
                    puntaje_palabra_actual += puntajes['puntos_letra'][char]
                palabras_posibles.append(palabra, puntaje_palabra_actual)
            
            palabra_elegida =  palabras_posibles[len(palabras_posibles)//2]
            return(palabra_elegida)

        def facil(palabras):
            palabra_elegida = str
            with open('valores_puntajes.json') as f:
                puntajes = json.load(f)
            min = 999
            for palabra in palabras:
                puntaje_palabra_actual = 0
                for char in palabra:
                    puntaje_palabra_actual += puntajes['puntos_letra'][char]
                if puntaje_palabra_actual < min:
                    min = puntaje_palabra_actual
                    palabra_elegida = palabra
            return(palabra_elegida)

        if dificultad == 'facil':
            return(facil(palabras_utilies))
        elif dificultad == "dificil":
            return(dificil(palabras_utilies))
        else:
            return(medio(palabras_utilies))
    

    letras.sort()
    palabras_posibles = []
    for palabra in lexicon.keys():
        if palabra in spelling.keys(): #por cada palabra que tiene pattern
            palabra_deletrada = []
            for char in palabra: #la separamos por caracteres y la ordenamos 
                palabra_deletrada.append(char)
            palabra_deletrada.sort()
            if (sirve(letras, palabra_deletrada) ): #si la lista de letras ordenadas es igual a la lista de letras de la IA
                palabras_posibles.append(palabra)  #agregamos la palabra a nuestra lista de palabras utiles
    

    palabras_posibles_dos = [] #esto no está al pedo, es para hacer la busqueda de wiktionary mas rapida
    for palabra in palabras_posibles:
        if len(palabra) > 2:
            palabras_posibles_dos.append(palabra)
    
    if len(palabras_posibles_dos) == 0:
        return(None)
    palabras_utilies = []
    w = Wiktionary(language="es")
    for palabra in palabras_posibles_dos:
        cumple = False
        analisis = parse(palabra).split('/')
        if (analisis[1] in ('AO','JJ','AQ','DI','DT','NC','NN','NCS','NCP','NNS','NP','NNP','W','VAG','VBG','VAI','VAN','MD','VAS','VMG','VMI','VB','VMM','VMN','VMP','VBN','VMS','VSG','VSI','VSN','VSP','VSS')):
            article=w.search(palabra)
            if article!=None:
                cumple= True
            else:
                cumple = False
        if cumple:
            palabras_utilies.append(palabra)
    if len(palabras_utilies) == 1:
        return(palabras_utilies)
    elif(len(palabras_utilies) > 1):
        print(palabras_utilies)
        return(por_dificulad(palabras_utilies, dificultad))
    else:
        return(None)


def validar_palabra(palabra):
    palabra = parse(palabra).split('/')
    if palabra[1] in ('AO','JJ','AQ','DI','DT','VAG','VBG','VAI','VAN','MD','VAS','VMG','VMI','VB','VMM','VMN','VMP','VBN','VMS','VSG','VSI','VSN','VSP','VSS'): #VB:verbo  ,  JJ:adjetivo
        if palabra[0] not in lexicon.keys():
            if palabra[0] not in spelling.keys():
                w = Wiktionary(language="es")
                article = w.search(palabra[0])
                if article != None :
                    return True
                else:
                    return  False
            else:
                return True
        else:
            return True
    elif palabra[1] in ('NC','NN','NCS','NCP','NNS','NP','NNP','W'): #sustantivo 
        w = Wiktionary(language="es")
        article = w.search(palabra[0])
        if article != None :
            return True
        else:
            return False


if __name__ == '__main__':
    dificultad = 'dificil'
    ejemplo = ['s','g','a','v','m','r','h']
    pas= elegir_palabra(ejemplo, dificultad)   
    print(pas)
    #print(validar_palabra('asada'))

