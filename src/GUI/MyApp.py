# Cria de fato a interface da aplicacao
from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QListWidget, QListWidgetItem, QVBoxLayout, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from .smallWidgets import buttonMainMenu,messageDialog
from imageManipulation.imagen import Image
from .constants import ICON2_PATH, WINDOW_HEIGTH, WINDOW_WIDTH
from imageRequest.Download import Download
from pathlib import Path
from urllib.parse import urlparse
import os
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

       
       # Mostra as imagens disponíveis para a manipulação
        button_list_images = buttonMainMenu("Listar Imagens")
        button_list_images.clicked.connect(self.listImages) # Adiciona funcao para esse botao
        
        # Sai da aplicacao
        button_exit = buttonMainMenu("Sair")
        button_exit.clicked.connect(self.exitAplication) # Adiciona funcao para esse botao
  
        # Adiciona os botoes no layout
        layout.addWidget(button_select_image, alignment=CENTER)
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

        botao_editar = buttonMainMenu("Editar")
        botao_editar.clicked.connect(self._editar_imagem)

        # Botão voltar
        btnVoltar = buttonMainMenu("Voltar")
        btnVoltar.clicked.connect(self.showMainMenu)
        layout.addWidget(btnVoltar)
        layout.addWidget(botao_editar)

        self.setCentralWidget(widget)

    def importarURL(self):
        url = self.inputUrl.text().strip()

        if not url:
            QMessageBox.warning(self, "Aviso", "Digite uma URL primeiro.")
            return

        try:
            downloader = Download()
            destino = downloader.getImagem(url, str(Path(__file__).parent.parent.parent / Path("assets/Imagens")))
            self.selectedImage = str(destino)
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

    def listImages(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Criar lista de imagens
        self.listaImagens = QListWidget()
        self.listaImagens.setSelectionMode(QListWidget.SelectionMode.SingleSelection)  # permitir selecionar 1 imagem
        self.listaImagens.setViewMode(QListWidget.ViewMode.IconMode)
        self.listaImagens.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.listaImagens.setIconSize(QSize(128, 128))
        self.listaImagens.setSpacing(10)
        self.listaImagens.itemClicked.connect(self._on_item_clicked)

        botao_voltar = buttonMainMenu("Voltar")
        botao_voltar.clicked.connect(self.showMainMenu)
        botao_editar = buttonMainMenu("Editar")
        botao_editar.clicked.connect(self._editar_imagem)

        layout.addWidget(self.listaImagens)
        layout.addWidget(botao_voltar)
        layout.addWidget(botao_editar)

        self.setCentralWidget(widget)

        # Carregar imagens do diretório
        self._carregar_imagens()

    def _on_item_clicked(self, item: QListWidgetItem):
        """Atualiza selectedImage para o caminho da imagem quando o usuário clica na lista."""
        if item is None:
            self.selectedImage = None
        else:
            caminho = item.data(32)
            self.selectedImage = str(caminho)
        
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
            lambda: self.atribuição_imagem("contourImage","Contorno")
        )

        button_blurred = buttonMainMenu("Borrado")              # Botão filtro borrado
        button_blurred.clicked.connect(
            lambda: self.atribuição_imagem("blurredImage","Borrado")
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
            
    def _carregar_imagens(self):
        diretorio = Path(__file__).parent.parent.parent / Path("assets/Imagens")
        extensoes = [".jpg", ".png"]

        self.listaImagens.clear()

        for arquivo in diretorio.iterdir():
            if arquivo.suffix.lower() in extensoes:
                pixmap = QPixmap(str(arquivo)).scaled(128, 128)
                nome = self.nome_resumido(arquivo.name)
                item = QListWidgetItem(QIcon(pixmap), nome)
                item.setData(32, str(arquivo))
                self.listaImagens.addItem(item)

        if self.listaImagens.count() > 0:
            item = self.listaImagens.item(0)
            self.listaImagens.setCurrentItem(item)
            self.selectedImage = item.data(32)


    def nome_resumido(self, url, max_len=35):
        # pega apenas o nome do arquivo
        nome = os.path.basename(urlparse(url).path)
        # se ainda for grande, trunca
        if len(nome) > max_len:
            return nome[:20] + "..." + nome[-10:]
        return nome

    def _editar_imagem(self):
        item = None

        if hasattr(self, "listaImagens"):
            item = self.listaImagens.currentItem()

        if item is None:
            if not self.selectedImage:
                QMessageBox.warning(self, "Nenhuma imagem", "Selecione uma imagem para editar.")
                return
        else:
            self.selectedImage = str(item.data(32))

        self.applyFilter()


    # Sai da aplicacao
    def exitAplication(self):
        sys.exit()
