#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, threading, time, rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from codegen.python.state import State
from codegen.python.temporaltransition import TemporalTransition
from codegen.python.conditionaltransition import ConditionalTransition
from codegen.python.runtimegui import RunTimeGui
from PyQt5.QtWidgets import QApplication


class RosNode():
	def __init__(self):
		rospy.init_node("obstacleAvoidancePython", anonymous=True)

		self.turtlebotROS_mobile_base_commands_velocityPub = rospy.Publisher("/turtlebotROS/mobile_base/commands/velocity", Twist, queue_size=10)
		self.turtlebotROS_laser_scanSub = rospy.Subscriber("/turtlebotROS/laser/scan", LaserScan, self.turtlebotROS_laser_scanCallback)
		self.turtlebotROS_laser_scan = LaserScan()
		self.obstacle_threshold = 0.4
		self.is_obstacle = False
		

		time.sleep(1) # wait for initialization of the node, subscriber, and publisher

	def stop(self):
		rospy.signal_shutdown("exit ROS node")

	def publishturtlebotROS_mobile_base_commands_velocity(self, turtlebotROS_mobile_base_commands_velocity):
		self.turtlebotROS_mobile_base_commands_velocityPub.publish(turtlebotROS_mobile_base_commands_velocity)



	def turtlebotROS_laser_scanCallback(self, turtlebotROS_laser_scan):
		self.turtlebotROS_laser_scan = turtlebotROS_laser_scan


	def calculate_obstacle(self):
		laserData = self.turtlebotROS_laser_scan
		for val in laserData.ranges:
			if val < self.obstacle_threshold:
				self.is_obstacle = True
				return
		self.is_obstacle = False


class State0(State):
	def __init__(self, id, initial, rosNode, cycleDuration, parent=None, gui=None):
		State.__init__(self, id, initial, cycleDuration, parent, gui)
		self.rosNode = rosNode

	def runCode(self):
		pass


class State1(State):
	def __init__(self, id, initial, rosNode, cycleDuration, parent=None, gui=None):
		State.__init__(self, id, initial, cycleDuration, parent, gui)
		self.rosNode = rosNode

	def runCode(self):
		velCommand = Twist()
		velCommand.linear.x = 0.3
		velCommand.angular.z = 0.0
		self.rosNode.publishturtlebotROS_mobile_base_commands_velocity(velCommand)


class State2(State):
	def __init__(self, id, initial, rosNode, cycleDuration, parent=None, gui=None):
		State.__init__(self, id, initial, cycleDuration, parent, gui)
		self.rosNode = rosNode

	def runCode(self):
		velCommand = Twist()
		velCommand.linear.x = 0.0
		velCommand.angular.z = 0.1
		self.rosNode.publishturtlebotROS_mobile_base_commands_velocity(velCommand)


class Tran1(ConditionalTransition):
	def __init__(self, id, destinationId, rosNode):
		ConditionalTransition.__init__(self, id, destinationId)
		self.rosNode = rosNode

	def checkCondition(self):
		self.rosNode.calculate_obstacle();
		return self.rosNode.is_obstacle;

	def runCode(self):
		pass

class Tran2(ConditionalTransition):
	def __init__(self, id, destinationId, rosNode):
		ConditionalTransition.__init__(self, id, destinationId)
		self.rosNode = rosNode

	def checkCondition(self):
		self.rosNode.calculate_obstacle()
		return not self.rosNode.is_obstacle

	def runCode(self):
		pass

displayGui = False
guiThread = None
gui = None

def readArgs():
	global displayGui
	for arg in sys.argv:
		splitedArg = arg.split('=')
		if splitedArg[0] == '--displaygui':
			if splitedArg[1] == 'True' or splitedArg[1] == 'true':
				displayGui = True
				print('runtime gui enabled')
			else:
				displayGui = False
				print('runtime gui disabled')

def runGui():
	global gui
	app = QApplication(sys.argv)
	gui = RunTimeGui()
	gui.show()
	app.exec_()

if __name__ == "__main__":
	rosNode = RosNode()

	readArgs()
	if displayGui:
		guiThread = threading.Thread(target=runGui)
		guiThread.start()


	if displayGui:
		while(gui is None):
			time.sleep(0.1)

		gui.addState(0, "root", True, 0.0, 0.0, None)
		gui.addState(1, "move", True, 845.0, 970.0, 0)
		gui.addState(2, "avoid", False, 1023.0, 981.0, 0)

		gui.addTransition(1, "obstacle", 1, 2, 931.0, 884.0)
		gui.addTransition(2, "no obstacle", 2, 1, 927.0, 1056.0)

	if displayGui:
		gui.emitLoadFromRoot()
		gui.emitActiveStateById(0)

	state0 = State0(0, True, rosNode, 100, None, gui)
	state1 = State1(1, True, rosNode, 100, state0, gui)
	state2 = State2(2, False, rosNode, 100, state0, gui)

	tran1 = Tran1(1, 2, rosNode)
	state1.addTransition(tran1)

	tran2 = Tran2(2, 1, rosNode)
	state2.addTransition(tran2)

	try:
		state0.startThread()
		state0.join()
		rosNode.stop()
		sys.exit(0)
	except:
		state0.stop()
		if displayGui:
			gui.close()
			guiThread.join()

		state0.join()
		rosNode.stop()
		sys.exit(1)
