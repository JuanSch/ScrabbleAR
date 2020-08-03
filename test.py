# TEST DIFICULTADES IA

# import IA as ia
# import logica as lg
#
# fichas = {'1': lg.Ficha('a', 1),
#           '2': lg.Ficha('t', 2),
#           '3': lg.Ficha('a', 1),
#           '4': lg.Ficha('r', 4),
#           '5': lg.Ficha('p', 3),
#           }
#
# print(f'Palabra fácil: {ia.elegir_palabra(fichas, "Facil")}')
# print(f'Palabra medio: {ia.elegir_palabra(fichas, "Medio")}')
# print(f'Palabra difícil: {ia.elegir_palabra(fichas, "Dificil")}')


# TEST WIKTIONARY

# from pattern.web import Wiktionary
#
#
# def validar(palabra):
#     w = Wiktionary(language="es")
#     article = w.search(palabra)
#     if article is not None:
#         secciones = [x.title for x in article.sections]
#         res = ''
#         if 'Español' not in secciones:
#             res = 'no'
#         print(f'La palabra {palabra} {res} existe en el español')
#     else:
#         print(f'No existe un artículo para la palabra {palabra} ')
#
#
# palabras = [('at', 3), ('ta', 3), ('ar', 5), ('ra', 5), ('tr', 6), ('apta', 7), ('pata', 7), ('tra', 7), ('atar', 8), ('par', 8), ('rata', 8), ('arpa', 9), ('para', 9), ('part', 10), ('prat', 10), ('parta', 11)]
# palabras = [x[0] for x in palabras]
# print(palabras)
#
# for palabra in palabras:
#     validar(palabra)
#
#
# TEST CASILLAS VALIDAS
#
# def test_ocupadas(tablero):
#     ocupadas = {}
#     # print('Ocupadas:\n')
#     for x in range(15):
#         # string = ''
#         for y in range(15):
#             ocupadas[(x, y)] = not tablero.getcasilla((x, y)).ocupado
#             # string = ' '.join([string, f'({x}, {y}): {casilla.ocupado}'])
#         # print(string)
#     return ocupadas
#
#
# def test_posibles(tablero):
#     posibles = {}
#     # print('Posibles:\n')
#     for x in range(15):
#         # string = ''
#         for y in range(15):
#             posibles[(x, y)] = (x, y) in tablero.getposibles()
#             # string = ' '.join([string, f'({x}, {y}): {(x, y) in tablero.getposibles()}'])
#         # print(string)
#     return posibles
#
#
# def print_ocupadas(tablero):
#     print('Ocupadas:\n')
#     for x in range(15):
#         string = ''
#         for y in range(15):
#             string = ' '.join([string, f'({x}, {y}): {not tablero.getcasilla((x, y)).ocupado}'])
#         print(string)
#
#
# def print_posibles(tablero):
#     print('Posibles:\n')
#     for x in range(15):
#         string = ''
#         for y in range(15):
#             string = ' '.join([string, f'({x}, {y}): {(x, y) in tablero.getposibles()}'])
#         print(string)
