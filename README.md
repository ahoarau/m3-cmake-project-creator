# M3 CMake Project Creator #

This scripts generates a CMake project to control the Meka robot, using the real-time components.
## Run the script ##
```
#!Bash
python m3project_creator.py
```
Then follow the instructions, and click on Apply to generate the project files.

Note : No files except the factory_proxy.cpp will be overwritten
TODO : Add overwriting options

## The generated files ##

* **mycontroller.cpp** # The source file that contains your component class (inherits from the M3Component class).
* **mycontroller.h** # The header file associated.
* **factory_proxy.cpp** # This file is used by the m3 system to instantiate your component.
* (OPTIONAL) **mycontroller.proto** # A protobuf file that can be used to communicate with your controller (using python for example). This is used in the m3 software.
* (OPTIONAL) **mycontroller.py** # The python interface to your controller
* (OPTIONAL) **controller_example.py** # An example on how to use the python interface

### The generated project ###
The structure is as follow :
>
project_name/
>>src/
>>>project_name/
>>>>mycomponents/
>>>>>mycontroller.cpp 
>>>>>factory_proxy.cpp 

>>include/
>>>project_name/
>>>>mycomponents/
>>>>>mycontroller.h

>>proto/
>>>project_name/
>>>>mycomponents/
>>>>>mycontroller.proto

>>python/
>>>project_name/
>>>>mycomponents/
>>>>>mycontroller.py
>>>>>controller_example.py
>

## Compile your project ##

```
#!Bash
cd /path/to/your/project
mkdir build
cd build
cmake ..
make
```
This will generate the following files:
* **libmycontroller.so** : The library that needs to be loaded in m3.
* **mycontroller.cc** : The generated protobuf source file.
* **mycontroller.pb.h** : The generated protobuf header.
* **mycontroller.pb.py** : The generated protobuf python source.

## Run your project ##
De



Based on m3project_creator.py provided by Meka Robotics, LLC.