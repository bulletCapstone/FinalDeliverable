# Visualizer Documentation

### Visualizer Usage
- Visualizer is used to view the bvh tree visually after each functions that modifies the tree have been executed.

### Relevant Files

- Visualizer.py (in the Visualizer Script Directory)
- btDbvt(visualizer).h (modified)
- btDbvt(visualizer).cpp (modified)

### Required Packages

- GraphViz (https://graphviz.org)
- OpenCV (https://pypi.org/project/opencv-python/)

You should be able to install these packages using the following command:
```bash
sudo apt-get install <package name>
```

### How to use the Visualizer

1. make sure that you have the btDbvt(visualizer).h and btDbvt(visualizer).cpp for visualizer in the correct directory (bullet3/src/BulletCollision/BroadphaseCollision)
2. rename the original btDbvt.h and btDbvt.cpp into something else and rename the btDbvt(visualizer).h and btDbvt(visualizer).cpp into btDbvt.h and btDbvt.cpp repectively.
3. recompile bullet again using the following command in the root directory of the project in the commandline interface.
``` bash
make
```
4. compile the simulation that you have written with the following command


- **NOTE:**
make sure that you are providing the correct directory relative to your development setup. You must provide directory that BulletCollision, LinearMath, BulletSoftBody, BulletDynamics, and src is located. Find the exact location where the src and each of the Bullet directories are located and replace the commands accordingly. src directory should be located in the root directory of the project file.


```bash
g++ -g -std=c++11 -pg SimpleCollision.cpp -L ../../src/BulletCollision -L ../../src/LinearMath -L../../src/BulletSoftBody -L ../../src/BulletDynamics -lBulletDynamics -lBulletSoftBody -lBulletCollision -lLinearMath -I ../../src -o a.out
```
4. Run the simulation to create the graph.txt


- **NOTE:**
running the simulation will create a file called graph.txt (dot format for creating graphs using graphviz)

```bash
./a.out
```

5. Use the visualizer to create all the recorded graphs in graph.txt into an image format and compile the image file into a single video

```bash
python3 visualizer.py < graph.txt
```

- **NOTE:**
visualizer will create the bvhtree directory that contains the png files of the tree after the function that modifies the tree is executed. These images are then compiled into a single video named project.avi




### Visualizer Walkthrough

#### btDbvt.h

- In line 331 of this file, you will notice that the printTree() has been defined. This method will be used to create graph.txt. In line 332 of this file, there is also a pointerToString() function that is used to convert the pointer to a string.
    ``` cpp
        static void printTree(btDbvt* pdbvt);
        static std::string pointerToString(const btDbvtNode* node);
    ```

#### btDbvt.cpp

- From the original bullet3, following code has been added along with printTree() that has been inserted in the functions that inserts and deletes.
- we write it to the graph.txt in a DOT language format (https://graphviz.org/doc/info/lang.html) 

``` cpp
void btDbvt::printTree(btDbvt* pdbvt)
    {
        const char* filename = "graph.txt";
        std::ofstream myfile;
        myfile.open(filename,std::ofstream::app); //create a file named graph.txt and open it.
        myfile << "digraph G {\n";


        std::queue<btDbvtNode*> q; //We will use a breadth first search to iterate through the tree
        if(pdbvt->m_root){ //push the root to the queue
            q.push(pdbvt->m_root);
        }
        while(!q.empty())
        {
            const btDbvtNode* const temp_node = q.front();
            q.pop();
            if (nodeIndex.find(pointerToString(temp_node))==nodeIndex.end()){ //we try to search through the nodeIndex hashmap to see if that node has already been indexed.
                nodeIndex[pointerToString(temp_node)] = nodeNum; // If it does not exist in the nodeIndex, we insert the pointer and it's identifier into the hashmap
                nodeNum += 1; //nodeNum is a global variable used to identify each node.
            }

            if (!temp_node->isleaf()) { //if the node has a child, we will need to add the children to the queue
                if (nodeIndex.find(pointerToString(temp_node->childs[0]))==nodeIndex.end()){
                    nodeIndex[pointerToString(temp_node->childs[0])] = nodeNum;
                    nodeNum += 1;
                }
                if (nodeIndex.find(pointerToString(temp_node->childs[1]))==nodeIndex.end()){
                    nodeIndex[pointerToString(temp_node->childs[1])] = nodeNum;
                    nodeNum += 1;
                }
                
                myfile << "\t";
                myfile << nodeIndex[pointerToString(temp_node)];
                myfile << " -> ";
                myfile << nodeIndex[pointerToString(temp_node->childs[0])];
                myfile << ";\n";
                
                myfile << "\t";
                myfile << nodeIndex[pointerToString(temp_node)];
                myfile << " -> ";
                myfile << nodeIndex[pointerToString(temp_node->childs[1])];
                myfile << ";\n"; //before reach the end of the loop, we want to write these nodes to the graph.txt file and connect them with the parent.
                q.push(temp_node->childs[0]);
                q.push(temp_node->childs[1]);
            }

        }
        myfile << "# step: " << stepPrint << std::endl;
        stepPrint+=1;
        myfile << "}\n";
        myfile.close();
    }

    std::string btDbvt::pointerToString(const btDbvtNode* node){ // we are using the pointer to identify each unique node. This methods converts the pointer to a string.
        std::stringstream ss;
        ss << node;
        std::string str = ss.str();
        return str;
    }
```

####  visualizer.py
- visualizer.py converts the trees from DOT language into png files and creates a video from the png files created
```py
    import graphviz #used to create png files of the graphs written in DOT language
    import sys, subprocess
    import cv2 #used to convert png files into a single video
    import numpy as np
    import glob
    # visualizer.py < textfile

    count = 0
    currentLine = ""
    for line in sys.stdin: #we split each trees since graph.txt has multiple trees that are recorded.
        if line != "}\n":
            currentLine += line
        else:
            count+=1
            currentLine += line
            src = graphviz.Source(currentLine)
            print(count)
            number = str(count)
            number = number.zfill(6)
            src.render('bvhtree/'+number,view=False,format='png') #create trees into png files using graphviz.
            currentLine = ""




    img_array = []
    files = glob.glob('./bvhtree/*.png')
    files.sort()
    shape = 1000, 1000

    # for reference on how to convert videos from images: https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
    for filename in files: # we go through each png files
        print(filename)
        img = cv2.imread(filename)
        resized = cv2.resize(img,shape)
        # height, width, layers = img.shape
        # size = (width,height)
        img_array.append(resized)
    out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 0.8, shape) #we compile those images into video using opencv
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
```



