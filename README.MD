# Proyecto Flask Criptomonedas

Aplicación web desarrollada con Flask que permite gestionar una cartera de criptomonedas.  
El usuario puede comprar, vender y consultar el estado actual de su inversión.

---

## Funcionalidades

- Visualización de movimientos realizados
- Compra y venta de criptomonedas
- Conversión de monedas mediante API
- Control de saldo (no permite vender más de lo disponible)
- Cálculo del estado de la inversión:
  - Invertido
  - Recuperado
  - Valor de compra
  - Valor actual
  - Beneficio o pérdida

---

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML + Jinja2
- Pico.css

---
## Arquitectura (MVC)

El proyecto sigue el patrón MVC (Modelo-Vista-Controlador):

- **Modelo (Model):** Base de datos SQLite (`movements.db`) y funciones de acceso a datos como `get_mov`, `add_mov` o `get_saldo`.
- **Vista (View):** Templates HTML con Jinja (`movimientos.html`, `compra_venta.html`, `estado.html`).
- **Controlador (Controller):** Rutas definidas en Flask (`app.py`) que gestionan la lógica de la aplicación.

Aunque parte de la lógica se encuentra en el controlador, esto es habitual en aplicaciones Flask sencillas.

## Instalación

1. Clonar el repositorio:

```bash
git clone <https://github.com/alba095/Proyecto-final.-BOOTCAMPCERO.git>
cd <PROYECTO_FINAL>

