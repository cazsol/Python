from PIL import Image
fg = Image.open('logo-1.png')
tamano = fg.size # tuple with (width, height)
newIm = Image.new("RGB", tamano,"white")
fg_rgb = fg.convert('RGB')
new = []
for row in range(tamano[1]):
    for col in range(tamano[0]):
        fgpix = fg.getpixel((col,row))
        fg1 = fgpix[0]
        fg2 = fgpix[1]
        fg3 = fgpix[2]
        fgr = fg1 + fg2 + fg3
        if fg2 <= 1 and fg1 <= 1 and fg3 <=1: # if there is some sign of least bit
        #if (fg1 != fg2) and (fg2 == fg3): # if colors are the same
            #newPix = image.Pixel(255,255,255)
            newIm.putpixel((col,row),(255,255,255)) # puts a white pixel
            #if row == 499:
            #    new.append()
        else:
            newIm.putpixel((col,row),(0,0,0))
        #newIm.putpixel(col,row,newPix)
newIm.show()
win = image.ImageWin(500,500)
newIm.draw(win)
win.exitonclick()
