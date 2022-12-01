#Import the necessary stuff
from PIL import Image, ImageDraw
import os
import sys
from random import SystemRandom
random = SystemRandom()

#This is incase the user does not specify an imagefile
xrange = range
if len(sys.argv) != 2:
    print("The image to be split needs to be provided")
    exit()
infile = str(sys.argv[1])
if not os.path.isfile(infile):
    print("This file does not exist. Please specify a file")
    exit()

#If the user specifies a correct Imagefile, this gets executed:
img = Image.open(infile)
f, e = os.path.splitext(infile)
out_file_A = f+"_A.png"
out_file_B = f+"_B.png"
img = img.convert('1')  # convert image to 1 bit
print("Image size: {}".format(img.size))

# Prepare two empty slider images for drawing
width = img.size[0]*2
height = img.size[1]*2
print("{} x {}".format(width, height))
out_A = Image.new('1', (width, height))
out_B = Image.new('1', (width, height))
draw_A = ImageDraw.Draw(out_A)
draw_B = ImageDraw.Draw(out_B)

# These are the possible patterns:
patterns = ((1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
            (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1))
#Here's the driver code to encrypt the pixels
for x in xrange(0, int(width/2)):
    for y in xrange(0, int(height/2)):
        pixel = img.getpixel((x, y))
        pattern = random.choice(patterns)
        draw_A.point((x*2, y*2), pattern[0])
        draw_A.point((x*2+1, y*2), pattern[1])
        draw_A.point((x*2, y*2+1), pattern[2])
        draw_A.point((x*2+1, y*2+1), pattern[3])
        if pixel == 0:
            draw_B.point((x*2, y*2), 1-pattern[0])
            draw_B.point((x*2+1, y*2), 1-pattern[1])
            draw_B.point((x*2, y*2+1), 1-pattern[2])
            draw_B.point((x*2+1, y*2+1), 1-pattern[3])
        else:
            draw_B.point((x*2, y*2), pattern[0])
            draw_B.point((x*2+1, y*2), pattern[1])
            draw_B.point((x*2, y*2+1), pattern[2])
            draw_B.point((x*2+1, y*2+1), pattern[3])

out_A.save(out_file_A, 'PNG')
out_B.save(out_file_B, 'PNG')
print("The image shares have been saved on your system")
