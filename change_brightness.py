from PIL import Image, ImageEnhance

#read the image
im = Image.open("cedulas_test/barcode6.png")

#image brightness enhancer
enhancer = ImageEnhance.Brightness(im)

factor = 1.5
im_output = enhancer.enhance(factor)
im_output.save('cedulas_test/brightened-image.png')