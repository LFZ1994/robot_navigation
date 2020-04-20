#!/usr/bin/env python
# Copyright 2017 HyphaROS Workshop.
# Developer: HaoChih, LIN (hypha.ros@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rospy
import string
import math
import time
import sys

from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseActionResult
from actionlib_msgs.msg import GoalStatusArray
from geometry_msgs.msg import PoseStamped
import tf
class MultiGoals:
    def __init__(self, goalListX, goalListY, goalListZ,loopTimes, map_frame):
        self.sub = rospy.Subscriber('move_base/result', MoveBaseActionResult, self.statusCB, queue_size=10)
        self.pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)   
        # params & variables
        self.goalListX = goalListX
        self.goalListY = goalListY
        self.goalListZ = goalListZ
        self.loopTimes = loopTimes
        self.loop = 1
        self.wayPointFinished = False 
        self.goalId = 0
        self.goalMsg = PoseStamped()
        self.goalMsg.header.frame_id = map_frame
        self.goalMsg.pose.orientation.z = 0.0
        self.goalMsg.pose.orientation.w = 1.0
        # Publish the first goal
        time.sleep(1)
        self.goalMsg.header.stamp = rospy.Time.now()
        self.goalMsg.pose.position.x = self.goalListX[self.goalId]
        self.goalMsg.pose.position.y = self.goalListY[self.goalId]
        self.goalMsg.pose.orientation.x = 0.0
        self.goalMsg.pose.orientation.y = 0.0
        if abs(self.goalListZ[self.goalId]) > 1.0:
            self.goalMsg.pose.orientation.z = 0.0
            self.goalMsg.pose.orientation.w = 1.0
        else:
            w = math.sqrt(1 - (self.goalListZ[self.goalId]) ** 2)
            self.goalMsg.pose.orientation.z = self.goalListZ[self.goalId]
            self.goalMsg.pose.orientation.w = w
        self.pub.publish(self.goalMsg) 
        rospy.loginfo("Current Goal ID is: %d", self.goalId)   
        self.goalId = self.goalId + 1 

    def statusCB(self, data):
        if self.loopTimes and (self.loop > self.loopTimes):
            rospy.loginfo("Loop: %d Times Finshed", self.loopTimes)
            self.wayPointFinished = True
        if data.status.status == 3 and (not self.wayPointFinished): # reached
            self.goalMsg.header.stamp = rospy.Time.now()                
            self.goalMsg.pose.position.x = self.goalListX[self.goalId]
            self.goalMsg.pose.position.y = self.goalListY[self.goalId]
            if abs(self.goalListZ[self.goalId]) > 1.0:
                self.goalMsg.pose.orientation.z = 0.0
                self.goalMsg.pose.orientation.w = 1.0
            else:
                w = math.sqrt(1 - (self.goalListZ[self.goalId]) ** 2)
                self.goalMsg.pose.orientation.z = self.goalListZ[self.goalId]
                self.goalMsg.pose.orientation.w = w
            self.pub.publish(self.goalMsg)  
            rospy.loginfo("Current Goal ID is: %d", self.goalId)              
            if self.goalId < (len(self.goalListX)-1):
                self.goalId = self.goalId + 1
            else:
                self.goalId = 0
                self.loop += 1

            
                


if __name__ == "__main__":
    try:    
        # ROS Init    
        rospy.init_node('way_point', anonymous=True)

        # Get params
        goalListX = rospy.get_param('~goalListX', '[2.0, 2.0]')
        goalListY = rospy.get_param('~goalListY', '[2.0, 4.0]')
        goalListZ = rospy.get_param('~goalListZ', '[0.0, 0.0]')
        map_frame = rospy.get_param('~map_frame', 'map' )
        loopTimes = int(rospy.get_param('~loopTimes', '0')) 

        goalListX = goalListX.replace("[","").replace("]","")
        goalListY = goalListY.replace("[","").replace("]","")
        goalListZ = goalListZ.replace("[","").replace("]","")
        goalListX = [float(x) for x in goalListX.split(",")]
        goalListY = [float(y) for y in goalListY.split(",")]
        goalListZ = [float(z) for z in goalListZ.split(",")]
        if len(goalListX) == len(goalListY) == len(goalListZ) & len(goalListY) >=2:          
            # Constract MultiGoals Obj
            rospy.loginfo("Multi Goals Executing...")
            mg = MultiGoals(goalListX, goalListY, goalListZ, loopTimes, map_frame)          
            rospy.spin()
        else:
            rospy.errinfo("Lengths of goal lists are not the same")
    except KeyboardInterrupt:
        print("shutting down")



