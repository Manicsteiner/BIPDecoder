import os
import sys
import struct

from PIL import Image


def getFileNameWithoutExtension(path):
    return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

def bip2png(file, saveDir='.'):
    fl = open(file, 'rb')
    filename = getFileNameWithoutExtension(file)
    fl.seek(0x14)
    sign, = struct.unpack('>I', fl.read(4))
    dx = 0
    dy = 0
    sliced = True
    if (sign == 0x00011700):
        dx = 512
        dy = 16
    elif (sign == 0x00011600):
        dx = 1024
        dy = 32
    elif (sign == 0x00011300):
        sliced = False
        # print("480direct")
        dx = 512
        dy = 16
    else:
        print("Unknown format")
        return
    fl.seek(0x88)
    width, = struct.unpack('<H', fl.read(2))
    height, = struct.unpack('<H', fl.read(2))
    finalimg = Image.new('RGBA', (width, height))
    fl.seek(0x100)

    if (sliced):
        dwidth = ((width + (dy - 2) - 1) // (dy - 2)) * dy
        dheight = ((height + (dy - 2) - 1) // (dy - 2)) * dy
        focus_H = (dwidth * dheight + dx - 1) // dx
        focus_T = (focus_H + dy - 1) // dy

        for t in range(focus_T):
            for y in range(dy):
                for x in range(dx):
                    color = fl.read(4)
                    i2x = x + t * dx
                    i3t = i2x // dwidth
                    i3x = i2x - i3t * dwidth
                    i3y = i3t * (dy - 2) + y
                    i4x = i3x - i3x // dy * dy + i3x // dy * (dy - 2)

                    if (i3x >= dwidth or i4x >= width or i3y >= height):
                        continue
                    finalimg.putpixel((i4x, i3y), (color[0], color[1], color[2], 0xFF))
    else:
        focus_H = (width * height + dx - 1) // dx
        focus_T = (focus_H + dy - 1) // dy
        for t in range(focus_T):
            for y in range(dy):
                for x in range(dx):
                    color = fl.read(4)
                    i2x = x + t * dx
                    i3t = i2x // width
                    i3x = i2x - i3t * width
                    i3y = i3t * dy + y
                    if (i3x >= width or i3y >= height):
                        continue
                    finalimg.putpixel((i3x, i3y), (color[0], color[1], color[2], 0xFF))
    
    fl.close()
    
    finalimg.save(filename + '.png', 'png')
    print("bin2png: '" + file + "' convert png success! Save as '" + filename + '.png' + "'")

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit()
    files=[]
    files=sys.argv[1:]
    for file in files:
        bip2png(file, '.')