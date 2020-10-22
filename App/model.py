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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
import datetime
from Sorting import shellsort as ls

assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None,
                'hoursIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['hoursIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)                
    return analyzer

# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================


def addCrime(analyzer, crime):
    """
    """
    lt.addLast(analyzer['accidents'], crime)
    updateDateIndex(analyzer['dateIndex'], crime)
    updateHoursIndex(analyzer['hoursIndex'], crime)
    return analyzer

# ==============================
# Arbol de fechas
# ==============================

def updateDateIndex(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['Start_Time']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, crimedate.date())
    if entry is None:
        datentry = newDataEntry(crime)
        om.put(map, crimedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    lst = datentry['lstcrimes']
    lt.addLast(lst, crime)
    return map

# ==============================
# Arbol de tiempo
# ==============================

def updateHoursIndex(map, crime):
    occurreddate = crime['Start_Time']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    tiempos = redondear_horas(crimedate.time())
    entry = om.get(map, tiempos)
    if entry is None:
        datentry = newDataHours(crime)
        om.put(map, tiempos, datentry)
    else:
        datentry = me.getValue(entry)
    lst = datentry['lstaccidents']
    lt.addLast(lst, crime)
    return map

# ==============================
# Función de redondeo
# ==============================

def redondear_horas(tiempo):
    tiempo = tiempo.replace(second = 0)
    minuto = tiempo.minute
    h = tiempo.hour + 1
    if minuto <= 15:
        tiempo = tiempo.replace(minute= 0)
    elif minuto > 15 and minuto <= 45:
        tiempo = tiempo.replace(minute= 30)
    elif minuto > 45 and minuto <= 59:
        if h == 24:
            h = 0
        tiempo = tiempo.replace(hour= h) 
        tiempo = tiempo.replace(minute= 0)
    return tiempo

# ==============================
# Diccionarios para almacenar información
# ==============================


def newDataHours(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'lstaccidents': None}

    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'states': None, 'lstcrimes': None}
    #entry['offenseIndex'] = m.newMap(numelements=30,
                                     #maptype='PROBING',
                                     #comparefunction=compareIds)
    entry['lstcrimes'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


# ==============================
# Funciones de datos de los arboles
# ==============================


def crimesSize(analyzer):
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    return om.maxKey(analyzer['dateIndex'])




def indexHeight1(analyzer):
    return om.height(analyzer['hoursIndex'])


def indexSize1(analyzer):
    return om.size(analyzer['hoursIndex'])


def minKey1(analyzer):
    return om.minKey(analyzer['hoursIndex'])


def maxKey1(analyzer):
    return om.maxKey(analyzer['hoursIndex'])




# ==============================
# Requerimiento 1
# ==============================

def getCrimesByRange(analyzer, initialDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.get(analyzer['dateIndex'], initialDate)
    entry = me.getValue(lst)
    fila = entry['lstcrimes']
    topSeverity(fila)
    return entry

# ==============================
# Requerimiento 2
# ==============================

def getCrimesByRangeFinal(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    dic={}
    cont=0
    lst = om.keys(analyzer['dateIndex'], initialDate, finalDate)
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        crime = it.next(iterator)
        date2 = datetime.datetime.strptime(str(crime), '%Y-%m-%d')
        llave = om.get(analyzer['dateIndex'], date2.date())
        entry = me.getValue(llave)
        fecha = str(crime)
        cont+=lt.size(entry['lstcrimes'])
        if fecha not in dic:
            dic[fecha] = lt.size(entry['lstcrimes'])
    m = (max(dic.values()))
    for i in dic:
        if m == dic[i]:
            va = "La fecha con más accidentes es: " + i + ' con una cantidad de: ' + str(dic[i])
    print("La cantidad total de accidentes anterior a la fecha dada fue de: " + str(cont))
    print(va)

# ==============================
# Requerimiento 3
# ==============================
def Req_3(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    dicc={}
    cont=0 
    lst = om.keys(analyzer['dateIndex'], initialDate, finalDate)
    iterator= it.newIterator(lst)
    while it.hasNext(iterator):
        crime= it.next(iterator)
        date2= datetime.datetime.strptime(str(crime), "%Y-%m-%d")
        llave= om.get(analyzer["dateIndex"], date2.date())
        entry=me.getValue(llave)
        cont+=lt.size(entry["lstcrimes"])
        iterator2 = it.newIterator(entry['lstcrimes'])
        while it.hasNext(iterator2):
            crime2 = it.next(iterator2)
            estado = str(crime2['Severity'])
            if estado in dicc:
                dicc[estado] += 1
            else:
                dicc[estado] = 1
    l = (max(dicc.values()))
    for i in dicc:
        if l == dicc[i]:
            ve = "\n La categoria con más accidentes en el rango es: " + i + ' con una cantidad de: ' + str(dicc[i])
    print(dicc)
    print(ve)
    print("La cantidad de accidentes en el rango dado fue de: " + str(cont))


# ==============================
# Requerimiento 5
# ==============================

def getAccidentstimeByRange(analyzer, initialDate, finalDate):
    dicc = {}
    cont = 0
    lst = om.keys(analyzer['hoursIndex'], initialDate, finalDate)
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        crime = it.next(iterator)
        date2 = datetime.datetime.strptime(str(crime), '%H:%M:%S')
        llave = om.get(analyzer['hoursIndex'], date2.time())
        entry = me.getValue(llave)
        tiempo = str(crime)
        cont += lt.size(entry['lstaccidents'])
        iterator2 = it.newIterator(entry['lstaccidents'])
        while it.hasNext(iterator2):
            crime2 = it.next(iterator2)
            estado = crime2['Severity']
            if estado in dicc:
                dicc[estado] += 1
            else:
                dicc[estado] = 1
    print("En el rango con tiempo se obtuvieron los siguientes datos: \n")
    for i in dicc:
        if i == "1":
            print("Con una severidad de " + i + " son " + str(dicc[i]) + " accidentes" + " con un porcentaje de: " + str(round((dicc[i]/cont), 2)*100) + "%")
        if i == "2":
            print("Con una severidad de " + i + " son " + str(dicc[i]) + " accidentes" + " con un porcentaje de: " + str(round((dicc[i]/cont), 2)*100) + "%")
        if i == "3":
            print("Con una severidad de " + i + " son " + str(dicc[i]) + " accidentes" + " con un porcentaje de: " + str(round((dicc[i]/cont), 2)*100) + "%")
        if i == "4":
            print("Con una severidad de " + i + " son " + str(dicc[i]) + " accidentes" + " con un porcentaje de: " + str(round((dicc[i]/cont), 2)*100) + "%")   
    print("\nTiene un total de: " + str(cont) + " accidentes")




# ==============================
# Requerimiento 4
# ==============================


def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    dicc = {}
    dicct = {}
    lst = om.keys(analyzer['dateIndex'], initialDate, finalDate)
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        crime = it.next(iterator)
        date2 = datetime.datetime.strptime(str(crime), '%Y-%m-%d')
        llave = om.get(analyzer['dateIndex'], date2.date())
        entry = me.getValue(llave)
        fecha = str(crime)
        if fecha not in dicct:
            dicct[fecha] = lt.size(entry['lstcrimes'])
        iterator2 = it.newIterator(entry['lstcrimes'])
        while it.hasNext(iterator2):
            crime2 = it.next(iterator2)
            estado = crime2['State']
            if estado in dicc:
                dicc[estado] += 1
            else:
                dicc[estado] = 1
    m = (max(dicct.values()))
    for i in dicct:
        if m == dicct[i]:
            va = "\nLa fecha con más accidentes en el rango es: " + i + ' con una cantidad de: ' + str(dicct[i])
    print(va)
    l = (max(dicc.values()))
    for i in dicc:
        if l == dicc[i]:
            ve = "\nEl estado con más accidentes en el rango es: " + i + ' con una cantidad de: ' + str(dicc[i])
    print(ve)
    return None











# ==============================
# Funciones de Ordenamiento
# ==============================


def topSeverity(lstmovies):
    monika = ls.shellSort(lstmovies, topAccidents)
    return monika

def topAccidents(element1, element2):
    if (int(element1['Severity']) > int(element2['Severity'])):
        return True
    return False


# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1