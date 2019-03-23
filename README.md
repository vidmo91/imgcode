<h1>imgcode</h1>

<p>tool for creating GCODE for laser etching images<p/> 
<p>functional, but still work in progress (offsets do not work yet)<p/> 
<p>python 3.7.2 was used for creation of this software, necessary python modules are listed in requirements.txt<p/> 
<hr>
<p>correct execution command:<p/> 
<p>python imgcode.py image_path output_file_path x_offset_mm y_offset_mm output_image_horizontal_size_mm pixel_size_mm max_feedrate_rpm number_of_colours<p/> 
<p>e.g. python .\imgcode.py lena.png test.nc 0 0 10 0.2 255 5<p/> 
<p>e.g. python .\imgcode.py "C:\Documents\laser files\lena.png" "C:\laser files\out files\output_gcode.nc" 0 0 10 0.2 255 5<p/> 
<p>more detailed info in imgcode.py<p/> 
<br>
<p>for windows users:<p/> 
<p><p/>  
<br>
<p>I compiled imgcode to exe file. It is in dist folder. Usage is similar to python version:<p/> 
<p>imgcode.exe image_path output_file_path x_offset_mm y_offset_mm output_image_horizontal_size_mm pixel_size_mm max_feedrate_rpm number_of_colours<p/> 
<p>e.g. imgcode.exe "C:\Documents\laser files\lena.png" "C:\laser files\out files\output_gcode.nc" 0 0 10 0.2 255 5<p/> 
<p><p/> 
<br>
<p>It was my first python exe file so I have no idea If it will work on any other machine. Mine is Win10 x64 1809 with Intel i7-7700HQ CPU <p/> 
<br>
<p>If you want to use python script, there is install_requirements.bat file which will install required modules in proper versions with minimal effort. Execute this file prior to first usage if you haven't use python before. Old python users will know what to do.<p/> 
