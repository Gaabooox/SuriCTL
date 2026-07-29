#!/usr/bin/env python3

import subprocess
import sys
import os


# ==========================
# RUTAS
# ==========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


PARSER = os.path.join(
    BASE_DIR,
    "parser",
    "eve-parser.py"
)


ANALYZER = os.path.join(
    BASE_DIR,
    "analyzer",
    "analyzer.py"
)


RULE_ENGINE = os.path.join(
    BASE_DIR,
    "intelligence",
    "rules_engine.py"
)


REPORTER = os.path.join(
    BASE_DIR,
    "reporter",
    "reporter.py"
)


ALERTAS_RESUMEN = os.path.join(
    BASE_DIR,
    "parser",
    "alertas_resumen.json"
)


ANALISIS = os.path.join(
    BASE_DIR,
    "analyzer",
    "analisis_comportamiento.json"
)


AMENAZAS = os.path.join(
    BASE_DIR,
    "intelligence",
    "amenazas_detectadas.json"
)


# ==========================
# COLORES
# ==========================

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"



# ==========================
# EJECUTOR
# ==========================

def ejecutar(nombre, comando):

    print()
    print(
        f"{CYAN}[+] {nombre}{RESET}"
    )


    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )


    if resultado.returncode != 0:

        print(
            f"{RED}[ERROR] Falló: {nombre}{RESET}"
        )

        print(
            resultado.stderr
        )

        sys.exit(1)


    print(
        f"{GREEN}[OK] {nombre} completado{RESET}"
    )



# ==========================
# MAIN
# ==========================

def main():

    print()
    print(
        "==============================="
    )
    print(
        "      SuriCTL AI Pipeline"
    )
    print(
        "==============================="
    )


    ejecutar(

        "Procesando eve.json",

        [
            "python3",
            PARSER
        ]

    )


    ejecutar(

        "Analizando comportamiento",

        [
            "python3",
            ANALYZER,
            ALERTAS_RESUMEN
        ]

    )


    ejecutar(

        "Evaluando amenazas",

        [
            "python3",
            RULE_ENGINE,
            ANALISIS
        ]

    )


    ejecutar(

        "Generando reporte",

        [
            "python3",
            REPORTER,
            ANALISIS,
            AMENAZAS
        ]

    )


    print()

    print(
        f"{GREEN}[FINALIZADO] Análisis completo{RESET}"
    )

    print()


if __name__ == "__main__":
    main()