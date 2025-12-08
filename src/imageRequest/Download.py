import os
import urllib.request
import shutil

class Download:
    def __init__(self):
        self.formatosValidos = (".jpg", ".png")

    #Recebe uma string de caminho que indica uma imagem. Caso seja uma url, realiza um download 
    #para o destino, senão copia da origem para o destino. Por padrão, o destino é a pasta imagens que vai
    #na estrutura da aplicação
    def getImagem(self, caminho, destino = "../../assets/Imagens"):

        if self.ehUrl(caminho):
            return self.internet(caminho, destino)
        else:
            return self.local(caminho, destino)

    #Retorna um true caso a string passada seja uma url
    def ehUrl(self, caminho):
        return caminho.startswith(("http://", "https://"))

    #Retorna uma mensagem de erro caso não possua a extensão correta
    def validaExtensao(self, nome):
        if not nome.lower().endswith(self.formatosValidos):
            raise ValueError("Formato inválido. Use apenas arquivos .jpg ou .png.")

    #Realiza o download da imagem passada para a pasta destino
    def internet(self, url, destino):

        self.validaExtensao(url)

        nome_arquivo = url.split("/")[-1]
        destino_final = os.path.join(destino, nome_arquivo)

        try:
            urllib.request.urlretrieve(url, destino_final)
            return destino_final

        except Exception as e:
            raise RuntimeError(f"Erro ao baixar imagem: {e}")

    #Copia o arquivo local passado para o destino
    def local(self, caminho, destino):
        
        if not os.path.exists(caminho):
            raise FileNotFoundError("Arquivo local não encontrado.")

        self.validaExtensao(caminho)

        nome_arquivo = os.path.basename(caminho)
        destino_final = os.path.join(destino, nome_arquivo)

        shutil.copy(caminho, destino_final)

        return destino_final
    
down = Download()
print(down.getImagem("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"))
