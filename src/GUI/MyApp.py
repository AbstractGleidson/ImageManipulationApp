# Cria de fato a interface da aplicacao
from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QListWidget, QListWidgetItem, QVBoxLayout, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from .smallWidgets import buttonMainMenu,messageDialog
from imageManipulation.imagen import Image
from .constants import ICON2_PATH, WINDOW_HEIGTH, WINDOW_WIDTH
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
        self.selectedImage = None
  
  
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
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Campo de entrada da URL
        self.inputUrl = QLineEdit()
        self.inputUrl.setPlaceholderText("Digite a URL da imagem (.jpg ou .png)")
        layout.addWidget(self.inputUrl)

        # Botão para baixar/importar
        btnImportar = buttonMainMenu("Importar imagem")
        btnImportar.clicked.connect(self.importarURL)
        layout.addWidget(btnImportar)

        # Botão voltar
        btnVoltar = buttonMainMenu("Voltar")
        btnVoltar.clicked.connect(self.showMainMenu)
        layout.addWidget(btnVoltar)

        self.setCentralWidget(widget)

    def importarURL(self):
        url = self.inputUrl.text().strip()

        if not url:
            QMessageBox.warning(self, "Aviso", "Digite uma URL primeiro.")
            return

        try:
            downloader = Download()
            destino = downloader.getImagem(url, "assets/Imagens")
            self.selectedImage = destino
            QMessageBox.information(
                self,
                "Sucesso",
                f"Imagem baixada e salva em:\n{destino}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível baixar a imagem:\n{str(e)}"
            )

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
        if not self.selectedImage:
            messageDialog(self, "ERRO", "Selecione uma imagem primeiro!")
            return
        CENTER = Qt.AlignmentFlag.AlignCenter
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_cinza = buttonMainMenu("Escala de Cinza")
        button_cinza.clicked.connect(
            lambda: self.atribuição_imagem("imageGrayScale", "Escala de Cinza")
        )
        
        button_preto_branco = buttonMainMenu("Preto e Branco")
        button_preto_branco.clicked.connect(
            lambda: self.atribuição_imagem("binaryImage", "Preto e Branco")
        )
        
        button_cartoon = buttonMainMenu("Cartoon")
        button_cartoon.clicked.connect(
            lambda: self.atribuição_imagem("cartoonImage", "Cartoon")
        )
        
        button_negativo = buttonMainMenu("Foto Negativa")
        button_negativo.clicked.connect(
            lambda: self.atribuição_imagem("negativeImage", "Foto Negativa")
        )
        
        button_contorno = buttonMainMenu("Contorno")            # Botão filtro contorno
        button_contorno.clicked.connect(
            lambda: self.atribuição_imagem("...","Contorno")
        )

        button_blurred = buttonMainMenu("Borrado")              # Botão filtro borrado
        button_blurred.clicked.connect(
            lambda: self.atribuição_imagem("...","Borrado")
        )

        button_voltar = buttonMainMenu("Voltar ao Menu")        # Botão menu
        button_voltar.clicked.connect(self.showMainMenu)
        
        layout.addWidget(button_cinza, alignment=CENTER)
        layout.addWidget(button_preto_branco, alignment=CENTER)
        layout.addWidget(button_cartoon, alignment=CENTER)
        layout.addWidget(button_negativo, alignment=CENTER)
        layout.addWidget(button_contorno, alignment=CENTER)
        layout.addWidget(button_blurred, alignment=CENTER)
        layout.addWidget(button_voltar, alignment=CENTER)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        pass

    def atribuição_imagem(self, nome_metodo: str, nome_filtro: str):
        try:
            
            imagem_obj = Image(self.selectedImage)
                       
            metodo = getattr(imagem_obj, nome_metodo)
                        
            resultado = metodo()
                        
            messageDialog(
                self,
                f"SUCESSO - {nome_filtro}",
                f"Filtro {nome_filtro} aplicado com sucesso!\n\n{resultado}"
            )
            
            self.showMainMenu()
        except Exception as e:
            messageDialog(
                self,
                "ERRO",
                f"Nao foi possivel aplicar o filtro {nome_filtro}:\n{str(e)}",
                icon=QMessageBox.Icon.Critical
            )
            self.showMainMenu()
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
