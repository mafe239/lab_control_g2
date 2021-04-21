#!/usr/bin/python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class Node():
    def __init__(self):
        #Esta funcion nos permite inicializar los diferentes elementos del nodo.
        #Vamos a utilizar la libreria rospy que permite interactuar con ROS usando python.
        #Para eso creamos una instancia de esta libreria en la clase Node()
        self.rospy = rospy
        #Inicializamos el nodo con el nombre que aparece en el primer argumento.
        self.rospy.init_node("nodo_control", anonymous = True)
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
        self.topic_ang = "/angular_grupo2"
        self.topic_lin = "/linear_grupo2"
        self.topic_vel = "/cmd_vel"
        self.topic_emergency = "/emergency"
        self.msg_ang = String()
        self.msg_lin = String()
        self.msg_emergency = String()
        self.msg_vel = Twist()
        self.change_ang = False
        self.change_lin = False
        self.change_emergency = False
        self.rate = self.rospy.Rate(10)
        return

    def callback_ang(self, msg):
        #El argumento msg tomara el valor del mensaje recibido
        self.msg_ang = msg.data
        self.change_ang = True
        return

    def callback_lin(self, msg):
        #El argumento msg tomara el valor del mensaje recibido
        self.msg_lin = msg.data
        self.change_lin = True
        return

    def callback_emergency(self, msg):
        #El argumento msg tomara el valor del mensaje recibido
        self.msg_emergency = msg.data
        self.change_emergency = True
        return

    def initSubscribers(self):
        #Aqui inicializaremos los suscriptrores
        self.sub_ang = self.rospy.Subscriber(self.topic_ang, String, self.callback_ang)
        self.sub_lin = self.rospy.Subscriber(self.topic_lin, String, self.callback_lin)
        self.sub_emergency = self.rospy.Subscriber(self.topic_emergency, String, self.callback_emergency)
        return

    def initPublishers(self):
        #Aqui inicializaremos los publicadores
        self.pub_vel = self.rospy.Publisher(self.topic_vel, Twist, queue_size = 10)
        return

    def main(self):
        #Aqui desarrollaremos el codigo principal
        print("Nodo OK")
        while not self.rospy.is_shutdown():
            if self.change_emergency and self.msg_emergency == "stop":
                self.msg_vel.linear.x = float(0)
                self.msg_vel.angular.z = float(0)
                self.pub_vel.publish(self.msg_vel)
                self.change_emergency = False
            elif self.change_ang and self.change_lin:
                self.msg_vel.linear.x = float(self.msg_lin)
                self.msg_vel.angular.z = float(self.msg_ang)
                self.pub_vel.publish(self.msg_vel)
                self.change_ang = False
                self.change_lin = False
            self.rate.sleep()

if __name__=="__main__":
    try:
        print("Iniciando Nodo")
        obj = Node()
    except rospy.ROSInterruptException:
        print("Finalizando Nodo")
