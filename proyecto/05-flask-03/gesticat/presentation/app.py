"""
Presentación/app: Interfaz web con Flask.

Segunda capa de presentación del proyecto. Expone todas las operaciones
del dominio como routes HTTP. El menú de consola (menu.py) sigue funcionando
sin cambios — ambas interfaces comparten el mismo ServicioColonia.
"""
import logging

from flask import Flask, redirect, url_for, request, render_template

from gesticat.infrastructure.datos_iniciales import crear_servicio_sqlite
from gesticat.infrastructure.errores import GatoNoEncontradoError, GatoYaExisteError
from gesticat.domain.gato import Sexo, EstadoGato
from gesticat.domain.colonia import EstadoColonia
from gesticat.domain.responsable import PersonaFisica, Protectora

app = Flask(__name__)

logging.basicConfig(
    filename='gesticat.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

servicio = crear_servicio_sqlite()

@app.before_request
def log_peticion():
    app.logger.info(f"{request.method} {request.path}")


# -- BIENVENIDA --

@app.route("/")
def inicio():
    return render_template("inicio.html")


# -- GATOS: LECTURA --

@app.route("/gatos/sin-esterilizar")
def listar_sin_esterilizar():
    gatos = servicio.listar_sin_esterilizar()
    colonia = servicio.reporte_colonia()
    return render_template("sin_esterilizar.html", gatos=gatos, colonia=colonia)


@app.route("/gatos")
def listar_gatos():
    gatos = servicio.listar_gatos()
    colonia = servicio.reporte_colonia()
    return render_template("gatos.html", gatos=gatos, colonia=colonia)


@app.route("/gatos/<id_gato>")
def ver_gato(id_gato):
    gato = servicio.obtener_gato(id_gato)
    if gato is None:
        return render_template("error.html", codigo=404,
                               mensaje=f"No existe ningún gato con id '{id_gato}'."), 404
    colonia = servicio.reporte_colonia()
    return render_template("gato_detalle.html", gato=gato, colonia=colonia)


# -- GATOS: ESCRITURA --

@app.route("/gatos/nuevo/<id_gato>/<nombre>/<color>/<sexo>/<estado>/<clinica>/<esterilizado>")
def registrar_gato(id_gato, nombre, color, sexo, estado, clinica, esterilizado):
    try:
        sexo_enum = Sexo(sexo)
    except ValueError:
        return f"Sexo no válido: '{sexo}'. Valores: H, M, ?", 400
    try:
        estado_enum = EstadoGato[estado]
    except KeyError:
        return f"Estado no válido: '{estado}'. Valores: COL, ACOG, ADOP, FALL, DESA", 400
    clinica_val = None if clinica == "none" else clinica
    esterilizado_bool = esterilizado == "True"
    try:
        servicio.registrar_gato(id_gato, nombre, color, sexo_enum,
                                estado_enum, clinica_val, esterilizado_bool)
    except GatoYaExisteError as e:
        return str(e), 409
    except ValueError as e:
        return str(e), 400
    return redirect(url_for("ver_gato", id_gato=id_gato))


@app.route("/gatos/<id_gato>/eliminar")
def quitar_gato(id_gato):
    try:
        servicio.quitar_gato(id_gato)
    except GatoNoEncontradoError as e:
        return str(e), 404
    return redirect(url_for("listar_gatos"))


@app.route("/gatos/<id_gato>/estado/<nuevo_estado>")
def cambiar_estado_gato(id_gato, nuevo_estado):
    try:
        estado_enum = EstadoGato[nuevo_estado]
    except KeyError:
        return f"Estado no válido: '{nuevo_estado}'. Valores: COL, ACOG, ADOP, FALL, DESA", 400
    try:
        servicio.actualizar_estado_gato(id_gato, estado_enum)
    except GatoNoEncontradoError as e:
        return str(e), 404
    except ValueError as e:
        return str(e), 400
    return redirect(url_for("ver_gato", id_gato=id_gato))


@app.route("/gatos/<id_gato>/esterilizar/<clinica>")
def esterilizar_gato(id_gato, clinica):
    clinica_val = None if clinica == "none" else clinica
    try:
        servicio.actualizar_esterilizacion_gato(id_gato, True, clinica_val)
    except GatoNoEncontradoError as e:
        return str(e), 404
    except ValueError as e:
        return str(e), 400
    return redirect(url_for("ver_gato", id_gato=id_gato))


# -- COLONIA --

@app.route("/colonia")
def reporte_colonia():
    reporte = servicio.reporte_colonia()
    return render_template("colonia.html", reporte=reporte)


@app.route("/colonia/censo")
def reporte_censo():
    reporte = servicio.reporte_censo()
    colonia = servicio.reporte_colonia()
    return render_template("censo.html", reporte=reporte, colonia=colonia)


@app.route("/colonia/estado/<nuevo_estado>")
def tramitar_anexo(nuevo_estado):
    try:
        estado_enum = EstadoColonia[nuevo_estado]
    except KeyError:
        return f"Estado no válido: '{nuevo_estado}'. Valores: ACTIVA, PENDIENTE, BAJA", 400
    try:
        servicio.tramitar_anexo(estado_enum)
    except ValueError as e:
        return str(e), 400
    return redirect(url_for("reporte_colonia"))


@app.route("/colonia/responsable/<tipo>/<nombre>/<telefono>/<email>/<identificacion>/<campo_extra>")
def asignar_responsable(tipo, nombre, telefono, email, identificacion, campo_extra):
    try:
        if tipo == "persona":
            responsable = PersonaFisica(nombre, telefono, email,
                                        identificacion, campo_extra)
        elif tipo == "protectora":
            responsable = Protectora(nombre, telefono, email,
                                     identificacion, campo_extra)
        else:
            return f"Tipo no válido: '{tipo}'. Valores: persona, protectora", 400
        servicio.asignar_responsable(responsable)
    except ValueError as e:
        return str(e), 400
    return redirect(url_for("reporte_colonia"))

@app.route("/ayuda")
def ayuda():
    reglas = [
        regla for regla in app.url_map.iter_rules()
        if regla.endpoint != "static"
    ]
    return render_template("ayuda.html", reglas=reglas)

# -- MANEJADORES DE ERROR --


@app.errorhandler(404)
def error_404(e):
    return render_template("error.html", codigo=404,
                           mensaje="La página solicitada no existe."), 404


@app.errorhandler(500)
def error_500(e):
    print("MANEJADOR 500 EJECUTADO")
    return render_template("error.html", codigo=500,
                           mensaje="Algo ha ido mal. Inténtalo de nuevo."), 500


if __name__ == "__main__":
    app.run(debug=True)