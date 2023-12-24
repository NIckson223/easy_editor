from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

with Image.open('original.jpeg') as pic_original:
    print("Розмір картинки", pic_original.size)
    print("Формат картинки", pic_original.format)
    print("Тип картинки", pic_original.mode)
    #pic_original.show()

    pic_gray =  pic_original.convert('L')
    pic_gray.save('bw.jpeg')
    #pic_gray.show()

    pic_blured = pic_original.filter(ImageFilter.BLUR)
    pic_blured.save('blured.jpeg')
    #pic_blured.show()

    pic_mirrow = pic_original.transpose(Image.FLIP_LEFT_RIGHT)
    pic_mirrow.save('mirrowed.jpeg')
    #pic_mirrow.show()

    pic_left = pic_original.transpose(Image.ROTATE_90)
    pic_left.save('left.jpeg')
    #pic_left.show()

    pic_contrast = ImageEnhance.Contrast(pic_original)
    pic_contrast = pic_contrast.enhance(1.5)
    pic_contrast.show()