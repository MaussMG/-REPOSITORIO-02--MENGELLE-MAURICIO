# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 23:03:51 2020

@author: Mau
"""

import csv

#Lista auxiliar para guardar los datos del csv
lista_datos=[]

with open("synergy_logistics_database.csv","r") as archivo_csv:
    
    archivo = csv.reader(archivo_csv)
    for linea in archivo:
        lista_datos.append(linea) #agregamos cada linea a la lista
#corregimos error de codificacion
lista_datos[0][0]= "register_id"

#Funcion que te extrae la informacion de las "Exports" o de "Imports"
def extraer_info(tipo):
    tipo_direccion = tipo
    ruta_tipo=[]
    for registro in lista_datos:
        if registro[1]== tipo_direccion:
            ruta_tipo.append(registro)
    return ruta_tipo

# Funcion que te devuelve el valor total del importe ganado en una lista
def total_ingreso(lista):
    suma=0
    for registro in lista:
        suma+=int(registro[9])
    return suma
    
    
#Hacemos el conteo de cuantas veces aparece una ruta y su agregado del importe por ruta
def conteo_rutas(ruta_tipo):
    rutas_existentes=set()
    conteo_rutas=[]
    for registro in ruta_tipo:
        contador=0
        total_ingreso=0
        ruta_actual=(registro[2],registro[3])
        
        if ruta_actual not in rutas_existentes:
            rutas_existentes.add((registro[2],registro[3]))
            
            for nuevo_registro in ruta_tipo:
                if nuevo_registro[2]==registro[2] and nuevo_registro[3]==registro[3]:
                    contador +=1
                    total_ingreso+= int(nuevo_registro[9])
            conteo_rutas.append([registro[2],registro[3],contador,total_ingreso])        
                    
    return conteo_rutas            

################################### OPCION 1
    
#Funcion que imprimiremos en el menu principal
def opcion1(tipo):
    ruta_exp_imp = extraer_info(tipo)
    conteo_exp_imp=conteo_rutas(ruta_exp_imp)
    
    conteo_exp_imp.sort(reverse=True, key = lambda x:x[2])
    
    ingreso_top10_rutas=0
    for ruta in conteo_exp_imp[0:10]:
        ingreso_top10_rutas  += ruta[3]  
        
    print("El ingreso total acumulado es: ", ingreso_top10_rutas)
    print("Lo que representa el: ", ingreso_top10_rutas*100/total_ingreso(ruta_exp_imp),"% \n")
    
    
    print("El ingreso 'abandonado' es de: ", total_ingreso(ruta_exp_imp)-ingreso_top10_rutas)
    print("El ingreso 'abandonado' tiene un porcentaje de: ", (total_ingreso(ruta_exp_imp)-ingreso_top10_rutas)*100/total_ingreso(ruta_exp_imp),"% \n")
    total_opcion1= ingreso_top10_rutas
    return total_opcion1

##################################################### OPCION 2   

def datos_por_transporte(lista,transporte):
    ruta_transp=[]
    for registro in lista:
        if registro[7]== transporte:
            ruta_transp.append(registro)
    
    return ruta_transp

def lista_transportes(lista=lista_datos):
    transportes=[]
    for linea in lista_datos[1:]:
        if linea[7] not in transportes:
            transportes.append(linea[7])
    
    return transportes

def total_por_transp(lista,lista_transp):
    lista_total=[]
    for transporte in lista_transp:
        lista_dat=datos_por_transporte(lista,transporte)
        total_transp=0
        for linea in lista_dat:
            total_transp+=int(linea[9])
        lista_total.append([transporte,total_transp])    
    
    return lista_total

def obtener_porcentaje(lista_ordenada):
    total=0
    for linea in lista_ordenada:
        total+=linea[1]
        
    for elem in lista_ordenada:
        porcentaje= elem[1]*100/total
        elem.append(porcentaje)
    return lista_ordenada

      
def opcion2(tipo):
    transportes = lista_transportes(extraer_info(tipo))
    total_opcion2= total_por_transp(extraer_info(tipo),transportes)
    total_opcion2.sort(reverse=True, key = lambda x:x[1])
    total_opcion2=obtener_porcentaje(total_opcion2)
    print("Estos son los ingresos por", tipo, "en orden")
    print("[Tipo, ingreso total, porcentaje]")
    for elementos in total_opcion2:
        print(elementos)
    return total_opcion2

    
##################################################### OPCION 3    


#Funcion que imprimiremos en el menu principal    
def opcion3(tipo): 
    
    #Extraemos la info de "Imports" o "Exports" ya que tiene el agregado del total por ruta
    exp_imp_por_valor=conteo_rutas(extraer_info(tipo))
    #Ordenamos por la variable de interes
    exp_imp_por_valor.sort(reverse=True, key = lambda x:x[3])
    
    #dato de referencia
    total=0
    for linea in exp_imp_por_valor:
        total+=linea[3]
    
    #Obtenemos el porcentaje que representa en el total de ingresos por cada ruta
    for linea in exp_imp_por_valor:
        porcentaje= (linea[3]/total)*100
        linea.append(porcentaje)
    
    top_rutas_valor=[]
    ochenta_porciento=0
    
    #Guardamos las rutas que representan el 80% de ingresos
    for linea in exp_imp_por_valor:
        top_rutas_valor.append(linea[0:4])
        ochenta_porciento+=linea[4]
        if ochenta_porciento > 80:
            break
        
    #Impresion del reporte    
    print("Se dejarian ", len(exp_imp_por_valor)-len(top_rutas_valor), "rutas")
    
    total_opcion3= 0
    for ruta in top_rutas_valor:
        total_opcion3  += ruta[3]
    
    print("El ingreso total generado si se opta por la opcion3 es de", total_opcion3)
    print("Lo que representa el ", (total_opcion3/total)*100,"%","de los ingresos totales\n")
        
    print("El ingreso que se abandonaria si se opta por la opcion3 es de", (total-total_opcion3))
    print("Lo que representa el ", ((total-total_opcion3)/total)*100,"%","de los ingresos totales")
    return total_opcion3




############################# MENU PRINCIPAL
flag=False

while flag==False:
    print("\nBienvenido al menu")
    print("¿Que desea hacer?")
    print("1. Ver reporte opcion 1 Rutas de importacion y exportacion")
    print("2. Ver reporte opcion 2 Medio de Transporte Utilizado")
    print("3. Ver reporte opcion 3 Valor total de importaciones y exportaciones")
    print("0. Salir")
    
    ingreso= input("Escriba su respuesta con numero: ")
    if ingreso== "1":
        print("¿Que desea hacer?")
        print("1. Ver por Exportaciones")
        print("2. Ver por Importaciones")
        op1= input("Escriba su respuesta con numero: ")
        if op1 == "1":
            print("\n")
            opcion1("Exports")
        elif op1=="2":
            print("\n")
            opcion1("Imports")
        else:
            print("\n")
            print("Opcion no registrada \n")
    elif ingreso== "2":
        print("¿Que desea hacer?")
        print("1. Ver por Exportaciones")
        print("2. Ver por Importaciones")
        op2= input("Escriba su respuesta con numero: \n")
        if op2 == "1":
            print("\n")
            opcion2("Exports")
        elif op2=="2":
            print("\n")
            opcion2("Imports")
        else:
            print("\n")
            print("Opcion no registrada \n")
    elif ingreso== "3":
        print("¿Que desea hacer?")
        print("1. Ver por Exportaciones")
        print("2. Ver por Importaciones")
        op3= input("Escriba su respuesta con numero: \n")
        if op3 == "1":
            print("\n")
            opcion3("Exports")
        elif op3=="2":
            print("\n")
            opcion3("Imports")
        else:
            print("\n")
            print("Opcion no registrada \n")
    elif ingreso== "0":
        print("¡Vuelva pronto! =)\n")    
        flag=True
    else:
        print("Intentelo NUEVAMENTE\n")
    
    
    
    
    
    
    
    
    
    
    
