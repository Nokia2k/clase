#!/usr/bin/python3

import sys
import os

gente = ["Adrian", "Lautaro", "David", "Jesus", "Victor", "Jose"]

path = os.path.expanduser('~')
path = str(path)+"/investigacion"
if os.path.exists(path):
    ask = input ("Quieres borrar la carpeta investigacion? ")
    if ask == "si":
        try:
            os.rmdir(path)
            print ("Carpeta borrada")
        except:
            print ("algo ha ido mal...")
            sys.exit(1)
    elif ask == "no":
        print ("Pues no se borra la carpeta")
        sys.exit(0)
    else:
        print ("* ERROR: Opcion invalida")
        print ("* Unicas opciones disponibles: si - no")

else:
    
    os.mkdir(path)
    print ("Carpeta investigacion creada")
    os.mkdir(str(path)+"/sospechosos")
    os.mkdir(str(path)+"/investigados")
    print ("Carpertas sospechosos y investigados creados")
    for crear in gente:
        os.open(str(path)+"/sospechosos/"+crear+".tkn",'x')
    
