from PIL import Image
import numpy as np
import os
import sys

class FontLoader :
    def __SplitFile__(this, filename):
        image = Image.open(filename, mode="r")
        letters = []
        if not os.path.isdir('./letters/'):
            os.mkdir('./letters/')
            os.mkdir('./letters/' + filename[:-4] + '/')
        if not os.path.isdir('./letters/' + filename[:-4] + '/'):
            os.mkdir('./letters/' + filename[:-4] + '/')

        for y in range(0, image.height,16):
            for x in range(0, image.width,16):
                sq = image.crop((x,y, x+16, y+16))
                letters.append(sq)
                sq.save('./letters/{}/letter_{}_{}.png'.format(filename[:-4], int(x/16), int(y/16)))

    def __LoadLib__(this, filename):
        this.fonts = []
        namegen = (file for __, __, file in os.walk('./letters/' + filename[:-4] + '/'))
        path = './letters/' + filename[:-4] + '/'
        for names in namegen:
            for file in names:
                if os.path.isfile(path + file):
                    this.fonts.append(Image.open(fp='./letters/' + filename[:-4] + '/' + file).convert('1'))

    def GetAvgBrightness(this, img):
        avg = 0
        pixels = img.load()
        for y in range(16):
            for x in range(16):
                avg += pixels[x,y]
        return avg / 256

    def GetLowestBrightness(this):
        lowest = 999999999
        lowestIndex = -1
        for i in range(len(this.fonts)):
            avg = this.GetAvgBrightness(this.fonts[i])
            if avg < lowest:
                lowest = avg
                lowestIndex = i
        print(lowest, lowestIndex)
        return lowestIndex, lowest

    def ObtainAllBrightness(this):
        this.averages = []
        for i in range(len(this.fonts)):
            this.averages.append((this.GetAvgBrightness(this.fonts[i]), i))
        this.averages.sort(key=lambda tup:tup[0])
        return this.averages

    def ChunkToTextValue(this, chunk):
        chunkAvg = -1
        chunkMatch = -1
        chunkAvg = this.GetAvgBrightness(chunk)
        minimum = min(this.averages, key=lambda v : abs(v[0] - chunkAvg))
        return this.fonts[minimum[1]]

    def MatchImageToAscii(this, image):
        print('matching image to ascii')
        nwidth = -1
        nheight = -1
        print(image.size)
        for i in range(image.width, 0, -1):
            if i % 16 == 0:
                nwidth = i
                break
        for i in range(image.height, 0, -1):
            if i % 16 == 0:
                nheight = i
                break
        if nwidth == -1 or nheight == -1:
            print('fail')
            return "fail"
        image = image.resize((nwidth,nheight))
        data = image.load()
        print(image.size)
        for y in range(0, image.height, 16):
            for x in range(0, image.width, 16):
                chunk = image.crop((x,y,x+16,y+16))
                text = this.ChunkToTextValue(chunk).load()
                for i in range(16):
                    for j in range(16):
                        data[x+j, y+i] = text[j,i]
        return image

    def __init__(this, filename) :
        if os.path.isdir('./letters/' + filename[:-4] + '/'):
            this.__LoadLib__(filename)
            print('Letters already stored.')
            print('Loaded {} letters.'.format(len(this.fonts)))
            print('The size of the loaded array is: {} bytes.'.format(sys.getsizeof(this.fonts)))
            this.ObtainAllBrightness()
            #this.ChunkToTextValue(this.fonts[1])
        else :
            print('Splitting.')
            this.__SplitFile__(filename)
            this.__LoadLib__(filename)
            print('Loaded {} letters.'.format(len(this.fonts)))


floader = FontLoader(filename='bw_fonts.png')
