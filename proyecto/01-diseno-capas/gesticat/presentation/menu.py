"""
Presentación/menu: Interfaz de consola del proyecto GestiCat.

Este módulo muestra el menú principal y gestiona la interacción con el usuario.
No contiene lógica de negocio — esa responsabilidad es del dominio.
"""

from application.servicio_colonia import ServicioColonia
from domain.colonia import EstadoColonia
from domain.gato import EstadoGato, Sexo
from domain.responsable import PersonaFisica, Protectora
from infrastructure.datos_iniciales import cargar_datos_iniciales

# -- MENÚ --

def mostrar_menu():
    """Muestra las opciones del menú principal."""
    print("\n=== GestiCat - Menú principal ===")
    print("--- Gatos ---")
    print("1. Registrar gato.")
    print("2. Borrar registro del gato.")
    print("3. Actualizar estado del gato.")
    print("4. Marcar gato como esterilizado.")
    print("5. Listar gatos sin esterilizar.")
    print("--- Colonia ---")
    print("6. Asignar responsable.")
    print("7. Tramitar anexo.")
    print("--- Reportes ---")
    print("8. Reporte de censo.")
    print("9. Reporte de colonia.")
    print("--- ---")
    print("0. Salir.")



# -- OPCIONES DE GATOS --

# TODO: Aplicar try/except para poder hacer bucles que repita solo el input incorrecto sin el 'return' de los fallos que sale de las funciones y regreas al bucle del menú principal. 

def registrar_gato(servicio: ServicioColonia):
    """Pide los datos de un gato y lo registra en la colonia."""
    print("\n-- Registrar gato. --")
    id_gato = input("ID (3 dígitos): ").strip()
    if not id_gato.isdigit() or len(id_gato) != 3:
        print("❌ El ID debe ser exactamente 3 dígitos.")
        return
    nombre = input("Nombre: ")
    color = input("Color: ")
    print("Sexo: H=Hembra, M=Macho, ?=Desconocido")
    sexo_input = input("Sexo: ").strip().upper()
    conversion = {"H": Sexo.HEMBRA, "M": Sexo.MACHO, "?": Sexo.DESCONOCIDO}
    if sexo_input not in conversion:
        print("❌ Sexo no válido.")
        return
    sexo = conversion[sexo_input]
    print("Estado: COL=En colonia, ACOG=En acogida, ADOP=Adoptado, FALL=Fallecido, DESA=Desaparecido")
    estado_input = input("Estado: ").strip().upper()
    if estado_input not in EstadoGato.__members__:
        print("❌ Estado no válido.")
        return
    estado = EstadoGato[estado_input]
    clinica = input("Clínica veterinaria (Enter para dejar vacío): ").strip() or None
    esterilizado_input = input("¿Esterilizado? (s/n): ").strip().lower()
    if esterilizado_input not in ("s", "n"):
        print("❌ Opción no válida. Introduce s o n.")
        return
    esterilizado = esterilizado_input == "s"
    fecha_registro = input("Fecha de registro (dd/mm/aaaa): ")
    servicio.registrar_gato(id_gato, nombre, color, sexo, estado,
                            clinica, esterilizado, fecha_registro)
    print(f"✅ Gato '{nombre}' registrado correctamente.")
    

def quitar_gato(servicio: ServicioColonia):
    """Pide el id de un gato y borra su registro de la colonia."""
    print("\n-- Borrar registro del gato. --")
    id_gato = input("ID del gato: ")
    servicio.quitar_gato(id_gato)
    print("✅ Registro del gato borrado correctamente.")


def actualizar_estado_gato(servicio: ServicioColonia):
    """Pide el id de un gato y actualiza su estado."""
    print("\n-- Actualizar estado del gato. --")
    id_gato = input("ID del gato: ")
    print("Estado: COL=En colonia, ACOG=En acogida, ADOP=Adoptado, FALL=Fallecido, DESA=Desaparecido")
    estado_input = input("Nuevo estado: ").strip().upper()
    if estado_input not in EstadoGato.__members__:
        print("❌ Estado no válido.")
        return
    estado = EstadoGato[estado_input]
    servicio.actualizar_estado_gato(id_gato, estado)
    print("✅ Estado actualizado correctamente.")


def actualizar_esterilizacion_gato(servicio: ServicioColonia):
    """Pide el id de un gato y lo marca como esterilizado."""
    print("\n-- Marcar gato como esterilizado. --")
    id_gato = input("ID del gato: ")
    clinica = input("Clínica veterinaria (Enter para mantener la actual): ").strip() or None
    servicio.actualizar_esterilizacion_gato(id_gato, True, clinica)
    print("✅ Gato marcado como esterilizado correctamente.")


