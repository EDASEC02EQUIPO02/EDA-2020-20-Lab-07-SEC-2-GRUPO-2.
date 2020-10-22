"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""





# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


crimefile = 'crime-utf8.csv'
crimefileus = 'us_accidents_small.csv'
accidentsfile = 'US_Accidents_Dec19.csv'
accidents2016 = 'us_accidents_dis_2016.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1")
    print("4- Requerimento 2")
    print("5- Requerimento 3")
    print("6- Requerimento 4")
    print("7- Requerimento 5 (grupal)")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de los accidentes ....")
        print("\nCargando información de los accidentes ....")
        controller.loadData(cont, accidentsfile)
        print('Accidentes cargados: ' + str(controller.crimesSize(cont)))
        print('\nInformación sobre el arbol de fechas: \n')        
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        print('\nInformación sobre el arbol de tiempo: \n')
        print('Altura del arbol: ' + str(controller.indexHeight1(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize1(cont)))
        print('Menor Llave: ' + str(controller.minKey1(cont)))
        print('Mayor Llave: ' + str(controller.maxKey1(cont)))       

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha específica: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        lst = controller.getCrimesByRange(cont, initialDate)
        print('Total de accidentes: ' + str(lt.size(lst['lstcrimes'])))
        iterator = it.newIterator(lst['lstcrimes'])
        while it.hasNext(iterator):
            crime = it.next(iterator)
            print("Descripción del accidente: " + crime['Description'] +', ' + "Su severidad fue de: " + str(crime['Severity']))
    
    elif int(inputs[0]) == 4:
        print("\nBuscando accidentes anteriores a una fecha específica: ")
        finalDate = input("Fecha (YYYY-MM-DD): ")
        lst = controller.getCrimesByRangeFinal(cont, finalDate)

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Inicial (YYYY-MM-DD): ")
        lst= controller.Requerimiento_3(cont, initialDate,finalDate)

    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: ")
        print("\nBuscando accidentes en un rango de fechas: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Inicial (YYYY-MM-DD): ")
        lst = controller.getAccidentsByRange(cont, initialDate, finalDate)

    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: ")
        print("\nBuscando accidentes en un rango de fechas: ")
        initialDate = input("Rango Inicial (HH:MM:SS): ")
        finalDate = input("Rango Inicial (HH:MM:SS): ")
        lst = controller.getAccidentstimeByRange(cont, initialDate, finalDate)

    else:
        sys.exit(0)
sys.exit(0)
