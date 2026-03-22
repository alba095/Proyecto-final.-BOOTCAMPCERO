from flask import render_template, request
from app import app
from models.database import *
from services.apiservices import get_conversion

@app.route("/")
def home():
    
    moves = get_mov()
    return render_template("movimientos.html", moves = moves, pagina = "inicio")


@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    moneda_from = ""
    moneda_to = ""
    cantidad = ""
    cantidad_to = ""
    error = ""
    mensaje = ""

    if request.method == "POST":
        accion = request.form.get("accion")
        moneda_from = request.form.get("moneda_from")
        moneda_to = request.form.get("moneda_to")
        cantidad = request.form.get("cantidad")
        cantidad_to = request.form.get("cantidad_to")

        if moneda_from == "" or moneda_to == "" or cantidad == "":
            error = "Hay que rellenar todos los campos"
            return render_template("compra_venta.html",pagina = "compra", error=error, moneda_from=moneda_from, moneda_to=moneda_to, cantidad=cantidad, cantidad_to=cantidad_to)

        try:
            cantidad = float(cantidad)
        except:
            error = "Introduce un número"
            return render_template("compra_venta.html",pagina = "compra", error=error, moneda_from=moneda_from, moneda_to=moneda_to, cantidad=request.form.get("cantidad"), cantidad_to=cantidad_to)

        if moneda_from == moneda_to:
            error = "Las monedas no pueden ser iguales"
            return render_template("compra_venta.html",pagina = "compra", error=error, moneda_from=moneda_from, moneda_to=moneda_to, cantidad=cantidad, cantidad_to=cantidad_to)

        elif cantidad <= 0:
            error = "La cantidad debe ser mayor que 0"
            return render_template("compra_venta.html",pagina = "compra", error=error, moneda_from=moneda_from, moneda_to=moneda_to, cantidad=cantidad, cantidad_to=cantidad_to)

        else:
            if accion == "calcular":
                cantidad_to = get_conversion(moneda_from, moneda_to, cantidad)
                return render_template("compra_venta.html",pagina = "compra", moneda_from=moneda_from, moneda_to=moneda_to, cantidad=cantidad, cantidad_to=cantidad_to)

            elif accion == "aceptar":
                if cantidad_to == "":
                    error = "Primero tienes que calcular la conversión"
                    return render_template("compra_venta.html",pagina = "compra", error=error, moneda_from=moneda_from, moneda_to=moneda_to, cantidad=cantidad, cantidad_to=cantidad_to)

                cantidad_to = float(cantidad_to)

                if moneda_from != "EUR":
                    saldo = get_saldo(moneda_from)
                    if saldo < cantidad:
                        error = "El saldo es insuficiente"
                        return render_template("compra_venta.html",pagina = "compra", error=error, moneda_from=moneda_from, moneda_to=moneda_to, cantidad=cantidad, cantidad_to=cantidad_to)

                add_mov(moneda_from, cantidad, moneda_to, cantidad_to)
                mensaje = "Movimiento enviado con éxito"
                return render_template("compra_venta.html",pagina = "compra", mensaje=mensaje, moneda_from="", moneda_to="", cantidad="", cantidad_to="")

    else:
        return render_template("compra_venta.html",pagina = "compra", moneda_from=moneda_from, moneda_to=moneda_to, cantidad=cantidad, cantidad_to=cantidad_to, error=error, mensaje=mensaje)



@app.route("/status")
def status():
    movimientos = get_mov()
    invertido = 0

    for mov in movimientos:
            if mov[3] == "EUR":
                invertido += mov[4]
 
    recuperado = 0
    for mov in movimientos:
        if mov[5] == "EUR":
            recuperado += mov[6]

    valor_compra = invertido - recuperado
    saldos = {}

    for mov in movimientos:
        moneda_from = mov[3]
        cantidad_from = mov[4]
        moneda_to = mov[5]
        cantidad_to = mov[6]

        # restar lo que sale
        if moneda_from != "EUR":
            if moneda_from not in saldos:
                saldos[moneda_from] = 0
            saldos[moneda_from] -= cantidad_from

        # sumar lo que entra
        if moneda_to != "EUR":
            if moneda_to not in saldos:
                saldos[moneda_to] = 0
            saldos[moneda_to] += cantidad_to
        
    valor_actual = 0
    for moneda, saldo in saldos.items():
        if saldo > 0:
            valor_actual += get_conversion(moneda, "EUR", saldo)

    invertido = round(invertido, 2)
    recuperado = round(recuperado, 2)
    valor_compra = round(valor_compra, 2)
    valor_actual = round(valor_actual, 2)

    beneficio = round(valor_actual - valor_compra, 2)
    
    return render_template("estado.html",pagina = "status", invertido=invertido, recuperado = recuperado, valor_compra = valor_compra, valor_actual = valor_actual, beneficio = beneficio)
