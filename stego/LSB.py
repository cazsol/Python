from PIL import Image
fg = Image.open('logo-1.png') # IMAGE NAME TO BE ANALIZED, PLEASE STORE IT IN THE SAME FOLDER THAN THE SCRIPT
dimensions = fg.size # TUPLE WITH (width, height) OF THE IMAGE
newIm = Image.new("RGB", dimensions,"white") # NEW IMAGE ALL WHITE WITH RGB PROPERTIES AND DIMENSIONS OF THE ANALYZED IMAGE
fg_rgb = fg.convert('RGB') # CREATES AN IMAGE IN RGB FROM THE ORIGINAL IMAGE
i = 0 # CREATES COUNTER
# CREATES A LOOP TO GO THROUGH ALL THE PIXELS OF THE IMAGE
for row in range(dimensions[1]):
    for col in range(dimensions[0]):
        fgpix = fg.getpixel((col,row)) # CREATES A TUPLE (1,3) WITH A BYTE PER POSITION CORRESPONDING TO THE PIXEL
        fg1 = fgpix[0] # BYTE CORRESPONDING TO R
        fg2 = fgpix[1] # BYTE CORRESPONDING TO G
        fg3 = fgpix[2] # BYTE CORRESPONDING TO B
        fgr = fg1 + fg2 + fg3 # SUMS THE INFORMATION OF THE THREE POSITIONS FOR ANALYSIS
        if fg2 <= 1 and fg1 <= 1 and fg3 <=1: # if there is some sign of least bit
            newIm.putpixel((col,row),(255,255,255)) # puts a white pixel
        else:
            newIm.putpixel((col,row),(0,0,0))
        # INCREASES THE COUNTER FOR INDICATIONS OF LSB USED FOR STORING INFORMATION
        if (fgr == 764 or fgr == 1):
            i += 1
        else:
            continue
if i != 0:
    print("Possible least significant bit." + str(i)+ " instances found.")
newIm.show()
win = image.ImageWin(dimensions[1],dimensions[0])
newIm.draw(win)
win.exitonclick()
