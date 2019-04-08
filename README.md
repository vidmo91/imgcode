<h1>imgcode</h1>
<p>simple image etching gcode generator</p> 
<p><a target="_blank" rel="noopener noreferrer" href="www.hackaday.io/project/164855-imgcode-simple-image-etching-gcode-generator">hackaday project entry with more detailed manual</a></p>
<p>functional, but still work in progress </p> 
<p>python 3.7.2 was used for creation of this software, necessary python modules are listed in requirements.txt</p> 
<br>
<h3>correct execution command:</h3> 
<p>python imgcode.py image_path output_file_path x_offset_mm y_offset_mm output_image_horizontal_size_mm pixel_size_mm feedrate max_laser_power number_of_colours</p> 
<p>e.g. python .\imgcode.py lena.png test.nc 0 0 10 0.2 100 255 5</p> 
<p>e.g. python .\imgcode.py "C:\Documents\laser files\lena.png" "C:\laser files\out files\output_gcode.nc" 0 0 10 0.2 220 1000 5</p> 
<br>
<p>more detailed info in imgcode.py</p> 
<br>
<h3>for windows users:</h3> 
<p>I compiled imgcode to exe file. It is in dist folder. Usage is similar to python version:</p> 
<p>imgcode.exe image_path output_file_path x_offset_mm y_offset_mm output_image_horizontal_size_mm pixel_size_mm feedrate max_laser_power number_of_colours</p> 
<p>e.g. imgcode.exe "C:\Documents\laser files\lena.png" "C:\laser files\out files\output_gcode.nc" 0 0 10 0.2 100 255 5</p> 
<br>
<p>Exec was tested on Win7 x64 and Win10 x64, I don't know about others.</p>
<p>You can compile it yourself. You'll need it working as python script. After testing you have to install pyinstaller module (run "pip install PyInstaller==3.4 --force-reinstall") after that run "pyinstaller --onefile .\imgcode.py -c -i icon.ico" or compile.bat in Windows. Exec should be in dist folder.</p> 
<br>
<p>If you want to use python script on Windows, and you are new to python, there is install_requirements.bat file, which will install required modules in proper versions with minimal effort. Execute this file prior to first usage if you haven't use python before.</p> 
