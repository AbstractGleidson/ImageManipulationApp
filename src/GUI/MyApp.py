# Cria de fato a interface da aplicacao
from PySide6.QtWidgets import QMainWindow, QWidget, QMessageBox, QInputDialog, QListWidget
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from .smallWidgets import buttonMainMenu
from GUI.constants import ICON2_PATH, WINDOW_HEIGTH, WINDOW_WIDTH
import sys

  
# Herda QMainWindow para ter acesso a alguns componentes da janela em si, como title e icon 
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ManipulApp")
        self.setFixedSize(WINDOW_HEIGTH, WINDOW_WIDTH)
        self.setWindowIcon(QIcon(ICON2_PATH)) # Troca o icone da janela
        self.showMainMenu()  # Mostra a primeira janela
  
  
    # Renderiza o menu principal da aplicacao 
    def showMainMenu(self):
        CENTER = Qt.AlignmentFlag.AlignCenter # Cria um centralizacao 
  
        widget = QWidget() # Widget generico
        layout = QVBoxLayout() # Box vertical 
  
        # Seleciona uma imagem pro Programa
        button_select_image = buttonMainMenu("Selecionar Imagem")
        button_select_image.clicked.connect(self.selectImage) # Adiciona funcao para esse botao

        button_apply_filter = buttonMainMenu("Aplicar Filtros")
        button_apply_filter.clicked.connect(self.applyFilter) # Adiciona funcao para esse botao

        # Mostra as imagens disponíveis para a manipulação
        button_list_images = buttonMainMenu("Listar Imagens")
        button_list_images.clicked.connect(self.listIMages) # Adiciona funcao para esse botao
        
        # Sai da aplicacao
        button_exit = buttonMainMenu("Sair")
        button_exit.clicked.connect(self.exitAplication) # Adiciona funcao para esse botao
  
        # Adiciona os botoes no layout
        layout.addWidget(button_select_image, alignment=CENTER)
        layout.addWidget(button_apply_filter, alignment=CENTER)
        layout.addWidget(button_list_images, alignment=CENTER)
        layout.addWidget(button_exit, alignment=CENTER)
        widget.setLayout(layout) # Adiciona o layout no widget generico
  
        self.setCentralWidget(widget)  # Renderiza esse widget generico que foi criado 
    
    def selectImage(self):
        pass
    def listIMages(self):
        pass
    def applyFilter(self):
        pass
    # Sai da aplicacao
    def exitAplication(self):
        sys.exit()