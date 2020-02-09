#change
from Fonts import FontLoader
from PIL import Image
import os

def LoadImages(directory, font):
    if not os.path.isdir(os.curdir + '/' + directory + '/') :
        print('directory does not exist')
        return
    path = './' + directory + '/'
    namegen = (file for __, __, file in os.walk('./inputs/'))
    for names in namegen:
        for file in names:
            print(file)
            image = Image.open(path+file).convert('1')
            output = font.MatchImageToAscii(image)
            output.save('./outputs/' + file[:-4] + '_out'+ file[-4:])

print('Input Folder')
imageFolderName = input()
print('Input Tile Size')
tileSize = input()
font = FontLoader(filename='bw_fonts.png', framesize=int(tileSize))
LoadImages(imageFolderName, font)
#test = Image.open(i, mode="r").convert('1')
#output = floader.MatchImageToAscii(test)
#output.save(o)
