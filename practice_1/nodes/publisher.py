#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

rospy.init_node('publisher')

# parameters
frequency = rospy.get_param('~frequency', 2)
message = rospy.get_param('~message', 'Hello World!')

rate = rospy.Rate(frequency)
pub = rospy.Publisher('/message', String, queue_size=10)

while not rospy.is_shutdown():
    pub.publish(message)
    rate.sleep()