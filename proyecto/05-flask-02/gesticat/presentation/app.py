"""
Presentación/app: Interfaz web con Flask.

Segunda capa de presentación del proyecto. Expone todas las operaciones
del dominio como routes HTTP. El menú de consola (menu.py) sigue funcionando
sin cambios — ambas interfaces comparten el mismo ServicioColonia.
"""
import logging

from flask import Flask, redirect, url_for, request

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
    return (
        "<h1>GestiCat LPGC</h1>"
        "<h2>😺 Gatos</h2>"
        "<ul>"
        "<li><a href='/gatos'>Lista de gatos</a></li>"
        "<li><a href='/gatos/sin-esterilizar'>Gatos sin esterilizar</a></li>"
        "</ul>"
        "<h2>🏠 Colonia</h2>"
        "<ul>"
        "<li><a href='/colonia'>Reporte general</a></li>"
        "<li><a href='/colonia/censo'>Reporte de censo</a></li>"
        "</ul>"
    )


# -- GATOS: LECTURA --

@app.route("/gatos/sin-esterilizar")
def listar_sin_esterilizar():
    gatos = servicio.listar_sin_esterilizar()
    if not gatos:
        return "Todos los gatos activos están esterilizados."
    lineas = [
        f"[{g.id_gato}] {g.nombre} — {g.sexo.value} — {g.estado.value}"
        for g in gatos
    ]
    return "<br>".join(lineas)


@app.route("/gatos")
def listar_gatos():
    gatos = servicio.listar_gatos()
    if not gatos:
        return "No hay gatos registrados."
    lineas = [
        f"[{g.id_gato}] {g.nombre} — {g.color} — {g.sexo.value} "
        f"— {g.estado.value} — Esterilizado: {g.esterilizado}"
        for g in gatos
    ]
    return "<br>".join(lineas)


@app.route("/gatos/<id_gato>")
def ver_gato(id_gato):
    gato = servicio.obtener_gato(id_gato)
    if gato is None:
        return f"No existe ningún gato con id '{id_gato}'.", 404
    return (
        f"ID: {gato.id_gato}<br>"
        f"Nombre: {gato.nombre}<br>"
        f"Color: {gato.color}<br>"
        f"Sexo: {gato.sexo.value}<br>"
        f"Estado: {gato.estado.value}<br>"
        f"Clínica: {gato.clinica_veterinaria or 'Sin clínica'}<br>"
        f"Esterilizado: {gato.esterilizado}<br>"
        f"Fecha registro: {gato.fecha_registro.strftime('%d/%m/%Y')}<br>"
    )


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
    r = servicio.reporte_colonia()
    return (
        f"Nombre: {r['nombre']}<br>"
        f"Responsable: {r['responsable']}<br>"
        f"Estado: {r['estado']}<br>"
        f"Última actualización: {r['ultima_actualizacion']}<br>"
        f"Necesita actualización: {r['necesita_actualizacion']}<br>"
        f"Total gatos activos: {r['total_gatos']}<br>"
    )


@app.route("/colonia/censo")
def reporte_censo():
    r = servicio.reporte_censo()
    return (
        f"Total activos: {r['total']}<br>"
        f"Machos: {r['machos']}<br>"
        f"Hembras: {r['hembras']}<br>"
        f"Desconocidos: {r['desconocidos']}<br>"
        f"Esterilizados: {r['esterilizados']}<br>"
        f"No esterilizados: {r['no_esterilizados']}<br>"
    )


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
    lineas = ["<h1>GestiCat — Rutas disponibles</h1><ul>"]
    for regla in app.url_map.iter_rules():
        if regla.endpoint != "static":
            regla_escapada = regla.rule.replace("<", "{").replace(">", "}")
            lineas.append(
                f"<li><code>{regla_escapada}</code> — {regla.endpoint}</li>"
            )
    lineas.append("</ul>")
    return "\n".join(lineas)

# -- MANEJADORES DE ERROR --

@app.errorhandler(404)
def error_404(e):
    return (
        "<h1>404 — Página no encontrada</h1>"
        "<img src='/static/404.jpg' alt='404 cat' width='400'><br>"        "<p>La ruta solicitada no existe.</p>"
        "<p><a href='/'>Volver al inicio</a></p>"
    ), 404


@app.errorhandler(500)
def error_500(e):
    return (
        "<h1>500 — Error interno del servidor</h1>"
        "<img src='/static/500.jpg' alt='500 cat' width='400'><br>"        "<p>La ruta solicitada no existe.</p>"
        "<p>Algo ha ido mal. Inténtalo de nuevo.</p>"
        "<p><a href='/'>Volver al inicio</a></p>"
    ), 500


if __name__ == "__main__":
    app.run(debug=True)