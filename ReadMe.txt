Checking website again and again for vaccine slot is difficult. I made a script it notify you when slot is available.

S/W Requirement
1. install python from https://www.python.org/downloads/
2. set path of python and pip in windows Environment variable
   On my system python.exe is at path C:\Users\mradul\AppData\Local\Programs\Python\Python39-32 
   and pip.exe is at path C:\Users\mradul\AppData\Local\Programs\Python\Python39-32\Scripts
3. After set PATH in window environment. Open command prompt and run below cmd to install "requests" and "win10toast". Both are require to run python script
   	'pip install "requests" 
	'pip install win10toast'

Run - change directoty to the path of script and run below command.
      python vaccineSlot.py -p <your pin code> -a <This is age group value. 18/45/all choose one> -t <time interval in minute. script will check slot automatically after this time interval>
