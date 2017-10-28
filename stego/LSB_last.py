from PIL import Image
#fg = Image.open('pexels-photo-110854.jpeg') # IMAGE NAME TO BE ANALIZED, PLEASE STORE IT IN THE SAME FOLDER THAN THE SCRIPT
fg = Image.open('pexels-photo-110854.jpeg') # IMAGE NAME TO BE ANALIZED, PLEASE STORE IT IN THE SAME FOLDER THAN THE SCRIPT
dimensions = fg.size # TUPLE WITH (width, height) OF THE IMAGE
rowString1 = ""
text = ""
for row in range(dimensions[1]):
    for col in range(dimensions[0]):
        fgpix = fg.getpixel((col,row)) # CREATES A TUPLE (1,3) WITH A BYTE PER POSITION CORRESPONDING TO THE PIXEL
        #for i in range(3)[::-1]:
        for i in range(3):
            fgvalue = bin(fgpix[i])[-1:]
            rowString1 += fgvalue
for i in range(0, len(rowString1), 8):
    if 32 < int(rowString1[i:i+8], 2) < 126:
        text += chr(int(rowString1[i:i+8], 2))
    else:
        text += "."
print(text)