def listar_sin_esterilizar(servicio: ServicioColonia):
    """Muestra los gatos activos no esterilizados."""
    print("\n-- Gatos sin esterilizar. --")
    gatos = servicio.listar_sin_esterilizar()
    if not gatos:
        print("Todos los gatos activos están esterilizados.")
        return
    for g in gatos:
        print(f"  {g.id_gato} | {g.nombre} | {g.sexo.value} | {g.estado.value}")


# -- OPCIONES DE COLONIA --

def asignar_responsable(servicio: ServicioColonia):
    """Pide los datos de un responsable y lo asigna a la colonia."""
    print("\n-- Asignar responsable. --")
    print("Tipo: 1=Persona física, 2=Protectora.")
    tipo = input("Tipo: ").strip()
    if tipo not in ("1", "2"):
        print("❌ Tipo no válido.")
        return
    nombre = input("Nombre: ")
    telefono = input("Teléfono (9 dígitos): ")
    email = input("Email: ")
    identificacion = input("DNI/NIF/CIF: ")
    if tipo == "1":
        fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
        responsable = PersonaFisica(nombre, telefono, email,
                                    identificacion, fecha_nacimiento)
    else:
        numero_registro = input("Número de registro: ")
        responsable = Protectora(nombre, telefono, email,
                                 identificacion, numero_registro)
    servicio.asignar_responsable(responsable)
    print("✅ Responsable asignado correctamente.")


def tramitar_anexo(servicio: ServicioColonia):
    """Muestra los estados disponibles y tramita el cambio."""
    print("\n-- Tramitar anexo. --")
    print("Estados disponibles:")
    print("  ACTIVA    → Registro municipal aprobado.")
    print("  PENDIENTE → Requiere revisión trimestral.")
    print("  BAJA      → Cese de actividad.")
    estado_input = input("Nuevo estado: ").strip().upper()
    if estado_input not in EstadoColonia.__members__:
        print("❌ Estado no válido.")
        return
    estado = EstadoColonia[estado_input]
    servicio.tramitar_anexo(estado)
    print("✅ Anexo tramitado correctamente.")


# -- REPORTES --

def mostrar_reporte_censo(servicio: ServicioColonia):
    """Muestra el reporte de censo de la colonia."""
    print("\n-- Reporte de censo. --")
    reporte = servicio.reporte_censo()
    print(f"  Total gatos activos : {reporte['total']}")
    print(f"  Machos              : {reporte['machos']}")
    print(f"  Hembras             : {reporte['hembras']}")
    print(f"  Desconocidos        : {reporte['desconocidos']}")
    print(f"  Esterilizados       : {reporte['esterilizados']}")
    print(f"  No esterilizados    : {reporte['no_esterilizados']}")


def mostrar_reporte_colonia(servicio: ServicioColonia):
    """Muestra la información general de la colonia."""
    print("\n-- Reporte de colonia. --")
    reporte = servicio.reporte_colonia()
    print(f"  Nombre              : {reporte['nombre']}")
    print(f"  Responsable         : {reporte['responsable']}")
    print(f"  Estado              : {reporte['estado']}")
    print(f"  Última actualización: {reporte['ultima_actualizacion']}")
    print(f"  Necesita revisión   : {'Sí' if reporte['necesita_actualizacion'] else 'No'}")
    print(f"  Total gatos activos : {reporte['total_gatos']}")


# -- BUCLE PRINCIPAL --

def main():
    """Punto de entrada del menú interactivo."""
    colonia = cargar_datos_iniciales()
    servicio = ServicioColonia(colonia)
    while True:
        mostrar_menu()
        opcion = input("\nElige una opción: ").strip()
        try:
            if opcion == "0":
                print("See you later, alligator!")
                break
            elif opcion == "1":
                registrar_gato(servicio)
            elif opcion == "2":
                quitar_gato(servicio)
            elif opcion == "3":
                actualizar_estado_gato(servicio)
            elif opcion == "4":
                actualizar_esterilizacion_gato(servicio)
            elif opcion == "5":
                listar_sin_esterilizar(servicio)
            elif opcion == "6":
                asignar_responsable(servicio)
            elif opcion == "7":
                tramitar_anexo(servicio)
            elif opcion == "8":
                mostrar_reporte_censo(servicio)
            elif opcion == "9":
                mostrar_reporte_colonia(servicio)
            else:
                print("❌ Opción no válida.")
        except ValueError as e:
            print("❌ " + str(e))


if __name__ == "__main__":
    main()