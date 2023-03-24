from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import QByteArray, QIODevice, QBuffer, Qt
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QScreen, QKeySequence
import main
import consult
import sqlite3
from PyQt5.QtGui import QPixmap


class Testing(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # cargar el archivo .ui
        uic.loadUi('sources/test.ui', self)

        self.conexion = sqlite3.connect('sources/database.bd', timeout=10)

        # conecta los botones a sus correspondientes funciones
        self.btn_start.clicked.connect(self.funcion_iniciar)
        self.btn_save.clicked.connect(self.funcion_terminar)
        self.btn_cancel.clicked.connect(self.funcion_cancelar)

        # Conectar la tecla "F1" a la función 'show'
        self.keyPressedSignal = QtCore.pyqtSignal(int)
        #self.keyPressedSignal.connect(self.keyPressEvent)

    # Agregar el siguiente método para capturar las pulsaciones de teclas
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.funcion_guardar_imagen()
            print("imagen guardada con f1")
        else:
            super().keyPressEvent(event)

    def id_registro(self):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()
            cursor.execute("SELECT ejecucion_id FROM registros ORDER BY ejecucion_id DESC LIMIT 1")
            resultado = cursor.fetchone()
            return resultado[0]
        except Exception as e:
            print(f"Error: {e}")
            msg = (f"Ha ocurrido un error: {e}")
            self.ventana_emergente(msg)
            pass
        pass

    def funcion_iniciar(self):
        pass

    # -----funcion principal ------------------------------------
    def funcion_guardar_imagen(self):
        id_fk = self.id_registro()
        caso = ""
        foto = self.funcion_capturar()

        if foto:
            bArray = QByteArray()
            buff = QBuffer(bArray)
            buff.open(QIODevice.WriteOnly)
            foto.save(buff, "PNG")

        try:
            cursor = self.conexion.cursor()
            cursor.execute("INSERT INTO evidencias(ejecucion_id, caso, evidencia) VALUES (?, ?, ?)", (id_fk, caso, bArray))
            self.conexion.commit()
            cursor.close()
            print("foto guardada")
            pass
        except Exception as e:
            print(f"Error: {e}")
            msg = (f"Ha ocurrido un error: {e}")
            self.ventana_emergente(msg)
            pass
        pass

    def funcion_capturar(self):
        # captura la pantalla y convierte la imagen en un QPixmap
        screen = QScreen.grabWindow(QApplication.primaryScreen(), 0)
        # screen =  ImageGrab.grab()
        pixmap = QPixmap(screen)
        return pixmap

    def funcion_terminar(self):
        msg = "Ejecucion finalizada"
        self.ventana_emergente(msg)
        self.main = consult.Consutar()
        self.main.show()
        self.close()
        pass

    def eliminar_preregistro(self):
        try:
            # Crear un cursor
            cursor = self.conexion.cursor()
            # Eliminar el último registro
            cursor.execute("DELETE FROM registros WHERE ejecucion_id = ?", (self.id_registro(),))
            self.conexion.commit()
            cursor.close()
            print("se elimino el ultimo registro")
            pass
        except Exception as e:
            print(f"Error: {e}")
            msg = (f"Ha ocurrido un error: {e}")
            self.ventana_emergente(msg)
            pass
        pass

    #popup
    def ventana_emergente(self, mensaje):
        popup = QMessageBox()
        popup.setWindowTitle("Aviso!")
        popup.setText(mensaje)
        popup.setIcon(QMessageBox.Information)
        popup.exec_()
        pass

    def funcion_cancelar(self):
        self.eliminar_preregistro()
        self.main = main.TestKeep()
        self.main.show()
        self.close()


