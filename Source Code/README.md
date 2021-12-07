# Source Code Documentation
Jeff Van Buskirk - jef@lehigh.edu

## Original Data Structure
The original data structure used by Bullet is a bounding volume Heirarchy (bvh/bvt). This data structure is extremely quick at checking collisions. It works by grouping items spacially and then running collision detections on the groups. Internal nodes represent groups of items/other internal nodes. The leaf nodes represent the actual objects in the simulation. 

To get a more conceptual understanding of this data structure use my slides here 
    https://docs.google.com/presentation/d/1cgoFmLhCI4T64JPPgrvRuQhVf9lPTCcGWIPvql8JGn4/edit?usp=sharing 

Internal nodes represent groups of items/other internal nodes. The leaf nodes represent the actual objects in the simulation. 

The code for the original data structure is stored in 
bullet3/src/BulletCollision/BroadphaseCollision

The two files you will mainly be working with are
1. btDbvt.cpp
2. btDbvt.h

In the zip file of code I have put extensively commented versions of these two files. Most comments are related to functions/objects that you will actually be using. 

There is one other file that failed when creating the linked list
bullet3/src/BulletCollision/CollisionDispatch/btCompoundCompoundCollisionAlgorithm.cpp

This file as well as some soft body files directly acess the data structure and need to be adapted to function with your chosen structure.

## Linked List 
Linked List: https://github.com/bulletCapstone/bullet3/tree/jefBranch 

Our group was able to successfully implement a Linked List that replaces the Bvt. To do so we changed the strucutre of nodes to have one child instead of two, and then adapted all of the bvt functions to work with this node structure. These linked list files are attached in the Linked List folder as well as the btCompoundCompoundCollisionAlgorithm.cpp file that was changed to get it working correctly. These files are a lot simpler than the Bvt and I recommend building your structure from these files rather than from the bvt files. 

I also recommend building bullet in your container and replacing these files with the given bullet ones rather than simply cloning my repo. It is good to know how to build the original project and will probably be cleaner. 

The makefiles/cmakefiles are setup to work with the names the files already have. You can change these to work with names or simply rename linkedList.cpp/.h to btDbvt.cpp/.h and the makefiles will work fine with them. I ended up having two copies of the Bullet repo, one being the unchanged original to act as a control and the other to change my files in. 


## Debugging
When compiling, the makefiles will not produce executables that can be run with GDB. To change this we need to edit a few makefiles and compile the main file with a command different to make.

- Navigate to the root directory 
- run the commands 
    - `make clean`
    - `cmake clean`
    - `cmake .`
- Navigate to the following files
    1. bullet3/src/BulletCollision/CMakeFiles/BulletCollision.dir/flags.make
    2. bullet3/src/BulletDynamics/CMakeFiles/BulletDynamics.dir/flags.make
    3. bullet3/src/LinearMath/CMakeFiles/LinearMath.dir/flags.make

    On line 5 of all of these files there are the CXX flags used when compiling. When you build with cmake these flags are 01 - Debug. 

    **Change line 5 to CXX_FLAGS = -O0 -g**

- Navigate to the root directory
- run `make`

Doing this will create the libraries in a way that allows GDB to see their symbols. You only need to do this once when you first make bullet and then the makefiles will work as long as you don't run cmake clean.

To allow GDB to see the symbols of the main file we will use the hello world in bullet3/examples/HelloWorld

Run the following command: 
`g++ -g -std=c++11 -pg HelloWorld.cpp -L ../../src/BulletCollision -L ../../src/LinearMath -L ../../src/BulletDynamics -l BulletDynamics -l BulletCollision -l LinearMath -I ../../src -o a.out`

This will take the HelloWorld.cpp and create an executable named a.out

You can rename those names to whatever you like. To run your executable run `./a.out` and to debug it run `GDB ./a.out`

After setting up GDB I recommend running the program in GDB in `layout src` to follow the code in both our linked list implementation and the original bvt. This will give you a better idea of what files are connecting with the bvt and where things can be optimized.

If you have any issues getting the Linked List to work or 







Name: Jared Lee
email: jrl222@lehigh.edu

# Benchmarking


    Goal: Find the code that would determine the performance of the data and runtime.
          Once code was altered, the benchmark would be run comparatively to that of the original 
          bullet code.

    This was going to be achieved with the CProfiler.

    To find the CProfile code, it is located in 
    src/LinearMaths/btQuickProf.h

    In that section of code, there are functions all related to the Cprofiler.
    The specific function that was attempted was the CprofileManager::dumpAll() function.

    This section would have been used with a simulation to tell the preformance and runtime of the bullet code. 
    An altered version would have been tested along with the original bullet code to determine changes in speed.

# Concurrent Data
    Goal: Find concurrency within the code of bullet


    There are files within examples that contain information multithreading as well as demo within the 
    examples folder.
        - examples/MultiThreading
    I had a bit of difficulty being able to make use of those. 

    Suggestion was made through looking into OpenCL code that are online for sources on multithreading.
    There are also files on OpenCL within the examples folder:
        - examples/OpenCL
