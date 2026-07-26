#!/bin/bash

# ==========================================
# SuricTL Uninstaller
# ==========================================


# ========= COLORES =========

WHITE="\e[37m"
GREEN="\e[32m"
RED="\e[31m"
CYAN="\e[36m"
YELLOW="\e[33m"
BOLD="\e[1m"
RESET="\e[0m"


# ========= FUNCIONES =========

line() {
    printf "%b\n" "${CYAN}============================================================${RESET}"
}

title() {
    clear
    line
    printf "%b\n" "${BOLD}${WHITE}              DESINSTALADOR SURicTL${RESET}"
    line
    printf "\n"
}

ok() {
    printf "%b\n" "${GREEN}[OK]${RESET} $1"
}

info() {
    printf "%b\n" "${CYAN}[INFO]${RESET} $1"
}

warn() {
    printf "%b\n" "${YELLOW}[AVISO]${RESET} $1"
}

error() {
    printf "%b\n" "${RED}[ERROR]${RESET} $1"
}


# ========= CONFIGURACION =========

INSTALL_PATH="/usr/local/bin/surictl"


# ========= VALIDACION ROOT =========

title


if [[ $EUID -ne 0 ]]; then

    error "Este desinstalador necesita permisos root."

    echo ""
    echo "Ejecuta:"
    echo "sudo ./uninstall.sh"

    exit 1

fi


# ========= CONFIRMACION =========


warn "Esto eliminará únicamente SuricTL."

echo ""

echo "Se eliminará:"
echo "  $INSTALL_PATH"

echo ""

echo "No se eliminarán:"
echo "  /etc/suricata/"
echo "  /var/lib/suricata/"
echo "  /var/log/suricata/"

echo ""

read -rp "¿Continuar? [s/N]: " confirm


if [[ "$confirm" != "s" && "$confirm" != "S" ]]; then

    info "Operación cancelada."
    exit 0

fi



# ========= ELIMINACION =========


echo ""

info "Eliminando SuricTL..."


if [[ -f "$INSTALL_PATH" ]]; then

    rm -f "$INSTALL_PATH"

    if [[ $? -eq 0 ]]; then

        ok "SuricTL eliminado correctamente."

    else

        error "No se pudo eliminar SuricTL."
        exit 1

    fi

else

    warn "SuricTL no estaba instalado."

fi



# ========= VERIFICACION =========


echo ""

info "Verificando eliminación..."


if command -v surictl >/dev/null 2>&1; then

    error "SuricTL todavía aparece en el sistema."

else

    ok "SuricTL eliminado del PATH."

fi



echo ""

line

printf "%b\n" "${BOLD}${WHITE} Desinstalación completada ${RESET}"

line

echo ""
