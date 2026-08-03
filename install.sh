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

DISTRO=""
PKG_MANAGER=""
INSTALL_CMD=""


# ========= DETECCION DE SISTEMA =========

# Detecta la distro (Debian, Arch, Fedora y sus derivados)
# y elige el gestor de paquetes correcto.
detectar_distro() {
    local distro_id=""
    local like=""

    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        distro_id="${ID:-}"
        like="${ID_LIKE:-}"
    fi

    case "$distro_id" in
        debian|ubuntu|linuxmint|kali|pop|elementary|zorin)
            DISTRO="Debian (o derivado)"
            PKG_MANAGER="apt"
            INSTALL_CMD="apt install -y"
            ;;
        arch|manjaro|endeavouros|cachyos|garuda)
            DISTRO="Arch (o derivado)"
            PKG_MANAGER="pacman"
            INSTALL_CMD="pacman -S --noconfirm"
            ;;
        fedora|centos|rhel|rocky|almalinux)
            DISTRO="Fedora (o derivado)"
            PKG_MANAGER="dnf"
            INSTALL_CMD="dnf install -y"
            ;;
        *)
            case "$like" in
                *debian*)
                    DISTRO="Debian (o derivado)"
                    PKG_MANAGER="apt"
                    INSTALL_CMD="apt install -y"
                    ;;
                *arch*)
                    DISTRO="Arch (o derivado)"
                    PKG_MANAGER="pacman"
                    INSTALL_CMD="pacman -S --noconfirm"
                    ;;
                *fedora*|*rhel*)
                    DISTRO="Fedora (o derivado)"
                    PKG_MANAGER="dnf"
                    INSTALL_CMD="dnf install -y"
                    ;;
                *)
                    return 1
                    ;;
            esac
            ;;
    esac
}

# Instala un paquete con el gestor detectado.
instalar() {
    local pkg="$1"
    info "Instalando $pkg con $PKG_MANAGER..."

    # shellcheck disable=SC2086
    if $INSTALL_CMD "$pkg"; then
        ok "$pkg instalado correctamente."
        return 0
    fi

    error "No se pudo instalar $pkg."
    echo ""
    warn "Inténtalo manualmente:"
    echo ""
    printf "%b\n" "${GREEN}sudo $INSTALL_CMD $pkg${RESET}"
    return 1
}


# ========= VALIDACIONES =========

title


if [[ $EUID -ne 0 ]]; then
    error "Este instalador necesita permisos root."
    echo "Ejecuta:"
    echo "sudo ./install.sh"
    exit 1
fi


if ! detectar_distro; then
    error "No se pudo detectar una distro soportada."
    echo ""
    echo "SuricTL soporta: Debian (apt), Arch (pacman) y Fedora (dnf)."
    echo "En tu distro, instala manualmente 'suricata' y 'jq', y vuelve a ejecutar este instalador."
    exit 1
fi

info "Sistema detectado: $DISTRO"
ok "Gestor de paquetes: $PKG_MANAGER"
echo ""


# ========= DEPENDENCIAS =========


info "Comprobando Suricata..."

if command -v suricata >/dev/null 2>&1; then

    ok "Suricata encontrado."

else

    error "Suricata no está instalado."
    echo ""
    warn "Instalando Suricata automáticamente con $PKG_MANAGER..."
    echo ""

    if ! instalar "suricata"; then
        exit 1
    fi

fi



info "Comprobando jq..."


if command -v jq >/dev/null 2>&1; then

    ok "jq encontrado."

else

    warn "jq no encontrado."

    if ! instalar "jq"; then
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
