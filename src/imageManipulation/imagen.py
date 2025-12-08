import cv2 as openCv  
import numpy
from pathlib import Path
import os
from InvalidFormatImage import InvalidFormatImage
from saveImageError import SaveImageError

class Image:
    def __init__(self, image_path):
        
        # Verifica se o formato da imagem é adequado
        if not self.validationFormat(image_path):
            raise InvalidFormatImage("A imagem deve ser .jpg ou .png") 
        
        # Faz a leitura da imagem
        data = openCv.imread(str(image_path))
        
        # Verifica se foi possivel carregar a imagem
        if data is None:
            raise FileNotFoundError("Não foi possivel carregar a imagem!")
        else:
            self.imagem_data = numpy.array(data) # Converte para um numpy array
        
        # Nome da imagem
        self.nameImage = os.path.basename(image_path)
        self.BASEPAHT = Path(__file__).parent.parent.parent / "assets" / "Imagens" # Local para salvar os resultados dos filtros
        
    def imageGrayScale(self):
        """
        Aplica filtro cinza na imagem e salva o resultado
        Returns:
            str: local onde foi salvo o resultado.
        """
        
        grayImage = openCv.cvtColor(self.imagem_data, openCv.COLOR_BGR2GRAY) # Converte a imagem pra escala de cinza 
            
        # Salva imagem
        return self.saveImage(grayImage, "gray")
        
    def _imageGrayScale(self):
        """Retorna o numpy array da imagem em escala de cinza"""
        grayImage = openCv.cvtColor(self.imagem_data, openCv.COLOR_BGR2GRAY) # Converte a imagem pra escala de cinza 
    
        return numpy.array(grayImage)
    
    def binaryImage(self):
        """
        Aplica filtro binario na imagem e salva resultado.
        Returns:
            str: local onde foi salvo o resultado. 
        """
        
        # Convete para escala de cinza
        gray_image = self._imageGrayScale()
        
        # Convete para binario 
        binary_image = numpy.array(gray_image > 128).astype("uint8")
        
        # Faz uma nova quantização
        binary_image *= 255
        
        return self.saveImage(binary_image, "binary")
    
    def negativeImage(self):
        """
        Aplica filtro negativo na imagem e salva o resultado.
        Returns:
            str: local onde foi salvo o resultado. 
        """
        
        negative_image = -self.imagem_data
        
        return self.saveImage(negative_image, "negative")
    
    def cartoonImage(self):
        """
        Aplica filtro cartoon na imagem e salva o resultado.
        Returns:
            str: local onde foi salvo o resultado. 
        """
        
        gray_image = self._imageGrayScale()
        
        edges = openCv.adaptiveThreshold(
            gray_image, 
            255, 
            openCv.ADAPTIVE_THRESH_MEAN_C, 
            openCv.THRESH_BINARY, 
            9, 
            9
        )
         
        color = openCv.bilateralFilter(self.imagem_data, 9, 200, 200)
        
        cartoon = openCv.bitwise_and(color, color, mask = edges)
        
        return self.saveImage(cartoon, "cartoon")
    
    def validationFormat(self, path_image: str):
        """
        Verifica o formato da imagem e retorna se é um formato valido
        Args:
            path_image (str): caminho da imagem que deve ser validada.

        Returns:
            bool: valor booleano que indica se a imagem é valida 
        """
        
        extension = str(path_image).split(".")[-1]
        
        return (extension == "jpg" or extension == "png")
    
    def saveImage(self, image, filter: str):
        """
        Salva imagem no diretório padrão assets/Imagens.
        Args:
            image (numpy array): Matriz que representa a imagem.
            filter (str): filtro aplicado sobre a imagem.

        Raises:
            SaveImageError: Erro ao salvar imagem.

        Returns:
            str: Caminho onde a imagem foi salva.
        """
        
        imageName = f"{filter}_{self.nameImage}"
        savePath = str(self.BASEPAHT / imageName)
        
        if openCv.imwrite(savePath, image):
            return f"Imagem salva em: {savePath}"
        else:
            raise SaveImageError("Não foi possivel salvar a imagem!") 

# if __name__ == "__main__":
    
#     p = Path(__file__).parent.parent.parent / "assets" / "Imagens" / "image.jpg"
     
#     image = Image(p)

#     image.cartoonImage()    