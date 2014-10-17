M3 CMake Project Creator
==============================

This scripts generates a CMake project that contains a simple sin controller to control the Meka robot.

## Download
```bash
sudo -E pip install m3project-creator
```
## Upgrades

```bash
sudo -E pip install m3project-creator --upgrade
```

## Run the script
Launch the GUI : 
```bash
m3create_pkg
```
or the console version :
```bash
m3create_pkg -h 
```
Example : 
```bash
m3create_pkg m3awesome_project sincontrollers myawesomecontroller 
```
New Features:

* Template based generator (see the template folder)
* Console interface
* On the GUI : Preview the files before being generated (double-click on them on the tree)

### The generated files

* **mycontroller.cpp**: The source file that contains your component class (inherits from the M3Component class).
* **mycontroller.h**: The header file associated.
* **factory_proxy.cpp**: This file is used by the m3 system to instantiate your component.
* (OPTIONAL) **mycontroller.proto**: A protobuf file that can be used to communicate with your controller (using python for example). This is used in the m3 software.
* (OPTIONAL) **mycontroller.py**: The python interface to your controller
* (OPTIONAL) **controller_example.py**: An example on how to use the python interface

### The generated project

```bash
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
|       |   |-- my_class.py
|       |   `-- my_class_example.py
|       `-- __init__.py
|-- robot_config
|   |-- mycomponent
|   |   `-- my_class_v1.yml
|   `-- m3_config.yml
`-- CMakeLists.txt
```
## Compile your project
If you don't have the M3_CMAKE_MODULES var set (latest version of m3 software):
```
echo $M3_CMAKE_MODULES 
```
Then,you might want to get some useful FindXXX.cmake (for M3 system, Yamlccp, protobuf etc):
```
cd /path/to/your/project
git clone https://github.com/ahoarau/meka-cmake-modules.git
```
Then you can compile your project safely:

```bash
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
* **setup.bash**: A file that contains information about your package
* 
## Run your project ##
Let M3 knows there's an external path to check out (you should do that in all terminals you open):
```bash
source /path/to/your/project/setup.bash
```
Run the server as usual:
```bash
m3rt_server_run
```
Your component should be at the top of the available components lists (default name is controller_example_v1).

Vizualize the robot in rviz : 
```bash
roslaunch meka_description m3ens_viz.launch
```
Add a robot model and change 'fixed frame' to 'T0'.
Now **enable** your component and see the robot moves:
```bash
# source your setup.bash first !
cd /path/to/your/project/python/componentdir/mycontroller/
python mycontroller_example.py
```

Good luck !

Based on m3project_creator.py provided by Meka Robotics, LLC.
