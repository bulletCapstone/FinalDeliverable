...
# Setting up Bullet

### This guide is intended to help set up a development environment in your machine and compile bullet for testing.

### Required Files

- cloned bullet3 repository (https://github.com/bulletphysics/bullet3)
- DockerFile (included with this README)

### Setting up the development environment

1. use the following command to build images using DockerFile

```bash
docker build -t bullet [location of your dockerfile]
```
2. Run the container

```
docker run --privileged --rm -v $(pwd)/bullet3:/root --name capstone-bullet -it bullet
```
This command will create the dev container. Make sure that you correctly mounted the bullet directory for your container.
Replace the $(pwd)/bullet3:/root with the bullet directory in your pc.

### Building the Bullet

1. on your root directory of the project, type the following command.

```
cmake .
```

2. build the bullet (in the root directory of the project)

```
make
```

### testing the simulation.

Once the bullet is successfully compiled, we can start creating our own simulation by importing each libraries from bullet.
The sample collision simulation is provided below. Feel free to try creating new objects in space and apply force to them to test them out.


```cpp
#include <stdio.h>
#include <vector>
#include "../../src/btBulletDynamicsCommon.h"	//you may need to change this
#include "../../src/LinearMath/btQuickprof.h" //you may need to change this
#include "../../src/LinearMath/btVector3.h"//you may need to change this

#include <iostream>
#include <chrono>
#include <ctime>

/*
 Every library except for softbody seems to be required to compile any
 simulation program
*/

btDynamicsWorld* world;	//every physical object go to the world
btDispatcher* dispatcher;	//what collision algorithm to use
btCollisionConfiguration* collisionConfig;	//what collision algorithm to use
btBroadphaseInterface* broadphase;	//should Bullet examine every object, or just what close to each other
btConstraintSolver* solver;					//solve collisions, apply forces, impulses
std::vector<btRigidBody*> bodies;

btRigidBody* addSphere(float rad,float x,float y,float z,float mass)
{
	btTransform t;	//position and rotation
	t.setIdentity();
	t.setOrigin(btVector3(x,y,z));	//put it to x,y,z coordinates
	btSphereShape* sphere=new btSphereShape(rad);	//it's a sphere, so use sphereshape
	btVector3 inertia(0,0,0);	//inertia is 0,0,0 for static object, else
	if(mass!=0.0)
		sphere->calculateLocalInertia(mass,inertia);	//it can be determined by this function (for all kind of shapes)
	
	btMotionState* motion=new btDefaultMotionState(t);	//set the position (and motion)
	btRigidBody::btRigidBodyConstructionInfo info(mass,motion,sphere,inertia);	//create the constructioninfo, able to create multiple bodies with the same info
	btRigidBody* body=new btRigidBody(info);	//create the body 
	world->addRigidBody(body);	//put it into the world
	bodies.push_back(body);	//store in a vector for cleanup
	return body;
}


void init()
{
	//pretty much initialize everything logically
	collisionConfig=new btDefaultCollisionConfiguration();
	dispatcher=new btCollisionDispatcher(collisionConfig);
	broadphase=new btDbvtBroadphase();
	solver=new btSequentialImpulseConstraintSolver();
	world=new btDiscreteDynamicsWorld(dispatcher,broadphase,solver,collisionConfig);
	world->setGravity(btVector3(0,-10,0));	//gravity on Earth
	
	//similar to createSphere
	btTransform t;
	t.setIdentity();
	t.setOrigin(btVector3(0,0,0));
	btStaticPlaneShape* plane=new btStaticPlaneShape(btVector3(0,1,0),0);
	btMotionState* motion=new btDefaultMotionState(t);
	btRigidBody::btRigidBodyConstructionInfo info(0.0,motion,plane);
	btRigidBody* body=new btRigidBody(info);
	world->addRigidBody(body);
	bodies.push_back(body);
	
	addSphere(1.0,0,20,0,1.0);	//add a new sphere above the ground 
}


int main()
{

    std::chrono::time_point<std::chrono::system_clock> start, end;
    start = std::chrono::system_clock::now();
    
	int i =0;
	init();
	btRigidBody* sphere1 = addSphere(2.0,0,20,0,1.0);
	btRigidBody* sphere2 = addSphere(2.0,10,20,5,1.0);
	btRigidBody* sphere3 = addSphere(2.0,12,20,5,1.0);
	for (i = 0; i < 150; i++)
	{
		sphere1->setLinearVelocity(btVector3(20.0,0,0));
		sphere2->setLinearVelocity(btVector3(20.0,0,0));
		sphere3->setLinearVelocity(btVector3(20.0,0,0));

		//CProfileManager::Reset();
		world->stepSimulation(1.f / 60.f);
		//CProfileManager::dumpAll();
		//printf("stepSimulation time (ms): %f\n", CProfileManager::Get_Time_Since_Reset());


		//print positions of all objects
		for (int j = world->getNumCollisionObjects() - 1; j >= 0; j--)
		{
			btCollisionObject* obj = world->getCollisionObjectArray()[j];
			btRigidBody* body = btRigidBody::upcast(obj);
			btTransform trans;
			if (body && body->getMotionState())
			{
				body->getMotionState()->getWorldTransform(trans);
			}
			else
			{
				trans = obj->getWorldTransform();
			}
			//printf("world pos object %d = %f,%f,%f\n", j, float(trans.getOrigin().getX()), float(trans.getOrigin().getY()), float(trans.getOrigin().getZ()));
		}
		//CProfileManager::dumpAll();
	}
	//CProfileManager::dumpAll();

	for(int i=0;i<bodies.size();i++)
	{
		world->removeCollisionObject(bodies[i]);
		btMotionState* motionState=bodies[i]->getMotionState();
		btCollisionShape* shape=bodies[i]->getCollisionShape();
		delete bodies[i];
		delete shape;
		delete motionState;
	}
	delete dispatcher;
	delete collisionConfig;
	delete solver;
	delete broadphase;
	delete world;

    end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds = end-start;
    std::time_t end_time = std::chrono::system_clock::to_time_t(end);
  
    std::cout << "finished computation at " << std::ctime(&end_time)
              << "elapsed time: " << elapsed_seconds.count() << "s\n";
}


```

### building the simulation

You can build the simulation using the below command (make sure to change the directory accordingly!!)
```
g++ -g -std=c++11 -pg SimpleCollision.cpp -L ../../src/BulletCollision -L ../../src/LinearMath -L../../src/BulletSoftBody -L ../../src/BulletDynamics -lBulletDynamics -lBulletSoftBody -lBulletCollision -lLinearMath -I ../../src -o a.out
```

### Moving On

There is also source code for visualizer and the linked list version of bullet to aid in your projects. You can replace the source code as shown in the documentation in those files. Be sure to check the documentations there as well.
