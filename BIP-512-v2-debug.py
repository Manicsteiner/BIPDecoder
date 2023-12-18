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
    dx = 512
    dy = 16
    dwidth = ((width + (dy - 2) - 1) // (dy - 2)) * dy
    dheight = ((height + (dy - 2) - 1) // (dy - 2)) * dy
    focus_H = (dwidth * dheight + dx - 1) // dx
    focus_T = (focus_H + dy - 1) // dy
    if (focus_T > focus_H // dy):
        focus_H += dy
        focus_T = focus_H // dy

    fl.seek(0x100)
    # img = Image.new('RGBA', (width, height))
    tmpimg1 = Image.new('RGBA', (dx, focus_H))
    for t in range(focus_T):
        for y in range(dy):
            for x in range(dx):
                color = fl.read(4)
                tmpimg1.putpixel((x, y + t * dy), (color[0], color[1], color[2], 0xFF))

    fl.close()
    tmpimg1.save(filename + '_f1.png', 'png')
    
    num_bars = (focus_H + dy - 1) // dy
    
    tmpimg2 = Image.new('RGBA', (num_bars * dx, dy))
    for i in range(num_bars):
        bar = tmpimg1.crop((0, i * dy, dx, (i + 1) * dy))
        tmpimg2.paste(bar, (i * dx, 0))
    tmpimg2.save(filename + '_f2.png', 'png')
    
    num_new_bars = (num_bars * dx + dwidth - 1) // dwidth
    new_bar_width = dwidth
    tmpimg3 = Image.new('RGBA', (dwidth, dheight // dy * (dy - 2)))
    for i in range(num_new_bars):
        cutx = (i + 1) * new_bar_width
        if (cutx > num_bars * dx):
            cutx = num_bars * dx
        new_bar = tmpimg2.crop((i * new_bar_width, 0, cutx, dy))
        tmpimg3.paste(new_bar, (0, i * (dy - 2)))
    tmpimg3.save(filename + '_f3.png', 'png')
    
    tmpimg4 = Image.new('RGBA', (dwidth // dy * (dy - 2), dheight // dy * (dy - 2)))
    num_final_bars = dwidth // dy
    for i in range(num_final_bars):
        final_bar = tmpimg3.crop((i * dy, 0, (i + 1) * dy, dheight // dy * (dy - 2)))
        tmpimg4.paste(final_bar, (i * (dy - 2), 0))
    tmpimg4.save(filename + '_f4.png', 'png')
    
    finalimg = Image.new('RGBA', (width, height))
    f2cut = tmpimg4.crop((0, 0, width, height))
    finalimg.paste(f2cut, (0, 0))
    finalimg.save(filename + '.png', 'png')
    print("bin2png: '" + file + "' convert png success! Save as '" + filename + '.png' + "'")

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit()
    files=[]
    files=sys.argv[1:]
    for file in files:
        bip2png(file, '.')