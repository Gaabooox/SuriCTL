#!/usr/bin/env python3
# noqa: EXE001
import argparse
import json
from collections import defaultdict
from datetime import datetime


def cargar_logs(ruta):

    eventos = []

    try:
        with open(ruta, "r") as archivo:

            for linea in archivo:

                try:
                    data = json.loads(linea)

                    if data.get("event_type") == "alert":
                        eventos.append(data)

                except json.JSONDecodeError:
                    continue

    except FileNotFoundError:
        print("[ERROR] No existe el archivo eve.json")
        exit(1)

    return eventos



def obtener_hora(timestamp):

    try:
        fecha = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

        return fecha.strftime("%H:00")

    except Exception:
        return "desconocido"

def limpiar_alerta(evento):

    alerta = evento.get("alert", {})

    return {
        "timestamp": evento.get("timestamp"),
        "firma": alerta.get("signature"),
        "sid": alerta.get("signature_id"),
        "severidad": alerta.get("severity"),
        "origen": evento.get("src_ip"),
        "destino": evento.get("dest_ip"),
        "protocolo": evento.get("proto"),
        "puerto_destino": evento.get("dest_port")
    }



def generar_alertas_clean(eventos):

    limpias = []

    for evento in eventos:
        limpias.append(
            limpiar_alerta(evento)
        )

    return limpias



def guardar_json_simple(datos, salida):

    with open(
        salida,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )

def procesar_alertas(eventos):

    resumen = defaultdict(
        lambda: {
            "total_eventos": 0,
            "primer_evento": None,
            "ultimo_evento": None,
            "ataques": defaultdict(
                lambda: {
                    "cantidad": 0,
                    "horas": defaultdict(int),
                    "destinos": set(),
                    "protocolos": set()
                }
            )
        }
    )


    for evento in eventos:

        ip_origen = evento.get(
            "src_ip",
            "desconocida"
        )


        ip_destino = evento.get(
            "dest_ip",
            "desconocida"
        )


        protocolo = evento.get(
            "proto",
            "desconocido"
        )


        timestamp = evento.get(
            "timestamp",
            ""
        )


        firma = evento.get(
            "alert",
            {}
        ).get(
            "signature",
            "Sin firma"
        )


        hora = obtener_hora(timestamp)


        atacante = resumen[ip_origen]


        atacante["total_eventos"] += 1


        if atacante["primer_evento"] is None:
            atacante["primer_evento"] = timestamp


        atacante["ultimo_evento"] = timestamp



        ataque = atacante["ataques"][firma]


        ataque["cantidad"] += 1

        ataque["horas"][hora] += 1

        ataque["destinos"].add(ip_destino)

        ataque["protocolos"].add(protocolo)



    return resumen



def convertir_sets(data):

    if isinstance(data, defaultdict):
        data = dict(data)


    if isinstance(data, dict):

        for clave, valor in data.items():
            data[clave] = convertir_sets(valor)


    elif isinstance(data, set):

        return list(data)


    return data



def guardar_json(datos, salida):

    datos = convertir_sets(datos)

    with open(
        salida,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )



def main():

    parser = argparse.ArgumentParser(
        description="Parser inteligente de alertas Suricata"
    )


    parser.add_argument(
        "-i",
        "--input",
        default="/var/log/suricata/eve.json",
        help="Archivo eve.json"
    )


    parser.add_argument(
        "-o",
        "--output",
        default="alertas_resumen.json",
        help="JSON generado"
    )


    args = parser.parse_args()



    print("[INFO] Leyendo eventos...")


    eventos = cargar_logs(args.input)


    print(
        f"[INFO] Alertas encontradas: {len(eventos)}"
    )


    print("[INFO] Generando alertas limpias...")


    alertas_clean = generar_alertas_clean(eventos)


    guardar_json_simple(
        alertas_clean,
        "alertas_clean.json"
    )


    print("[OK] Generado: alertas_clean.json")



    print("[INFO] Generando resumen inteligente...")


    resumen = procesar_alertas(eventos)


    guardar_json(
        resumen,
        "alertas_resumen.json"
    )


    print("[OK] Generado: alertas_resumen.json")



if __name__ == "__main__":
    main()
