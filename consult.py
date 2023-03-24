from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import main
import sqlite3
from PyQt5.QtGui import QPixmap


class Consutar(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # cargar el archivo .ui
        self.main = None
        uic.loadUi('sources/consult.ui', self)

        # establecer tamaño fijo de la ventana
        self.setFixedSize(self.size())

        self.conexion = sqlite3.connect('sources/database.bd', timeout=10)
        self.flag = 0
        # conecta los botones a sus correspondientes funciones
        self.btn_consult.clicked.connect(self.funcion_consultar)
        self.btn_delete.clicked.connect(self.funcion_eliminar)
        self.btn_export.clicked.connect(self.funcion_exportar)
        self.btn_cancel.clicked.connect(self.funcion_cancelar)

        self.btn_back.clicked.connect(self.funcion_volver)
        self.btn_update.clicked.connect(self.funcion_actualizar)
        self.btn_next.clicked.connect(self.funcion_siguiente)

        self.mostrar_combobox()

    def mostrar_combobox(self):
        # Obtener los datos de la columna de la tabla
        cursor = self.conexion.cursor()
        datos = []

        try:
            cursor.execute("SELECT * FROM registros")
            datos = cursor.fetchall()
            cursor.close()
        except Exception as e:
            msg = (f"Ha ocurrido un error: {e}")
            self.ventana_emergente(msg)

        # Agregar los datos al combo box
        for dato in datos:
            self.cb_project.addItem(str(dato[1]))
            self.cb_loop.addItem(str(dato[2]))
            self.cb_id.addItem(str(dato[3]))
            self.cb_tester.addItem(str(dato[9]))
            self.cb_case.addItem(str(dato[4]))
        pass

    def buscar_id(self):
        cursor = self.conexion.cursor()

        proyecto = self.cb_project.currentText()
        ciclo = self.cb_loop.currentText()
        idc = self.cb_id.currentText()
        caso = self.cb_case.currentText()
        tester = self.cb_tester.currentText()

        try:
            cunsulta = """SELECT ejecucion_id FROM registros WHERE proyecto = ? AND ciclo = ? 
                        AND id = ? AND casoprueba = ? AND tester = ?"""
            parametros = (proyecto, ciclo, idc, caso, tester)

            # ejecutar consulta
            cursor.execute(cunsulta, parametros)
            resultado = cursor.fetchall()
            return resultado[0][0]
        except Exception as e:
            msg = (f"No se encontro registro con los datos proporcionados {e}")
            self.ventana_emergente(msg)

    def funcion_consultar(self):
        cursor = self.conexion.cursor()
        self.flag = 0

        try:
            cursor.execute("SELECT descripcion, resultadoesperado FROM registros WHERE ejecucion_id = ?",
                           (self.buscar_id(),))
            resultado = cursor.fetchall()

            # se cargan los label
            self.lbl_description.setText(f"Descripcion: {resultado[0][0]}")
            self.lbl_ra.setText(f"Resultado esperado: {resultado[0][1]}")

            # Cerrar la conexión a la base de datos y devolver el resultado de la consulta
            cursor.close()
            self.buscar_imagenes()
        except:
            pass

    def funcion_eliminar(self):
        cursor = self.conexion.cursor()
        try:
            ide = self.buscar_id()
            cprueba = cursor.execute("SELECT casoprueba FROM registros WHERE ejecucion_id = ?", (ide,)).fetchone()[0]
            cursor.execute("DELETE FROM evidencias WHERE ejecucion_id = ?", (ide,))
            cursor.execute("DELETE FROM registros WHERE ejecucion_id = ?", (ide,))
            self.conexion.commit()
            cursor.close()
            self.limpiar_box()
            self.mostrar_combobox()
            if not cprueba:
                msg = "Registro vacío"
            else:
                msg = (f"Se eliminó el registro: {cprueba}")
            self.ventana_emergente(msg)
        except Exception as e:
            print("llego aqi")
            msg = e
            self.ventana_emergente(msg)

    def funcion_volver(self):
        if self.lbl_fotopaso.pixmap() is None:
            # Si el QLabel no tiene una imagen asignada, no hace nada
            return
        elif self.flag == 0:
            msg = ("Estas en el primer registro")
            self.ventana_emergente(msg)
        else:
            self.flag -= 1
            self.buscar_imagenes(self.flag)

    def funcion_actualizar(self):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("SELECT * FROM evidencias WHERE ejecucion_id = ?", (self.buscar_id(),))
            bloque = cursor.fetchall()
            id_update = bloque[self.flag][0]
            casotext = self.txt_pasodesc.toPlainText()
            cursor.execute("UPDATE evidencias SET caso = ? WHERE id_primario = ?", (casotext, id_update))
            self.conexion.commit()
            cursor.close()
            msg = ("Registro actualizado! ")
            self.ventana_emergente(msg)
        except:
            pass

    def funcion_siguiente(self):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("SELECT COUNT(ejecucion_id) FROM evidencias WHERE ejecucion_id = ?", (self.buscar_id(),))
            conteo = cursor.fetchall()
            valores = int(conteo[0][0])
            if self.lbl_fotopaso.pixmap() is None:
                # Si el QLabel no tiene una imagen asignada, no hace nada
                return
            elif self.flag == valores-1:
                msg = ("Estas en el ultimo registro ")
                self.ventana_emergente(msg)
            else:
                self.flag += 1
                self.buscar_imagenes(self.flag)
        except:
            pass

    def buscar_imagenes(self, flag=0):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("SELECT * FROM evidencias WHERE ejecucion_id = ?", (self.buscar_id(),))
            evidencias = cursor.fetchall()
            if evidencias:
                self.txt_pasodesc.setText(evidencias[flag][2])
                foto = QPixmap()
                foto.loadFromData(evidencias[flag][3], "PNG", Qt.AutoColor)
                # Redimensionar la imagen al tamaño del QLabel
                foto = foto.scaled(self.lbl_fotopaso.width(), self.lbl_fotopaso.height())
                self.lbl_fotopaso.setPixmap(foto)
            else:
                self.lbl_numero.setText("Caso: None")
                self.lbl_imagens.clear()
            cursor.close()
        except:
            msg = ("No se encontro registro de evidencias ")
            self.ventana_emergente(msg)

    def funcion_exportar(self):
        # querys para extraer toda la informacion
        consulta_registro = (f"SELECT * FROM registros WHERE ejecucion_id = {self.buscar_id()}")
        consulta_evidencias = (f"SELECT * FROM evidencias WHERE ejecucion_id = {self.buscar_id()}")

        cursor = self.conexion.cursor()

        cursor.execute(consulta_registro)
        registro = cursor.fetchall()

        cursor.execute(consulta_evidencias)
        evidencias = cursor.fetchall()

        # Definir el estilo para los encabezados y párrafos en el documento
        estilo_encabezado = ParagraphStyle(name='Encabezado', fontSize=16, leading=20)
        estilo_parrafo = ParagraphStyle(name='Parrafo', fontSize=12, leading=14)
        # Definir el estilo para el título del documento
        estilo_titulo = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=20, leading=26,
                                       alignment=TA_CENTER)

        # Crear un objeto SimpleDocTemplate para generar el documento PDF
        nombre_archivo = f"{registro[0][1]}.pdf"
        pdf = SimpleDocTemplate(nombre_archivo, pagesize=letter)

        # Agregar el título al PDF utilizando el estilo definido
        titulo = "Documentacion de caso de prueba\n"
        contenido = [Paragraph(titulo, estilo_titulo)]

        # Agregar los valores al PDF utilizando los estilos definidos
        campos = ["Proyecto:", "Ciclo:", "Id caso de prueba:", "Nombre de caso de prueba:", "Descripción:",
                  "Pre requisitos:", "Datos de prueba:", "Resultado esperado:", "Tester:", "Fecha de ejecucion:"]
        for campo, valor in zip(campos, registro[0][1:]):
            contenido.append(Paragraph(campo, estilo_encabezado))
            contenido.append(Paragraph(valor, estilo_parrafo))
            contenido.append(Paragraph("\n", estilo_parrafo))

        for valor in evidencias:
            print(valor[2])
            contenido.append(Paragraph(valor[2], estilo_encabezado))
            print(valor[3])

        pdf.build(contenido)
        pass

    def ventana_emergente(self, mensaje):
        popup = QMessageBox()
        popup.setWindowTitle("Aviso!")
        popup.setText(mensaje)
        popup.setIcon(QMessageBox.Information)
        popup.exec_()

    def limpiar_box(self):
        self.cb_project.clear()
        self.cb_loop.clear()
        self.cb_id.clear()
        self.cb_tester.clear()
        self.cb_case.clear()
        self.lbl_description.clear()
        self.lbl_ra.clear()
        self.lbl_fotopaso.clear()
        self.txt_pasodesc.clear()

    def funcion_cancelar(self):
        self.main = main.TestKeep()
        self.main.show()
        self.close()
