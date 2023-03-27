from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import main
import test
import sqlite3
import datetime


class Nuevor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # cargar el archivo .ui
        uic.loadUi('sources/newr.ui', self)

        # establecer tamaño fijo de la ventana
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon("sources/tk_log.png"))

        #cargar base de datos
        self.conexion = sqlite3.connect('sources/database.bd', timeout=10)

        # conecta los botones a sus correspondientes funciones
        self.btn_start.clicked.connect(self.funcion_iniciar)
        self.btn_clean.clicked.connect(self.funcion_limpiar)
        self.btn_cancel.clicked.connect(self.funcion_regresar)

        # Establecer que el widgets cambie de foco cuando se presione Tab
        self.txt_proyecto.setTabChangesFocus(True)
        self.txt_loop.setTabChangesFocus(True)
        self.txt_id.setTabChangesFocus(True)
        self.txt_caset.setTabChangesFocus(True)
        self.txt_description.setTabChangesFocus(True)
        self.txt_sources.setTabChangesFocus(True)
        self.txt_datat.setTabChangesFocus(True)
        self.txt_result.setTabChangesFocus(True)
        self.txt_tester.setTabChangesFocus(True)


    #popup
    def ventana_emergente(self, mensaje):
        popup = QMessageBox()
        popup.setWindowTitle("Aviso!")
        popup.setText(mensaje)
        popup.setIcon(QMessageBox.Information)
        popup.exec_()

    #Se usa para guardar el registro del formulario
    def funcion_iniciar(self):

        proyecto = self.txt_proyecto.toPlainText()
        ciclo = self.txt_loop.toPlainText()
        id = self.txt_id.toPlainText()
        casoprueba = self.txt_caset.toPlainText()
        descripcion = self.txt_description.toPlainText()
        prerequisitos = self.txt_sources.toPlainText()
        datosprueba = self.txt_datat.toPlainText()
        resultadoesperado = self.txt_result.toPlainText()
        tester = self.txt_tester.toPlainText()
        fecha = datetime.date.today().strftime('%Y-%m-%d')

        try:
            #inserta en bd
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO registros (
                    proyecto,
                    ciclo,
                    id,
                    casoprueba,
                    descripcion,
                    prerequisitos,
                    datosprueba,
                    resultadoesperado,
                    tester,
                    fecha
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                proyecto,
                ciclo,
                id,
                casoprueba,
                descripcion,
                prerequisitos,
                datosprueba,
                resultadoesperado,
                tester,
                fecha
            ))
            self.conexion.commit()
            cursor.close()
            msg = "Datos guardados exitosamente"
            self.ventana_emergente(msg)
            self.funcion_limpiar()
            self.abrir_ventana_test()
            pass
        except Exception as e:
            msg = (f"Ha ocurrido un error: {e}")
            self.ventana_emergente(msg)
            self.funcion_limpiar()

    def funcion_limpiar(self):
        self.txt_proyecto.clear()
        self.txt_loop.clear()
        self.txt_id.clear()
        self.txt_caset.clear()
        self.txt_description.clear()
        self.txt_sources.clear()
        self.txt_datat.clear()
        self.txt_result.clear()
        self.txt_tester.clear()

    def abrir_ventana_test(self):
        self.nuevo = test.Testing()
        self.nuevo.show()
        self.hide()

    def funcion_regresar(self):
        self.main = main.TestKeep()
        self.main.show()
        self.close()
