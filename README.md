# 🛡️ SuricTL

**SuricTL** es una herramienta de administración para **Suricata IDS/IPS** desarrollada completamente en **Bash**.

Su objetivo es simplificar la administración de Suricata desde una interfaz interactiva en la terminal, permitiendo gestionar el servicio, las reglas, los logs, las alertas y la configuración sin editar manualmente múltiples archivos del sistema.

---

## 📌 Características

- Estado del servicio Suricata.
- Iniciar, detener y reiniciar Suricata.
- Validación de la configuración.
- Administración de reglas locales.
- Validación de reglas antes de aplicarlas.
- Edición de `local.rules`.
- Configuración de `suricata.yaml`.
- Cambio de interfaz de captura.
- Configuración de `HOME_NET`.
- Visualización de logs.
- Consulta de eventos en tiempo real.
- Gestión y filtrado de alertas.
- Exportación de alertas.
- Dashboard con información general del sistema.

---

# 📷 Capturas

## Dashboard

> Próximamente

---

## Estado

> Próximamente

---

## Reglas

> Próximamente

---

## Logs

> Próximamente

---

## Alertas

> Próximamente

---

## Configuración

> Próximamente

---

# 📂 Estructura

```
surictl/
├── surictl
├── install.sh
├── uninstall.sh
├── README.md
├── LICENSE
└── screenshots/
```

---

# ⚙️ Requisitos

- Linux: **Debian**, **Arch** o **Fedora** (y sus derivados)
- Bash
- Suricata
- jq
- systemd

> El instalador detecta tu distribución automáticamente y usa el gestor de
> paquetes correcto para instalar las dependencias faltantes.

---

# 🚀 Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Gaabooox/SuriCTL.git

cd SuriCTL
```

Dar permisos:

```bash
chmod +x install.sh
```

Instalar:

```bash
sudo ./install.sh
```

El instalador detecta el sistema automáticamente:

| Distribución | Gestor de paquetes |
|--------------|-------------------|
| Debian, Ubuntu, Mint, Kali | `apt` |
| Arch, Manjaro, CachyOS | `pacman` |
| Fedora, CentOS, Rocky | `dnf` |

Si Suricata o `jq` no están instalados, los instala por ti. En distros no
soportadas, te indica los comandos manuales.

---

# ▶️ Uso

Una vez instalado únicamente ejecutar:

```bash
surictl
```

---

# 📋 Menús disponibles

## Status

Permite administrar el servicio Suricata.

- Ver estado
- Iniciar
- Detener
- Reiniciar
- Validar configuración

---

## Reglas

Administración completa de reglas locales.

- Ver reglas
- Agregar reglas
- Eliminar reglas
- Editar reglas
- Validar reglas

---

## Logs

Consulta de los registros generados por Suricata.

- eve.json
- fast.log
- stats.log
- Eventos en vivo
- Búsqueda por IP

---

## Alertas

Visualización y análisis de alertas.

- Últimas alertas
- Buscar alerta
- Filtrar por IP
- Filtrar por severidad
- Estadísticas
- Exportación

---

## Configuración

Administración de la configuración principal.

- Cambiar interfaz
- Editar suricata.yaml
- Ver configuración
- Validar configuración
- Configurar HOME_NET

---

# 📁 Archivos utilizados

| Archivo | Descripción |
|----------|-------------|
| `/etc/suricata/suricata.yaml` | Configuración principal |
| `/var/lib/suricata/rules/local.rules` | Reglas locales |
| `/var/log/suricata/eve.json` | Eventos completos |
| `/var/log/suricata/fast.log` | Alertas resumidas |
| `/var/log/suricata/stats.log` | Estadísticas |

---

# 🛠 Tecnologías

- Bash
- Suricata
- jq
- systemd
- grep
- awk
- sed
- less

---

# 🎯 Objetivos del proyecto

- Facilitar la administración de Suricata.
- Centralizar las tareas más comunes en una sola herramienta.
- Evitar la edición manual de múltiples archivos.
- Servir como proyecto de aprendizaje en Bash y Blue Team.
- Evolucionar hacia una herramienta de administración completa para Suricata.

---

# 📈 Roadmap

## v1.0

- [x] Dashboard
- [x] Gestión del servicio
- [x] Gestión de reglas
- [x] Gestión de logs
- [x] Gestión de alertas
- [x] Gestión de configuración

## Próximas versiones

- [ ] Reportes automáticos
- [ ] Estadísticas avanzadas
- [ ] Detección de ataques comunes
- [ ] Integración con IA para explicación de alertas
- [ ] Soporte IPS
- [ ] Exportación de reportes PDF

---

# 🤝 Contribuciones

Las contribuciones son bienvenidas.

Si encuentras un error o tienes una sugerencia, puedes abrir un **Issue** o enviar un **Pull Request**.

---

# 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

---

# 👤 Autor

**Gabriel**

Proyecto desarrollado como parte de mi portafolio de Ciberseguridad y Blue Team utilizando Suricata IDS.
