# Astrophotography
Download and install Python from: https://www.python.org/downloads/windows/.  
Ensure Python is added to PATH during installation.  
Download and install PySiril by following the directions here: https://siril.org/tutorials/pysiril/#installation.  
Note: Download the file listed under "Download" (pysiril-X.X.XX-py3-none-any.whl). In a Powershell terminal, navigate to your Downloads folder (cd Downloads). Then, run the command listed below the file (pip install pysiril-X.X.XX-py3-none-any.whl).  

The file structure needed for the code to run correctly is as follows (also written in a comment block in the code):  

For the script for only one set of biases (...samebias):  
[work directory]  
-> biases  
-> S0i (replace i with a number for each night)  
&ensp;-> flats  
&ensp;-> lights  

For the script for different sets of biases (...diffbias):  
[work directory]  
-> S0i (replace i with a number for each night)  
&ensp;-> biases  
&ensp;-> flats  
&ensp;-> lights  
  
To run the program: download it and double-click on the .py file.

Note: This script requires a Windows operating system. Also, I do not claim responsibility if the code breaks or does not work correctly.
