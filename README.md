# M3 CMake Project Creator #

This scripts generates a CMake project that contains a simple sin controller to control the Meka robot.
## Run the script ##
Launch the GUI : 
```
python m3project_creator.py
```
or the console version :
```
python m3project_creator.py -h 
```
New Features:

* Template based generator (see the template folder)
* Console interface
* On the GUI : Preview the files before being generated (double-click on them on the tree)

### The generated files ###

* **mycontroller.cpp**: The source file that contains your component class (inherits from the M3Component class).
* **mycontroller.h**: The header file associated.
* **factory_proxy.cpp**: This file is used by the m3 system to instantiate your component.
* (OPTIONAL) **mycontroller.proto**: A protobuf file that can be used to communicate with your controller (using python for example). This is used in the m3 software.
* (OPTIONAL) **mycontroller.py**: The python interface to your controller
* (OPTIONAL) **controller_example.py**: An example on how to use the python interface

### The generated project ###

```
myproject
|-- src
|   `-- myproject
|       |-- mycomponent
|       |   |-- my_class.cpp
|       |   |-- my_class_factory.cpp
|       |   `-- CMakeLists.txt
|       `-- CMakeLists.txt
|-- include
|   `-- myproject
|       `-- mycomponent
|           `-- my_class.h
|-- proto
|   `-- myproject
|       `-- mycomponent
|           `-- my_class.proto
|-- python
|   `-- myproject
|       |-- mycomponent
|       |   |-- __init__.py
|       |   |-- my_clas.py
|       |   `-- my_class_example.py
|       `-- __init__.py
|-- robot_config
|   |-- mycomponent
|   |   `-- my_class_v1.yml
|   `-- m3_config.yml
`-- CMakeLists.txt
```
## Compile your project ##

```
cd /path/to/your/project
mkdir build
cd build
cmake ..
make
```

This will generate the following files:

* **libmycomponent.so**: The library that needs to be loaded in m3. Generated in lib/
* **my_class.cc**: The generated protobuf source file. Generated in build/
* **my_class.pb.h**: The generated protobuf header. Generated in build/
* **my_class.pb.py**: The generated protobuf python source. Generated in python/

## Run your project ##
Let M3 knows there's an external path to check out:
```
source /path/to/your/project/setup.bash
```
Run the server as usual:
```
m3rt_server_run
```
Your component should be at the end of the available components lists.



Based on m3project_creator.py provided by Meka Robotics, LLC.