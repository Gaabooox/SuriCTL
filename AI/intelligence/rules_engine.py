#!/usr/bin/env python3

import json
import sys


OUTPUT_FILE = "amenazas_detectadas.json"


# ==========================
# UTILIDADES
# ==========================

def cargar_json(path):

    with open(path, "r") as file:
        return json.load(file)



def guardar_json(data, path):

    with open(path, "w") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )



# ==========================
# MOTOR DE REGLAS
# ==========================


def detectar_fuerza_bruta(datos):


    indicadores = datos["indicadores"]

    servicios = datos["servicios_detectados"]


    if (

        "SSH" in servicios

        and

        indicadores["cantidad_eventos"] >= 5

    ):

        return {

            "tipo":
                "SSH_BRUTE_FORCE",

            "categoria":
                "Fuerza bruta",

            "severidad":
                "ALTO",

            "descripcion":
                "Múltiples intentos contra servicio SSH"

        }


    return None



def detectar_reconocimiento(datos):


    servicios = datos["servicios_detectados"]


    if len(servicios) >= 3:


        return {


            "tipo":
                "NETWORK_RECON",


            "categoria":
                "Reconocimiento",


            "severidad":
                "CRITICO",


            "descripcion":
                "La misma IP interactuó con múltiples servicios"

        }


    return None



def detectar_scan(datos):


    servicios = datos["servicios_detectados"]


    indicadores = datos["indicadores"]



    if (

        "SCAN" in servicios

        or

        indicadores["alta_frecuencia"]

    ):


        return {


            "tipo":
                "PORT_SCAN",


            "categoria":
                "Escaneo",


            "severidad":
                "MEDIO",


            "descripcion":
                "Posible escaneo automatizado"

        }


    return None



def detectar_automatizacion(datos):


    indicadores = datos["indicadores"]



    if indicadores["actividad_rapida"]:


        return {


            "tipo":
                "AUTOMATED_ACTIVITY",


            "categoria":
                "Automatización",


            "severidad":
                "MEDIO",


            "descripcion":
                "Patrón compatible con herramienta automática"

        }


    return None



# ==========================
# ANALISIS PRINCIPAL
# ==========================


def analizar_ip(ip, datos):


    amenazas = []


    reglas = [

        detectar_fuerza_bruta,

        detectar_reconocimiento,

        detectar_scan,

        detectar_automatizacion

    ]



    for regla in reglas:


        resultado = regla(datos)


        if resultado:

            amenazas.append(
                resultado
            )



    return {


        "ip_origen":
            ip,


        "nivel_riesgo_actual":
            datos["nivel_riesgo"],


        "amenazas_detectadas":
            amenazas,


        "cantidad_amenazas":
            len(amenazas)

    }



def ejecutar_motor(data):


    resultado = {}


    for ip, datos in data.items():


        resultado[ip] = analizar_ip(
            ip,
            datos
        )


    return resultado



# ==========================
# MAIN
# ==========================


def main():


    if len(sys.argv) < 2:

        print(
            "Uso: python3 rules_engine.py analisis_comportamiento.json"
        )

        sys.exit(1)



    archivo = sys.argv[1]


    print(
        "[INFO] Cargando análisis..."
    )


    datos = cargar_json(
        archivo
    )


    print(
        "[INFO] Ejecutando reglas de inteligencia..."
    )


    resultado = ejecutar_motor(
        datos
    )


    guardar_json(
        resultado,
        OUTPUT_FILE
    )


    print(
        "[OK] Generado:",
        OUTPUT_FILE
    )



if __name__ == "__main__":
    main()