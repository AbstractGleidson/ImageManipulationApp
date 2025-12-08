import cv2 as openCv  
import numpy
from pathlib import Path

class InvalidFormatImage(Exception):
    pass
 
class Image:
    def __init__(self, image_path):
        if not self.validationFormat(image_path):
            raise InvalidFormatImage("A imagem deve ser .jpg ou .png") 
        
        self.imagem_data = numpy.array(openCv.imread(image_path))
        self.BASEPAHT = Path(__file__).parent.parent / "assets" / "Image"
        
    def imageGrayScale(self):
        grayImage = openCv.cvtColor(self.imagem_data, openCv.COLOR_BGR2GRAY) # Converte a imagem pra escala de cinza 
            
        return numpy.array(grayImage)
    
    def binaryImage(self):
        
        # Convete para escala de cinza
        gray_image = self.imageGrayScale()
        
        # Convete para binario 
        binary_image = numpy.array(gray_image > 128).astype("uint8")
        
        # Faz uma nova quantização
        binary_image *= 255
        
        return binary_image
    
    def negativeImage(self):
        return -self.imagem_data
    
    def cartooImage(self):
        
        gray_image = self.imageGrayScale()
        
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
        
        return cartoon
    
    def validationFormat(self, path_image: str):
        extension = path_image.split(".")[-1]
        
        return (extension == "jpg" or extension == "png")