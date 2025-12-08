# Cria de fato a interface da aplicacao
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QListWidget, QListWidgetItem, QVBoxLayout, QListView
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from .smallWidgets import buttonMainMenu
from GUI.constants import ICON2_PATH, WINDOW_HEIGTH, WINDOW_WIDTH
from imageRequest.Download import Download
from pathlib import Path
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
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Criar lista de imagens
        self.listaImagens = QListWidget()
        self.listaImagens.setViewMode(QListWidget.ViewMode.IconMode)
        self.listaImagens.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.listaImagens.setIconSize(QSize(128, 128))
        self.listaImagens.setSpacing(10)
        botao_voltar = buttonMainMenu("Voltar")
        botao_voltar.clicked.connect(self.showMainMenu)


        layout.addWidget(self.listaImagens)
        layout.addWidget(botao_voltar)

        self.setCentralWidget(widget)

        # Carregar imagens do diretório
        self.carregar_imagens()
    def applyFilter(self):
        pass
    def carregar_imagens(self):
        diretorio = Path("assets/Imagens")
        extensoes = [".jpg", ".jpeg", ".png"]

        self.listaImagens.clear()

        for arquivo in diretorio.iterdir():
            if arquivo.suffix.lower() in extensoes:

                pixmap = QPixmap(str(arquivo)).scaled(128, 128)
                icon = QIcon(pixmap)

                item = QListWidgetItem(icon, arquivo.name)
                item.setData(32, str(arquivo))  # guarda o caminho completo

                self.listaImagens.addItem(item)

    # Sai da aplicacao
    def exitAplication(self):
        sys.exit()