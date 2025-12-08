import cv2 as openCv  
import numpy
from pathlib import Path
import os

class InvalidFormatImage(Exception):
    pass

class SaveImageError(Exception):
    pass
 
class Image:
    def __init__(self, image_path):
        if not self.validationFormat(image_path):
            raise InvalidFormatImage("A imagem deve ser .jpg ou .png") 
        
        data = openCv.imread(str(image_path))
        
        if data is None:
            raise FileNotFoundError("Não foi possivel carregar a imagem!")
        else:
            self.imagem_data = numpy.array(data)
        
        self.nameImage = os.path.basename(image_path)
        self.BASEPAHT = Path(__file__).parent.parent.parent / "assets" / "Imagens"
        
    def imageGrayScale(self):
        grayImage = openCv.cvtColor(self.imagem_data, openCv.COLOR_BGR2GRAY) # Converte a imagem pra escala de cinza 
            
        self.saveImage(grayImage, "gray")
        
    def _imageGrayScale(self):
        grayImage = openCv.cvtColor(self.imagem_data, openCv.COLOR_BGR2GRAY) # Converte a imagem pra escala de cinza 
    
        return numpy.array(grayImage)
    
    def binaryImage(self):
        
        # Convete para escala de cinza
        gray_image = self._imageGrayScale()
        
        # Convete para binario 
        binary_image = numpy.array(gray_image > 128).astype("uint8")
        
        # Faz uma nova quantização
        binary_image *= 255
        
        self.saveImage(binary_image, "binary")
    
    def negativeImage(self):
        
        negative_image = -self.imagem_data
        
        self.saveImage(negative_image, "negative")
    
    def cartoonImage(self):
        
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
        
        self.saveImage(cartoon, "cartoon")
    
    def validationFormat(self, path_image: str):
        extension = str(path_image).split(".")[-1]
        
        return (extension == "jpg" or extension == "png")
    
    def saveImage(self, image, filter: str):
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