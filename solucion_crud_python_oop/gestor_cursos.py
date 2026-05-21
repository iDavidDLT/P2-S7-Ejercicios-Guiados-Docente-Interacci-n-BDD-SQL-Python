"""
BASE DE DATOS II
Programa CRUD orientado a objetos en Python con SQL Server.
Base de datos: UDEMYTEST1
Tabla: Cursos
Conexión: config.json
Operaciones: Stored Procedures
"""

import json
import pyodbc


class GestorCursos:
    """Clase encargada de gestionar la conexión y las operaciones CRUD de Cursos."""

    def __init__(self):
        self.conexion = None

        try:
            with open("config.json", "r", encoding="utf-8") as archivo_config:
                config = json.load(archivo_config)

            name_server = config["name_server"]
            database = config["database"]
            controlador_odbc = config["controlador_odbc"]

            self.connection_string = (
                f"DRIVER={{{controlador_odbc}}};"
                f"SERVER={name_server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
            )

            self.conexion = pyodbc.connect(self.connection_string)
            print("\nConexión exitosa a SQL Server.\n")

        except Exception as e:
            print("\nOcurrió un error al conectar con SQL Server:")
            print(e)
            self.conexion = None

    def insertar_curso(self):
        """Inserta un nuevo curso usando el procedimiento almacenado sp_insertar_curso."""
        try:
            print("\n--- INSERTAR CURSO ---")
            nombre = input("Nombre del curso: ").strip()
            descripcion = input("Descripción: ").strip()
            duracion = int(input("Duración en horas: "))
            precio = float(input("Precio: "))
            estado = int(input("Estado (1 = activo, 0 = inactivo): "))

            cursor = self.conexion.cursor()
            cursor.execute(
                "EXEC dbo.sp_insertar_curso ?, ?, ?, ?, ?",
                nombre,
                descripcion,
                duracion,
                precio,
                estado,
            )
            resultado = cursor.fetchone()
            self.conexion.commit()

            print(f"Curso insertado correctamente. ID generado: {int(resultado[0])}")

        except ValueError:
            print("Error: La duración, el precio y el estado deben ser valores numéricos.")
        except Exception as e:
            print("Ocurrió un error al insertar el curso:", e)

    def consultar_cursos(self):
        """Consulta todos los cursos usando el procedimiento almacenado sp_consultar_cursos."""
        try:
            print("\n--- LISTA DE CURSOS ---")
            cursor = self.conexion.cursor()
            cursor.execute("EXEC dbo.sp_consultar_cursos")
            registros = cursor.fetchall()

            if not registros:
                print("No existen cursos registrados.")
                return

            print(f"{'ID':<5}{'Nombre':<25}{'Duración':<12}{'Precio':<12}{'Estado':<10}Descripción")
            print("-" * 95)
            for r in registros:
                estado_texto = "Activo" if r.Estado else "Inactivo"
                print(
                    f"{r.IDCurso:<5}"
                    f"{r.NombreCurso:<25}"
                    f"{r.DuracionHoras:<12}"
                    f"${float(r.Precio):<11.2f}"
                    f"{estado_texto:<10}"
                    f"{r.Descripcion}"
                )

        except Exception as e:
            print("Ocurrió un error al consultar los cursos:", e)

    def buscar_curso_por_id(self):
        """Busca un curso específico por su ID."""
        try:
            print("\n--- BUSCAR CURSO POR ID ---")
            id_curso = int(input("Ingrese el ID del curso: "))

            cursor = self.conexion.cursor()
            cursor.execute("EXEC dbo.sp_buscar_curso_por_id ?", id_curso)
            curso = cursor.fetchone()

            if curso is None:
                print("No se encontró un curso con ese ID.")
            else:
                estado_texto = "Activo" if curso.Estado else "Inactivo"
                print("\nCurso encontrado:")
                print(f"ID: {curso.IDCurso}")
                print(f"Nombre: {curso.NombreCurso}")
                print(f"Descripción: {curso.Descripcion}")
                print(f"Duración: {curso.DuracionHoras} horas")
                print(f"Precio: ${float(curso.Precio):.2f}")
                print(f"Estado: {estado_texto}")

        except ValueError:
            print("Error: El ID debe ser un número entero.")
        except Exception as e:
            print("Ocurrió un error al buscar el curso:", e)

    def actualizar_curso(self):
        """Actualiza un curso usando el procedimiento almacenado sp_actualizar_curso."""
        try:
            print("\n--- ACTUALIZAR CURSO ---")
            id_curso = int(input("ID del curso a actualizar: "))
            nombre = input("Nuevo nombre del curso: ").strip()
            descripcion = input("Nueva descripción: ").strip()
            duracion = int(input("Nueva duración en horas: "))
            precio = float(input("Nuevo precio: "))
            estado = int(input("Nuevo estado (1 = activo, 0 = inactivo): "))

            cursor = self.conexion.cursor()
            cursor.execute(
                "EXEC dbo.sp_actualizar_curso ?, ?, ?, ?, ?, ?",
                id_curso,
                nombre,
                descripcion,
                duracion,
                precio,
                estado,
            )
            resultado = cursor.fetchone()
            self.conexion.commit()

            if resultado and resultado.FilasAfectadas > 0:
                print("Curso actualizado correctamente.")
            else:
                print("No se actualizó ningún registro. Verifique el ID ingresado.")

        except ValueError:
            print("Error: El ID, duración, precio y estado deben ser valores numéricos.")
        except Exception as e:
            print("Ocurrió un error al actualizar el curso:", e)

    def eliminar_curso(self):
        """Elimina un curso usando el procedimiento almacenado sp_eliminar_curso."""
        try:
            print("\n--- ELIMINAR CURSO ---")
            id_curso = int(input("ID del curso a eliminar: "))
            confirmacion = input("¿Está seguro de eliminar este curso? (s/n): ").lower()

            if confirmacion != "s":
                print("Operación cancelada.")
                return

            cursor = self.conexion.cursor()
            cursor.execute("EXEC dbo.sp_eliminar_curso ?", id_curso)
            resultado = cursor.fetchone()
            self.conexion.commit()

            if resultado and resultado.FilasAfectadas > 0:
                print("Curso eliminado correctamente.")
            else:
                print("No se eliminó ningún registro. Verifique el ID ingresado.")

        except ValueError:
            print("Error: El ID debe ser un número entero.")
        except Exception as e:
            print("Ocurrió un error al eliminar el curso:", e)

    def ejecutar_menu(self):
        """Muestra el menú principal del sistema CRUD."""
        while True:
            print("\n\t******************************")
            print("\t** SISTEMA CRUD UDEMYTEST1  **")
            print("\t******************************")
            print("\t1. Crear registro")
            print("\t2. Consultar registros")
            print("\t3. Buscar registro por ID")
            print("\t4. Actualizar registro")
            print("\t5. Eliminar registro")
            print("\t6. Salir")

            opcion = input("\nSeleccione una opción 1-6: ").strip()

            if opcion == "1":
                self.insertar_curso()
            elif opcion == "2":
                self.consultar_cursos()
            elif opcion == "3":
                self.buscar_curso_por_id()
            elif opcion == "4":
                self.actualizar_curso()
            elif opcion == "5":
                self.eliminar_curso()
            elif opcion == "6":
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def cerrar_conexion(self):
        """Cierra la conexión con SQL Server."""
        try:
            self.conexion.close()
            print("Conexión cerrada correctamente.")
        except Exception as e:
            print("No se pudo cerrar la conexión:", e)


if __name__ == "__main__":
    gestor = None
    try:
        gestor = GestorCursos()
        gestor.ejecutar_menu()
    except Exception:
        print("El programa finalizó por un error de conexión o configuración.")
    finally:
        if gestor is not None:
            gestor.cerrar_conexion()
