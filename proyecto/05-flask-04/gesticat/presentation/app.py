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

@app.route("/gatos/nuevo", methods=['GET', 'POST'])
def registrar_gato():
    if request.method == 'POST':
        datos = request.form
        try:
            sexo_enum = Sexo(datos['sexo'])
            estado_enum = EstadoGato[datos['estado']]
            clinica = datos['clinica'].strip() or None
            esterilizado = datos['esterilizado'] == 'True'
            fecha = datos['fecha_registro'].strip() or None
            servicio.registrar_gato(
                datos['id_gato'], datos['nombre'], datos['color'],
                sexo_enum, estado_enum, clinica, esterilizado, fecha
            )
        except GatoYaExisteError as e:
            return render_template('registrar_gato.html', error=str(e), datos=datos), 409
        except (ValueError, KeyError) as e:
            return render_template('registrar_gato.html', error=str(e), datos=datos), 400
        return redirect(url_for('ver_gato', id_gato=datos['id_gato']))
    return render_template('registrar_gato.html', error=None, datos={})


@app.route("/gatos/<id_gato>/quitar", methods=['GET', 'POST'])
def quitar_gato(id_gato):
    gato = servicio.obtener_gato(id_gato)
    if gato is None:
        return render_template("error.html", codigo=404,
                               mensaje=f"No existe ningún gato con id '{id_gato}'."), 404
    if request.method == 'POST':
        try:
            servicio.quitar_gato(id_gato)
        except GatoNoEncontradoError as e:
            return render_template("error.html", codigo=404, mensaje=str(e)), 404
        return redirect(url_for('listar_gatos'))
    return render_template('quitar_gato.html', gato=gato)


@app.route("/gatos/<id_gato>/estado", methods=['GET', 'POST'])
def cambiar_estado_gato(id_gato):
    gato = servicio.obtener_gato(id_gato)
    if gato is None:
        return render_template("error.html", codigo=404,
                               mensaje=f"No existe ningún gato con id '{id_gato}'."), 404
    if request.method == 'POST':
        datos = request.form
        try:
            estado_enum = EstadoGato[datos['nuevo_estado']]
            servicio.actualizar_estado_gato(id_gato, estado_enum)
        except (KeyError, ValueError) as e:
            return render_template('cambiar_estado_gato.html', gato=gato,
                                   error=str(e), datos=datos), 400
        return redirect(url_for('ver_gato', id_gato=id_gato))
    return render_template('cambiar_estado_gato.html', gato=gato, error=None, datos={})


@app.route("/gatos/<id_gato>/esterilizar", methods=['GET', 'POST'])
def esterilizar_gato(id_gato):
    gato = servicio.obtener_gato(id_gato)
    if gato is None:
        return render_template("error.html", codigo=404,
                               mensaje=f"No existe ningún gato con id '{id_gato}'."), 404
    if request.method == 'POST':
        datos = request.form
        try:
            clinica = datos['clinica'].strip() or None
            servicio.actualizar_esterilizacion_gato(id_gato, True, clinica)
        except (ValueError, GatoNoEncontradoError) as e:
            return render_template('esterilizar_gato.html', gato=gato,
                                   error=str(e), datos=datos), 400
        return redirect(url_for('ver_gato', id_gato=id_gato))
    return render_template('esterilizar_gato.html', gato=gato, error=None, datos={})


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


@app.route("/colonia/estado", methods=['GET', 'POST'])
def tramitar_anexo():
    colonia = servicio.reporte_colonia()
    if request.method == 'POST':
        datos = request.form
        try:
            estado_enum = EstadoColonia[datos['nuevo_estado']]
            servicio.tramitar_anexo(estado_enum)
        except (KeyError, ValueError) as e:
            return render_template('tramitar_anexo.html', colonia=colonia,
                                   error=str(e), datos=datos), 400
        return redirect(url_for('reporte_colonia'))
    return render_template('tramitar_anexo.html', colonia=colonia, error=None, datos={})


@app.route("/colonia/responsable", methods=['GET', 'POST'])
def asignar_responsable():
    if request.method == 'POST':
        datos = request.form
        try:
            if datos['tipo'] == 'persona':
                responsable = PersonaFisica(
                    datos['nombre'], datos['telefono'], datos['email'],
                    datos['identificacion'], datos['campo_extra']
                )
            elif datos['tipo'] == 'protectora':
                responsable = Protectora(
                    datos['nombre'], datos['telefono'], datos['email'],
                    datos['identificacion'], datos['campo_extra']
                )
            else:
                raise ValueError("Tipo de responsable no válido.")
            servicio.asignar_responsable(responsable)
        except ValueError as e:
            return render_template('asignar_responsable.html',
                                   error=str(e), datos=datos), 400
        return redirect(url_for('reporte_colonia'))
    return render_template('asignar_responsable.html', error=None, datos={})

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