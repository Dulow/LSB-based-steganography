from PIL import Image

def jpgTopng(img):
    img.save('heart.png')

if __name__ == '__main__':
    img = Image.open('heart.jpg')
    jpgTopng(img)
