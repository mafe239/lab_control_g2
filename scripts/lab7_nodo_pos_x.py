#!/usr/bin/python
import rospy
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry

class NodePosition():
    def __init__(self):
        #Esta funcion nos permite inicializar los diferentes elementos del nodo.
        #Vamos a utilizar la libreria rospy que permite interactuar con ROS usando python.
        #Para eso creamos una instancia de esta libreria en la clase Node()
        self.rospy = rospy
        #Inicializamos el nodo con el nombre que aparece en el primer argumento.
        self.rospy.init_node("node_position", anonymous = True)
        #Inicializamos los parametros del nodo
        self.initParameters()
        #Creamos los suscriptores del nodo
        self.initSubscribers()
        #Creamos los publicacdores del nodo
        self.initPublishers()
        #Vamos a la funcion principal del nodo, esta funcion se ejecutara en un loop.
        self.main()
        return

    def initParameters(self):
        #Aqui inicializaremos todas las variables del nodo
        self.kp = 1
        self.ki = 1
        self.kd = 1
        self.xe_prev = 0
        self.v_limit = 0.5
        self.topic_odom = "/odometry/filtered"
        self.topic_set = "/setpoint"
        self.topic_vel = "/cmd_vel"
        self.topic_error = "/error"
        self.change_odom = False
        self.change_set = False
        self.rate = self.rospy.Rate(30)
        return

    def callback_odom(self, msg):
        self.xr = msg.pose.pose.position.x
        self.change_odom = True
        return

    def callback_set(self, msg):
        self.xd = msg.x
        self.change_set = True
        return

    def initSubscribers(self):
        #Aqui inicializaremos los suscriptrores
        self.sub_odom = self.rospy.Subscriber(self.topic_odom, Odometry, self.callback_odom)
        self.sub_set = self.rospy.Subscriber(self.topic_set, Point, self.callback_set)
        return

    def initPublishers(self):
        #Aqui inicializaremos los publicadores
        self.pub_vel = self.rospy.Publisher(self.topic_vel, Twist, queue_size = 10)
        self.pub_error = self.rospy.Publisher(self.topic_error, Point, queue_size = 10)
        return

    def controller(self):
        self.xe = self.xd - self.xr
        if abs(self.xe) <= 0.1:
            self.v = 0
        else:
            self.dxe = self.xe_prev - self.xe
            self.ixe = self.xe_prev + self.xe
            self.v = (self.kp*self.xe) + (self.ki*self.ixe) + (self.kd*self.dxe)
            self.v = self.v_limit*np.tanh(self.v_limit*self.v)
        self.xe_prev = self.xe
        return

    def makeVelMsg(self):
        self.msg_vel = Twist()
        self.msg_vel.linear.x = self.v
        return

    def makeErrorMsg(self):
        self.msg_error = Point()
        self.msg_error.x = self.xe
        return

    def main(self):
        #Aqui desarrollaremos el codigo principal
        print("Nodo OK")
        while not self.rospy.is_shutdown():
            if self.change_odom and self.change_set:
                self.controller()
                self.makeVelMsg()
                self.makeErrorMsg()
                self.pub_vel.publish(self.msg_vel)
                self.pub_error.publish(self.msg_error)
                self.change_odom = self.change_set = False
            self.rate.sleep()

if __name__=="__main__":
    try:
        print("Iniciando Nodo")
        obj = NodePosition()
    except rospy.ROSInterruptException:
        print("Finalizando Nodo")
