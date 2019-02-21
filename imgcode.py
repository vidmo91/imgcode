# imgcode v0.1 21/02/2019
# utility for CNC lasers image etching
# developed by M. "Vidmo" Widomski  
# github.com/vidmo91
# hackaday.io/vidmo91
# 
# e.g. of correct starting commands:
# python .\imgcode.py "C:\lena.png" test.nc 0 0 10 0.5 1000 2
# python .\imgcode.py lena.png test.nc 0 0 10 0.2 255 5
# try something like: python imgcode.py image_path output_file_path x_offset_mm y_offset_mm output_image_horizontal_size_mm pixel_size_mm max_feedrate_rpm number_of_colours
# 
# requirements contains list of modules I had it working on
# 
# todo:
# offsets are not implemented yet...
# make zigzag pattern 2 way 
# check and correct variable types, round floats
# add some manual
# add some GUI maybe?
#
# 
# 
# 

# Copyright 2019 M.Widomski
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy
import matplotlib
import matplotlib.pyplot
import imageio
import PIL.Image
import sys

def fileDialog(fileName):
    try:
        f = open(fileName, 'r')
        f.close
    except:
        print(fileName+" it is")
        f = open(fileName, 'w')
        f.close
    else:
        answer = input(
            fileName+" exists, do you want to overwrite it? (y/n): ")
        if (answer == 'y')or(answer == 'Y'):
            f = open(fileName, 'w')
            print(fileName+' will be overwritten')
            f.close
        elif answer == 'n'or(answer == 'N'):
            raise NameError("Specify right path next time")
        else:
            raise NameError("wrong answer")
    return f

if len(sys.argv) != 9:
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    raise NameError("Try something like: python imgcode.py image_path output_file_path x_offset_mm y_offset_mm output_image_horizontal_size_mm pixel_size_mm max_feedrate_rpm number_of_colours")
print("so far so good, now parsing values...")

# imread and convert to 8bit grayscale
try:
    img = imageio.imread(sys.argv[1], as_gray=True, pilmode="RGB")
    print("image loaded...")
except:
    raise NameError("Something is wrong with image. Probably path")
# imag = imag.astype(numpy.uint8)

# open text file for writing:
f = fileDialog(sys.argv[2])

# parsing values
try:
    x_offset_mm = float(sys.argv[3])
    y_offset_mm = float(sys.argv[4])
    output_image_horizontal_size_mm = float(sys.argv[5])
    pixel_size_mm = float(sys.argv[6])
    max_feedrate_rpm = int(sys.argv[7])
    number_of_colours = int(sys.argv[8])
    print("parameters look OK...")
except:
    raise NameError("Some of parameters are not numbers")

print("processing...")
# reseize image
y_size_input = len(img)
x_size_input = len(img[0])

# scale calculation 
x_size_output = output_image_horizontal_size_mm/pixel_size_mm
scale = x_size_output/x_size_input
# reseize image
img = PIL.Image.fromarray(img,)
img = img.resize((int(scale*x_size_input), int(scale*y_size_input)))
img = numpy.asarray(img)

# image size calculation
y_size_output = len(img)
x_size_output = len(img[0])

# negative for laser etching 
img=numpy.subtract(img,255)

# set max value of image colour to number of colours 
number_of_colours -= 1
img = numpy.rint(numpy.multiply(img, number_of_colours/255))

#save grayscale (comment to disable)
img_out=numpy.empty((x_size_output,y_size_output))
img_out=numpy.rint(numpy.multiply(img, 255/number_of_colours))
img_out = img_out.astype(numpy.uint8)
imageio.imwrite('out_img.png',img_out)

#convert to feedrates
img = numpy.rint(numpy.multiply(img, max_feedrate_rpm/number_of_colours))

# plot image (uncomment to display before processing)
# matplotlib.pyplot.imshow(img, cmap='gray')
# matplotlib.pyplot.show()

# flip up-down for simlicity 
img=numpy.flip(img,0)

#Gcode processing
prev_power = int(0)

f.write("M5 S0\n\r")
for y in range(y_size_output):

    # if y%2:
    #     for x in reversed(range(x_size_output)):
    # else:
    prev_power=int(0)
    
    for x in range(x_size_output):
        if (x == 0  and img[y][x] != 0): 
            f.write("G0 X"+str(round(x*pixel_size_mm,4))+" Y" + str(round(y*pixel_size_mm,4))+"\n\r")                                                                                                              
            f.write("M3 S"+str(int(img[y][x]))+"; pp: "+str(prev_power)+" x: "+str(x)+" y: "+str(y)+" img[y][x]: "+str(img[y][x])+" pp: "+str(prev_power)+" ;1. linia\n\r")                                                                     # turn on laser set power to img[y][x]
            prev_power = int(img[y][x])
        elif x==(x_size_output-1):
            f.write("M5 S0 ; koniec linii\n\r")
            prev_power=0
        elif (prev_power != img[y][x]):
            if (prev_power==0): 
                f.write("G0 X"+str(round((x-1)*pixel_size_mm,4))+" Y" + str(round(y*pixel_size_mm,4))+"\n\r")      
                f.write("M3 S"+str(int(img[y][x]))+"; pp: "+str(prev_power)+" x: "+str(x)+" y: "+str(y)+" img[y][x]: "+str(img[y][x])+" pp: "+str(prev_power)+" ;2. inny power prev = 0 \n\r")                                                                     # turn on laser set power to img[y][x]
                prev_power = int(img[y][x])
            if(prev_power != 0):
                f.write("G1 X"+str(round((x-1)*pixel_size_mm,4))+" Y" + str(round(y*pixel_size_mm,4))+"\n\r")      
                f.write("M3 S"+str(int(img[y][x]))+"; pp: "+str(prev_power)+" x: "+str(x)+" y: "+str(y)+" img[y][x]: "+str(img[y][x])+" pp: "+str(prev_power)+" ;3. inny power prev > 0 \n\r")                                                                     # turn on laser set power to img[y][x]
                prev_power = int(img[y][x])
        
input("everything done, press ENTER to exit, goodbye!")