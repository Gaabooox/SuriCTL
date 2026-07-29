#!/usr/bin/env python3

import json
import sys
from datetime import datetime


OUTPUT_FILE = "reporte_incidentes.json"


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



def fecha_actual():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



# ==========================
# GENERADOR DE REPORTE
# ==========================

def generar_reporte(
        analisis,
        amenazas
):

    reporte = []


    for ip, datos in amenazas.items():


        comportamiento = analisis.get(
            ip,
            {}
        )


        incidente = {


            "fecha_reporte":
                fecha_actual(),


            "ip_origen":
                ip,


            "riesgo":

                datos.get(
                    "nivel_riesgo_actual",
                    "DESCONOCIDO"
                ),



            "resumen":

                "",



            "periodo":

                comportamiento.get(
                    "periodo_actividad",
                    {}
                ),



            "estadisticas":

                comportamiento.get(
                    "estadisticas",
                    {}
                ),



            "servicios_afectados":

                comportamiento.get(
                    "servicios_detectados",
                    []
                ),



            "patrones":

                comportamiento.get(
                    "patrones",
                    []
                ),



            "amenazas":

                datos.get(
                    "amenazas_detectadas",
                    []
                ),



            "recomendaciones":

                comportamiento.get(
                    "recomendaciones",
                    [])

        }



        cantidad = datos.get(
            "cantidad_amenazas",
            0
        )


        if cantidad > 0:


            incidente["resumen"] = (
                f"La IP {ip} presenta "
                f"{cantidad} comportamiento(s) "
                "clasificado(s) como amenaza."
            )


        else:


            incidente["resumen"] = (
                f"La IP {ip} generó actividad "
                "sospechosa sin amenazas críticas detectadas."
            )



        reporte.append(
            incidente
        )


    return reporte



# ==========================
# MAIN
# ==========================

def main():


    if len(sys.argv) < 3:

        print(
            "Uso:"
        )

        print(
            "python3 reporter.py analisis_comportamiento.json amenazas_detectadas.json"
        )

        sys.exit(1)



    archivo_analisis = sys.argv[1]

    archivo_amenazas = sys.argv[2]



    print(
        "[INFO] Cargando análisis..."
    )


    analisis = cargar_json(
        archivo_analisis
    )



    print(
        "[INFO] Cargando amenazas..."
    )


    amenazas = cargar_json(
        archivo_amenazas
    )



    print(
        "[INFO] Generando reporte..."
    )


    reporte = generar_reporte(
        analisis,
        amenazas
    )



    guardar_json(
        reporte,
        OUTPUT_FILE
    )


    print(
        "[OK] Generado:",
        OUTPUT_FILE
    )



if __name__ == "__main__":

    main()