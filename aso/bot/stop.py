#!/usr/bin/python3
import os
import sys
import subprocess


# Nombre del servicio de Apache2
nom_servicio=sys.argv[1]

    # Iniciar el servicio Apache2
rc = subprocess.getstatusoutput(f' systemctl stop {nom_servicio} ')
if rc[0] == 0:
    print(rc[1])
    print (" * Parando servicio " + nom_servicio)
    # Inicia el servicio utilizando cysystemd
    #os.system (f"systemctl start {nom_servicio}")
    #os.system(f'systemctl enable {nom_servicio}')
else:
    print("No se ha encontrado el servicio")
