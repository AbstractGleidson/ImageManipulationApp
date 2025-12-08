from imagen import Image
import cv2 as openCv

if __name__ == "__main__":
    img = Image(".vasoco.flamengo.it.jpg")
    
    image = img.cartooImage()
    
    openCv.imshow("Imagem em escala de cinza", image)
    openCv.waitKey(0)
    openCv.destroyAllWindows()