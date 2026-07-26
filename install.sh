#!/bin/bash

# ==========================================
# SuricTL Installer
# ==========================================

# ========= COLORES =========

WHITE="\e[37m"
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
CYAN="\e[36m"
BOLD="\e[1m"
RESET="\e[0m"


# ========= FUNCIONES =========

line() {
    printf "%b\n" "${CYAN}============================================================${RESET}"
}

title() {
    clear
    line
    printf "%b\n" "${BOLD}${WHITE}                 INSTALADOR SURicTL${RESET}"
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
CURRENT_DIR="$(pwd)"
SOURCE_FILE="$CURRENT_DIR/surictl"


# ========= VALIDACIONES =========

title


if [[ $EUID -ne 0 ]]; then
    error "Este instalador necesita permisos root."
    echo "Ejecuta:"
    echo "sudo ./install.sh"
    exit 1
fi


info "Comprobando sistema..."


if [[ ! -f /etc/fedora-release ]]; then
    warn "Sistema diferente a Fedora detectado."
    warn "El instalador fue diseñado principalmente para Fedora."
fi


# ========= DEPENDENCIAS =========


info "Comprobando Suricata..."

if command -v suricata >/dev/null 2>&1; then

    ok "Suricata encontrado."

else

    error "Suricata no está instalado."
    echo ""
    echo "Instálalo con:"
    echo ""
    echo "sudo dnf install suricata"
    exit 1

fi



info "Comprobando jq..."


if command -v jq >/dev/null 2>&1; then

    ok "jq encontrado."

else

    warn "jq no encontrado."
    info "Instalando jq..."

    dnf install -y jq

    if command -v jq >/dev/null 2>&1; then
        ok "jq instalado correctamente."
    else
        error "No se pudo instalar jq."
        exit 1
    fi

fi



# ========= INSTALACION =========


info "Comprobando archivo surictl..."


if [[ ! -f "$SOURCE_FILE" ]]; then

    error "No se encontró el archivo surictl."

    echo ""
    echo "Ejecuta este instalador dentro de la carpeta del proyecto."

    exit 1

fi



info "Copiando SuricTL..."


cp "$SOURCE_FILE" "$INSTALL_PATH"


if [[ $? -eq 0 ]]; then

    ok "Archivo copiado."

else

    error "No se pudo copiar SuricTL."
    exit 1

fi



info "Asignando permisos..."


chmod +x "$INSTALL_PATH"


if [[ $? -eq 0 ]]; then

    ok "Permisos configurados."

else

    error "No se pudieron asignar permisos."
    exit 1

fi



# ========= VERIFICACION =========


echo ""

info "Verificando instalación..."


if command -v surictl >/dev/null 2>&1; then

    ok "SuricTL instalado correctamente."

else

    error "SuricTL no aparece en PATH."
    exit 1

fi



echo ""

line

printf "%b\n" "${BOLD}${WHITE} Instalación completada ${RESET}"

line

echo ""

echo "Ejecuta:"
echo ""

printf "%b\n" "${GREEN}surictl${RESET}"

echo ""
