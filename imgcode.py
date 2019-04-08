# imgcode v0.2.1 29/03/2019
# utility for CNC lasers image etching
# developed by M. "Vidmo" Widomski  
# github.com/vidmo91
# hackaday.io/vidmo91
# 
# correct execution command: python imgcode.py image_path output_file_path x_offset_mm y_offset_mm output_image_horizontal_size_mm pixel_size_mm feedrate max_laser_power number_of_colours
# e.g. of correct execution commands:
# python .\imgcode.py "C:\lena.png" test.nc 0 0 10 0.5 100 1000 2
# python .\imgcode.py lena.png test.nc 0 0 10 0.2 220 255 5
# 
# requirements contains list of modules I had it working on
# 
# todo:
# there probably something is wrong with last etched line logic. have to check that.
# 
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
import colorama
colorama.init()

# uncoment for berry veautiful splash screen
print(colorama.Fore.GREEN+"\t           _         __"+"\n"+"\t \\    / | | \\  |\\/| |  |"+"\n"+"\t  \\  /  | |  | |  | |  |"+"\n"+"\t   \\/   | |_/  |  | |__|\n \t\tpresents \n"+colorama.Fore.RED+"\t\timgcode"+colorama.Fore.RESET+"\n"+"\t"+colorama.Back.LIGHTCYAN_EX+colorama.Fore.RED+"mmmh... those aesthetics!!!"+colorama.Back.RESET+colorama.Fore.RESET+"\n\t"+colorama.Back.LIGHTCYAN_EX+colorama.Fore.RED+"  just berry veautiful!!!  "+colorama.Back.RESET+colorama.Fore.RESET+"\n\n")

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
            fileName+" exists, do you want to overwrite it? (Y/n): ")
        if (answer == 'y')or(answer == 'Y')or(answer == ''):
            f = open(fileName, 'w')
            print(fileName+' will be overwritten')
            f.close
        elif answer == 'n'or(answer == 'N'):
            raise NameError("Specify right path next time")
        else:
            raise NameError("wrong answer")
    return f

if len(sys.argv) != 10:

    print(colorama.Fore.RED+'Number of arguments:', len(sys.argv), 'arguments. (required 10 arguments)')
    print('Argument List:', str(sys.argv))
    print("correct execution command: ")
    print("python imgcode.py image_path output_file_path x_offset_mm y_offset_mm output_image_horizontal_size_mm pixel_size_mm feedrate max_laser_power number_of_colours")
    print("e.g. python .\\imgcode.py lena.png test.nc 0 0 10 0.2 100 255 5")
    print("e.g. python .\\imgcode.py \"C:\\Documents\\laser files\\lena.png\" \"C:\\laser files\\out files\\output_gcode.nc\" 0 0 10 0.2 100 255 5"+colorama.Fore.RESET)    
    raise NameError("wrong execution command")
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
    feedrate = int(sys.argv[7])
    max_laser_power = int(sys.argv[8])
    number_of_colours = int(sys.argv[9])
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
img=numpy.subtract(255,img)

# set max value of image colour to number of colours 
number_of_colours -= 1
img = numpy.rint(numpy.multiply(img, number_of_colours/255))

#save preview
img_out=numpy.empty((x_size_output,y_size_output))
img_out=numpy.rint(numpy.multiply(img, 255/number_of_colours))
img_out = img_out.astype(numpy.uint8)
imageio.imwrite('out_img.png',img_out)

#convert to feedrates
img = numpy.rint(numpy.multiply(img, max_laser_power/number_of_colours))

# display preview before processing - requires closing plot window before proceeding 
# img2=numpy.subtract(number_of_colours,img)
# matplotlib.pyplot.imshow(img2, cmap='gray')
# matplotlib.pyplot.show()

# flip up-down for simplicity 
img=numpy.flip(img,0)

#Gcode processing
f.write("; imgcode generated code \n")
f.write("; developed by M. \"Vidmo\" Widomski \n") 
f.write(";  github.com/vidmo91 \n")
f.write(";  hackaday.io/vidmo91 \n")
f.write(" \n")
f.write("H5 S0 \n")
f.write("F"+str(feedrate)+"\n")
f.write("G0 Z0 ; for some grbl senders compatibility \n")
f.write(" \n") #add your G-CODE file header here
# f.write("M5 S0\n")
for y in range(y_size_output):

    if 1-y%2:
        prev_power=int(0)
        for x in range(x_size_output):
            if (x == 0  and img[y][x] != 0): #first point, diffrent from 0
                f.write("G0 X"+str(round(x*pixel_size_mm+x_offset_mm,4))+" Y" + str(round(y*pixel_size_mm+y_offset_mm,4))+"\n")                                                                                                              
                f.write("M3 S"+str(int(img[y][x]))+"\n")                                                                     
                prev_power = int(img[y][x])
            elif x==(x_size_output-1):#eol
                f.write("M5 S0\n")
                prev_power=0
            elif (prev_power != img[y][x]):#different power
                if (prev_power==0): #transition from 0 to higher power
                    f.write("G0 X"+str(round((x-1)*pixel_size_mm+x_offset_mm,4))+" Y" + str(round(y*pixel_size_mm+y_offset_mm,4))+"\n")      
                    f.write("M3 S"+str(int(img[y][x]))+"\n") 
                    prev_power = int(img[y][x])
                if(prev_power != 0):# transition from some power to another
                    f.write("G1 X"+str(round((x-1)*pixel_size_mm+x_offset_mm,4))+" Y" + str(round(y*pixel_size_mm+y_offset_mm,4))+"\n")      
                    f.write("M3 S"+str(int(img[y][x]))+"\n")  
                    prev_power = int(img[y][x])
        
    else:
        prev_power=int(0)
        for x in reversed(range(x_size_output)):
            if (x == x_size_output-1  and img[y][x] != 0): #first point, diffrent from 0
                f.write("G0 X"+str(round(x*pixel_size_mm+x_offset_mm,4))+" Y" + str(round(y*pixel_size_mm+y_offset_mm,4))+"\n")                                                                                                              
                f.write("M3 S"+str(int(img[y][x]))+"\n")                                                                     
                prev_power = int(img[y][x])
            elif x==0:#eol
                f.write("M5 S0\n")
                prev_power=0
            elif (prev_power != img[y][x]):#different power
                if (prev_power==0): #transition from 0 to higher power
                    f.write("G0 X"+str(round((x-1)*pixel_size_mm+x_offset_mm,4))+" Y" + str(round(y*pixel_size_mm+y_offset_mm,4))+"\n")      
                    f.write("M3 S"+str(int(img[y][x]))+"\n")                                                                     
                    prev_power = int(img[y][x])
                if(prev_power != 0):# transition from some power to another
                    f.write("G1 X"+str(round((x-1)*pixel_size_mm+x_offset_mm,4))+" Y" + str(round(y*pixel_size_mm+y_offset_mm,4))+"\n")      
                    f.write("M3 S"+str(int(img[y][x]))+"\n")                                                                     
                    prev_power = int(img[y][x])
f.close()
            
#input("everything done, press ENTER to exit, goodbye!")
print(colorama.Fore.GREEN+"\neverything done, buh bye!\n")
input("press ENTER to exit")