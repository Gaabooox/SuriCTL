#!/usr/bin/env python3

import json
import sys
from datetime import datetime


OUTPUT_FILE = "analisis_comportamiento.json"


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



def convertir_fecha(fecha):

    return datetime.strptime(
        fecha,
        "%Y-%m-%dT%H:%M:%S.%f%z"
    )



# ==========================
# IDENTIFICACION
# ==========================

def identificar_servicio(nombre):

    nombre = nombre.lower()


    if "ssh" in nombre:
        return "SSH"


    if "ftp" in nombre:
        return "FTP"


    if "http" in nombre:
        return "HTTP"


    if "scan" in nombre:
        return "SCAN"


    return "DESCONOCIDO"



# ==========================
# INDICADORES
# ==========================

def calcular_indicadores(
        total,
        duracion,
        servicios
):

    velocidad = 0


    if duracion > 0:

        velocidad = round(
            total / duracion,
            2
        )


    return {

        "cantidad_eventos":
            total,


        "velocidad_eventos_segundo":
            velocidad,


        "multiples_servicios":
            len(servicios) > 1,


        "actividad_rapida":
            duracion < 60 and total >= 5,


        "alta_frecuencia":
            total >= 20

    }



# ==========================
# RIESGO
# ==========================

def calcular_riesgo(
        total,
        servicios,
        indicadores,
        ataques
):

    puntos = 0



    # volumen

    if total >= 20:
        puntos += 4

    elif total >= 10:
        puntos += 2



    # servicios

    if len(servicios) >= 3:
        puntos += 4

    elif len(servicios) >= 2:
        puntos += 2



    nombres = " ".join(
        ataques
    ).lower()



    if "fuerza bruta" in nombres:
        puntos += 4



    if "scan" in nombres:
        puntos += 3



    if indicadores["actividad_rapida"]:
        puntos += 2



    if indicadores["alta_frecuencia"]:
        puntos += 3



    if puntos >= 10:
        return "CRITICO"


    elif puntos >= 6:
        return "ALTO"


    elif puntos >= 3:
        return "MEDIO"


    return "BAJO"



# ==========================
# PATRONES
# ==========================

def detectar_patrones(
        servicios,
        ataques,
        indicadores
):

    patrones = []



    nombres = " ".join(
        ataques
    ).lower()



    if "ssh" in servicios:

        patrones.append(
            "Intentos contra servicio SSH detectados"
        )



    if "ftp" in servicios:

        patrones.append(
            "Intentos contra servicio FTP detectados"
        )



    if "scan" in servicios:

        patrones.append(
            "Posible reconocimiento de red"
        )



    if indicadores["alta_frecuencia"]:

        patrones.append(
            "Alta frecuencia de eventos"
        )



    if indicadores["multiples_servicios"]:

        patrones.append(
            "Actividad contra múltiples servicios"
        )



    if indicadores["actividad_rapida"]:

        patrones.append(
            "Posible comportamiento automatizado"
        )



    if not patrones:

        patrones.append(
            "Actividad sospechosa detectada"
        )


    return patrones



# ==========================
# RECOMENDACIONES
# ==========================

def recomendaciones(riesgo):


    acciones = {


        "CRITICO": [

            "Bloquear IP origen",
            "Revisar autenticaciones",
            "Aplicar reglas firewall",
            "Realizar investigación forense"

        ],


        "ALTO": [

            "Monitorear IP",
            "Revisar logs asociados",
            "Considerar bloqueo"

        ],


        "MEDIO": [

            "Continuar monitoreo",
            "Revisar comportamiento"

        ],


        "BAJO": [

            "Mantener monitoreo activo"

        ]

    }


    return acciones.get(
        riesgo,
        []
    )



# ==========================
# ANALIZADOR
# ==========================

def analizar(data):

    resultado = {}



    for ip, info in data.items():


        inicio = convertir_fecha(
            info["primer_evento"]
        )


        fin = convertir_fecha(
            info["ultimo_evento"]
        )


        duracion = int(
            (fin - inicio).total_seconds()
        )



        total = info.get(
            "total_eventos",
            0
        )



        servicios = []

        protocolos = []



        for nombre, ataque in info["ataques"].items():


            servicio = identificar_servicio(
                nombre
            )


            servicios.append(
                servicio
            )


            protocolos.extend(
                ataque.get(
                    "protocolos",
                    []
                )
            )



        servicios = list(
            set(servicios)
        )


        protocolos = list(
            set(protocolos)
        )



        indicadores = calcular_indicadores(
            total,
            duracion,
            servicios
        )



        riesgo = calcular_riesgo(
            total,
            servicios,
            indicadores,
            info["ataques"].keys()
        )



        resultado[ip] = {


            "ip_origen": ip,


            "periodo_actividad": {

                "inicio":
                    info["primer_evento"],


                "fin":
                    info["ultimo_evento"],


                "duracion_segundos":
                    duracion

            },



            "estadisticas": {

                "total_eventos":
                    total

            },



            "ataques_detectados":
                info["ataques"],



            "servicios_detectados":
                servicios,



            "protocolos":
                protocolos,



            "indicadores":
                indicadores,



            "nivel_riesgo":
                riesgo,



            "patrones":
                detectar_patrones(
                    servicios,
                    info["ataques"].keys(),
                    indicadores
                ),



            "recomendaciones":
                recomendaciones(
                    riesgo
                )

        }



    return resultado



# ==========================
# MAIN
# ==========================

def main():


    if len(sys.argv) < 2:

        print(
            "Uso: python3 analyzer.py alertas_resumen.json"
        )

        sys.exit(1)



    archivo = sys.argv[1]


    print(
        "[INFO] Leyendo resumen de alertas..."
    )


    data = cargar_json(
        archivo
    )


    print(
        "[INFO] Analizando comportamiento..."
    )


    resultado = analizar(
        data
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