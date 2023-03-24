from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
import newt
import consult


class TestKeep(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # cargar el diseño
        uic.loadUi('sources/main.ui', self)

        # Cargar imagen en un objeto QPixmap
        pixmap = QPixmap('sources/logo_exp.png')

        # Ajustar tamaño de la imagen de ser necesario
        #pixmap = pixmap.scaledToWidth(200)
        self.lbl_logo.setPixmap(pixmap)

        # conecta los botones a sus correspondientes funciones
        self.btn_new.clicked.connect(self.abrir_ventana_nuevo)
        self.btn_consult.clicked.connect(self.abrir_ventana_consultar)
        self.btn_exit.clicked.connect(self.funcion_exit)

    def abrir_ventana_nuevo(self):
        self.nuevo = newt.Nuevor()    # Crea una instancia de la clase "Nuevor" definida en el archivo "newt.py"
        self.nuevo.show()    # Muestra la ventana de la instancia "nuevo" y la hace visible
        self.hide()    # Oculta la ventana principal
        print("fue a nuevo")
        pass

    #realiza la misma funcion de ventana nuevo pero esta vez hacia la ventana consultar
    def abrir_ventana_consultar(self):
        self.nuevo = consult.Consutar()
        self.nuevo.show()
        self.hide()
        print("fue a nuevo")
        pass

    def funcion_exit(self):
        # Llamamos a la función para cerrar la aplicación
        QApplication.quit()
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = TestKeep()
    window.show()
    app.exec_()