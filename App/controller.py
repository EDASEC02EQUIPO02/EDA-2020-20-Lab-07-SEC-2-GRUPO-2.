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

import config as cf
from App import model
import datetime
import csv
from time import process_time


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    t1 = process_time()
    crimesfile = cf.data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"), delimiter=",")
    for crime in input_file:
        model.addCrime(analyzer, crime)
    t2  = process_time()
    print("El tiempo de procesamiento es de: ", t2 - t1)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________





def crimesSize(analyzer):
    return model.crimesSize(analyzer)


def indexHeight(analyzer):
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    return model.indexSize(analyzer)


def minKey(analyzer):
    return model.minKey(analyzer)


def maxKey(analyzer):
    return model.maxKey(analyzer)



def indexHeight1(analyzer):
    return model.indexHeight1(analyzer)


def indexSize1(analyzer):
    return model.indexSize1(analyzer)


def minKey1(analyzer):
    return model.minKey1(analyzer)


def maxKey1(analyzer):
    return model.maxKey1(analyzer)




def getCrimesByRange(analyzer, initialDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    
    return model.getCrimesByRange(analyzer, initialDate.date())

def getCrimesByRangeFinal(analyzer, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    fechaI= str(minKey(analyzer))
    initialDate = datetime.datetime.strptime(fechaI, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')

    return model.getCrimesByRangeFinal(analyzer, initialDate.date(), finalDate.date())

def Requerimiento_3(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.Req_3(analyzer, initialDate.date(),
                                  finalDate.date())



def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsByRange(analyzer, initialDate.date(),
                                  finalDate.date())


def getAccidentstimeByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%H:%M:%S')
    finalDate = datetime.datetime.strptime(finalDate, '%H:%M:%S')
    inicio = model.redondear_horas(initialDate.time())
    final = model.redondear_horas(finalDate.time())
    return model.getAccidentstimeByRange(analyzer, inicio,
                                  final)

#def getAccidentsByZone(analyzer, latitud, longitud, radio):
