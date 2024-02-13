[**Main Readme**](../README.md) -- [Next practice >](../practice_2/)

# Practice 1 - Introduction to ROS

In this practice, you will progressively build a basic ROS (Robot Operating System) setup involving a publisher and a subscriber node using Python. The goal is to introduce you to the fundamental concepts of ROS, such as creating nodes, publishers, subscribers, and launching nodes using launch files. 

#### Useful links
* [Writing a Simple Publisher and Subscriber (Python)](https://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29)
* [Creating ROS package](https://wiki.ros.org/ROS/Tutorials/CreatingPackage)
* [Building a ROS package](https://wiki.ros.org/ROS/Tutorials/BuildingPackages)
* [About using roslaunch and launch files](https://wiki.ros.org/ROS/Tutorials/UsingRqtconsoleRoslaunch#Using_roslaunch)

#### Expected outcome
* Understand the basics of ROS logic (publishers and subscribers)
* You can write your own simple ROS nodes
* Have an idea what is catkin workspace, ROS package and how to create them


## 1. Implement Publisher

Write a simple publisher node that publishes "Hello World!" to a topic called `/message` with a message type of [std_msgs/String](https://docs.ros.org/en/noetic/api/std_msgs/html/msg/String.html). The Publisher should publish the string with a frequency (rate) of 2Hz.

##### Instructions
1. Create an empty directory with custom name somewhere you can easily access it. We will be using it halfway through this practice and then transfer to another directory.
1. Create a new file `publisher.py` into that folder. 
2. Copy the following code into it:

```
import rospy
from std_msgs.msg import String

rospy.init_node('publisher')
rate = rospy.Rate(2)
pub = rospy.Publisher('/message', String, queue_size=10)

while not rospy.is_shutdown():
    pub.publish("Hello world!")
    rate.sleep()
```
3. Additional reading and explanations about the different parts of the code
   - `rospy.init_node('publisher')` - [Initialize ROS node](https://wiki.ros.org/rospy/Overview/Initialization%20and%20Shutdown#Initializing_your_ROS_Node)
   - `pub = rospy.Publisher('/message', String, queue_size=10)` [Create ROS publisher](https://wiki.ros.org/rospy/Overview/Publishers%20and%20Subscribers#Publishing_to_a_topic)
   - `rospy.Rate()` and `rate.sleep()` - set the frequency, and if the job is done, wait until it is time to act again
   - `while not rospy.is_shutdown():` - do this while the node is alive

##### Validation
* In 1st terminal, run the Publisher: `python publisher.py` - there should be a message:
```
Unable to register with master node [http://localhost:11311]: master may not be running yet. Will keep trying.
```
* The message is because the ROS master is not running.
* In the 2nd terminal run `roscore`
* Open also the 3rd terminal and try:
  - `rostopic list` - should show your topic `/message` in the list
  - `rostopic info /message` - should show that your node is publishing to that topic
  - `rostopic echo /message` - should display your published message (`Ctrl + C` to finish the echoing the topic)
  - `rostopic hz /message` - provides the frequency of the topic(`Ctrl + C` to exit)


## 2. Implement Subscriber

The Subscriber node should subscribe to the topic `/message`, get the string, and print it out in the console.

##### Instructions
1. Create a new file `subscriber.py` to the same directory.
2. The contents could look like this:
```
import rospy
from std_msgs.msg import String

def callback(msg):
    print(msg.data)

rospy.init_node('subscriber')
rospy.Subscriber("/message", String, callback)
rospy.spin()
```
3. More explanations:
   - Create the [Subscriber](https://wiki.ros.org/rospy/Overview/Publishers%20and%20Subscribers#Subscribing_to_a_topic)
   - `rospy.spin` - starts the thread that receives the messages and runs the callback


##### Validation
* If you closed the roscore and Publisher after the previous task, then
   - Terminal 1: `roscore`
   - Terminal 2: run the Publisher
* Terminal 3: run the Subscriber: `python subscriber.py`
   - In the same console window, it should start printing out the "Hello World!"
* Terminal 4: `rostopic hz /message`
* Terminal 5: `rostopic info /message`
   - See that the topic now has a Publisher and two subscribers. One of the subscribers is your node, and second subscriber is the ROS process that extracts the frequency (rostopic hz)


## 3. Create a workspace and a package

We needed three console windows to run the roscore and two nodes in part 2. What if our system grows bigger - it would be a nightmare to launch the nodes separately! We could run all of them with one command if we added nodes into a launch file. To do that, we first need to organize our files into the catkin workspace ([catkin](https://wiki.ros.org/catkin/conceptual_overview) is the ROS build system for workspaces and packages). Inside the Catkin workspace, we will create smaller ROS packages. In our case, all the practices will be separate packages. All packages belonging to the same catkin workspace will be built together.

For building and creating workspace and packages we will be using [catkin_tools](https://catkin-tools.readthedocs.io/en/latest/index.html)

##### Workspace creation
 
1. `mkdir -p ~/autoware_mini_practice/src` - create the folder for the workspace
   - workspace folder is `~/autoware_mini_practice`
   - all the code and packages will be under the `~/autoware_mini_practice/src/`
2. `cd ~/autoware_mini_practice` - go to the catkin workspace folder
3. And already we could build a workspace without actually having any contents there
   - `catkin build` - will initialize workspace and build the workspace and packages inside.
   - `ll` - see that additional folders like `build` and `devel` are created
4. Now we want to clone the repo into the `src` folder
   - `git clone git@github.com:<your_github_username>/autoware_mini_practice.git src` - we need to clone the repo under src folder because that is how ROS expects
5. `catkin build` - run again and see that some packages (`common`, `practice_2`, `practice_3`, ...) are built, but `practice_1` is not one of them. We will create it right in the next part.
6. `source devel/setup.bash` - source the workspace (sourcing is the way of letting the operating system know where the resources are located so it can access them)


##### About packages

Packages for other practices were built (after `catkin build`), except for `practice_1`. Some essential files are needed to define the package. These files could be created manually, but for practice_1 let us use the commands that are provided by catkin.

* Packages also follow standard folder structure, for example:
   - nodes, launch files, config files etc., are organized in their own folders
* Important files defining the package are
   - `package.xml` - meta information and lists dependencies
   - `CMakeLists.txt` - build instructions

##### Continue with ROS package creation
7. `cd ~/autoware_mini_practice/src` - go to that folder (it should already contain folder `practice_1`)
8. `catkin create pkg practice_1 --system-deps rospy std_msgs` - will create a package (namely the two essential files) and adds `rospy` and `std_msgs` as dependencies
9. Open and see the contents of `package.xml` and `CMakeLists.txt` files, edit metadata in `package.xml`
10. Optional: clean these files from unnecessary comments (all commented-out blocks)
11. Create folder `nodes` under the `~/autoware_mini_practice/src/practice_1` and move your previously created subscriber and publisher nodes there
12. Optional: `cd ~/autoware_mini_practice`
13. `catkin build` - observe the output and see if package `practice_1` is found and successfully built along with others
14. `source /devel/setup.bash` - source again your workspace since it is changed

##### Validation
* build process (`catkin build`) should be without errors
* `catkin list` - should list your packages, including `practice_1`
   - `rospack list` - should display your packages among a lot of others - displays all known packages (sourced) available to ROS
* Here it might be a good idea to commit your changes to github, so they won't be lost. Make regular meaningful commits with proper commit message.


## 4. Running the code as script or executable

If we want to run nodes using launch files, they are treated like executable files. Currently, we run them as Python scripts, and it is good to know that a very simple script could be used to interact with ROS.

How to run nodes:
1. Go to the folder where nodes are located: `cd ~/autoware_mini_practice/src/practice_1/nodes`
1. Currently, we ran the publisher.py and subscriber.py as python scripts `python publisher.py`
   - we are calling `python` and then adding the script name
2. But we can run these scripts also as any other executables `./publisher.py`, but then two things (you can experiment and try first without these) need to be done before:
   - give executable rights to a file: `chmod +x publisher.py`
   - add a "shebang" line at the start of the script: `#!/usr/bin/env python3` - this lets the operating system know how to interpret the script

##### Validation
* `roscore` - still needed
* Try `./publisher.py` and `./subscriber.py`
* Additionally, you should be able to run your nodes now from any directory using the rosrun command and referring to a package (because the package is built and sourced and ROS knows where hey are located)
   - `rosrun practice_1 publisher.py`
   - `rosrun practice_1 subscriber.py`
* Push your changes to github!


## 5. Run nodes using the launch file
1. Create a new folder `launch` into your package folder
2. Create `practice_1.launch` file in there and copy the following code there. More information about launch files and their syntax can be found here: [roslaunch / XML](https://wiki.ros.org/roslaunch/XML)

```
<launch>
    <node pkg="practice_1" name="publisher" type="publisher.py" output="screen" required="true"/>
    <node pkg="practice_1" name="subscriber" type="subscriber.py" output="screen" required="true"/>
</launch>
```

##### Validation
* Run in terminal: `roslaunch practice_1 practice_1.launch`
* "Hello world!" should be printed like after part 2.


## 5. Parameters in launch files and nodes

##### Parameters in launch file
What if we would like to publish another message instead of "Hello World!". Instead of replacing it in the code, we should turn it into the node's parameter that is acquired when the node starts. We can add reading the parameter values to nodes from the ROS parameter server, but before, something has to add the value there. It can be done with launch file [param tag](https://wiki.ros.org/roslaunch/XML/param):

```
<launch>
    <node pkg="practice_1" name="publisher" type="publisher.py" output="screen" required="true" >
         <param name="message"   value="Hello ROS!" />
    </node>

    <node pkg="practice_1" name="subscriber" type="subscriber.py" output="screen" required="true"/>
</launch>
```

##### Node parameters
Now we need to add the code line (provided below) into the node that will get the prameter value from the ROS parameter server. Read more in [Using Parameters in rospy](https://wiki.ros.org/rospy_tutorials/Tutorials/Parameters)

```
message = rospy.get_param('~message', 'Hello World!')
```

##### Instructions
1. Copy and replace the launch file code
2. Add the get_param line to the publisher code
3. Replace previously hardcoded message with new variable `message`

##### Validation
* `roslaunch practice_1 practice_1.launch`
* New message should be printed out


## 6. Reusing the node
ROS nodes can be reused - for example, we can run several instances of the publisher node with different parameters. We can do this with the help of the launch file. Let's create two publishers publishing on the same topic but with different rates and messages.

##### Instructions
1. Convert also the rate to a parameter
   - add it to the launch file
   - add it to the publisher node
2. In the launch file, duplicate the Publisher and change:
   - `name` - for example `publisher_1` and `publisher_2`. You can't have 2 nodes with the same name running.
   - change frequencies (for example, 2Hz and 10Hz) and messages to be different

##### Validation
* `roslaunch practice_1 practice_1.launch`
* See if the output in the console matches your changes
* `rosnode list` - will list all running nodes
* `rostopic list` - see all the topics
* `rostopic info /message` - see subscribers and publishers
* Make sure you have pushed your changes to git.
