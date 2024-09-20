import os
import sys
import struct

from PIL import Image


def getFileNameWithoutExtension(path):
    return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

def bip2png(file, saveDir='.'):
    fl = open(file, 'rb')
    filename = getFileNameWithoutExtension(file)
    fl.seek(0x88)
    width, = struct.unpack('<H', fl.read(2))
    height, = struct.unpack('<H', fl.read(2))
    r = 64
    t_w = (width + (r - 2) - 1) // (r - 2)
    dwidth = t_w * r
    t_h = (height + (r - 2) - 1) // (r - 2)
    dheight = t_h * r
    
    fl.seek(0x100)
    # img = Image.new('RGBA', (width, height))
    tmpimg1 = Image.new('RGBA', (dwidth, dheight))
    for t_y in range(t_h):
        for t_x in range(t_w):
            for y in range(r):
                for x in range(r):
                    color = fl.read(4)
                    tmpimg1.putpixel((x + t_x * r, y + t_y * r), (color[0], color[1], color[2], 0xFF))
    
    fl.close()
    tmpimg1.save(filename + '_f1.png', 'png')
    
    img = Image.new('RGBA', (width, height))
    for y in range(dheight):
        for x in range(dwidth):
            # tmppixel = tmpimg1.getpixel((x, y))
            if x % 64 in {0, 63} or y % 64 in {0, 63}:
                continue
            x2 = (x // 64) * 62 + (x % 64) - 1
            y2 = (y // 64) * 62 + (y % 64) - 1
            if x2 >= width or y2 >= height:
                continue
            img.putpixel((x2, y2), tmpimg1.getpixel((x, y)))
            
    img.save(filename + '.png', 'png')
    
    print("bin2png: '" + file + "' convert png success! Save as '" + filename + '.png' + "'")

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit()
    files=[]
    files=sys.argv[1:]
    for file in files:
        bip2png(file, '.')