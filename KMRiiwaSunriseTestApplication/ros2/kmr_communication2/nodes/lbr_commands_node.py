import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped
from rclpy.qos import qos_profile_sensor_data
from rclpy.utilities import remove_ros_args
import argparse
from scripts.tcpSocket import TCPSocket
from rclpy.action import ActionServer, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor



def cl_red(msge): return '\033[31m' + msge + '\033[0m'



class LbrCommandsNode(Node):
    def __init__(self,connection_type,robot):
        super().__init__('lbr_commands_node')
        self.name = 'lbr_commands_node'
        self.declare_parameter('port')
        #port = int(self.get_parameter('port').value)
        if robot == 'KMR':
            self.declare_parameter('KMR/ip')
            ip = str(self.get_parameter('KMR/ip').value)
        else:
            ip=None

        if connection_type == 'TCP':
            self.soc = TCPSocket(ip,port,self.name)
        else:
            self.soc=None


        self.callback_group = ReentrantCallbackGroup()
        

        # Make a listener for relevant topics
        sub_manipulator_vel = self.create_subscription(String, 'manipulator_vel', self.manipulatorVel_callback, 10)
        sub_shutdown = self.create_subscription(String, 'shutdown', self.shutdown_callback, 10)
        #sub_statusdata=self.create_subscription(LbrStatusdata, 'lbr_statusdata', self.status_callback, 10,callback_group=self.callback_group)
        #self.path_server = ActionServer(self,MoveManipulator,'move_manipulator', self.move_manipulator_callback,callback_group=self.callback_group)

        self.point_publisher = self.create_publisher(Float64, 'vinkel', 20)

        self.done_moving=False
        self.last_path_variable = False

        #while not self.soc.isconnected:
        #    pass
        self.get_logger().info('Node is ready')

    def status_callback(self,data):
        if (self.last_path_variable==False and data.path_finished == True):
            self.done_moving = True
            print("done_moving set to true")
        self.last_path_variable = data.path_finished

    def shutdown_callback(self, data):
        print(data)
        msg = "shutdown"
        self.soc.send(msg)
        self.soc.isconnected = False

    def manipulatorVel_callback(self, data):
        #self.soc.send(msg)
        msg = 'setLBRmotion ' + data.data
        print("Sending {}".format())


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--connection')
    parser.add_argument('-ro', '--robot')
    args = parser.parse_args(remove_ros_args(args=argv))

    rclpy.init(args=argv)
    lbr_commands_node = LbrCommandsNode(args.connection,args.robot)

    executor = MultiThreadedExecutor()
    rclpy.spin(lbr_commands_node)

    try:
        lbr_commands_node.destroy_node()
        rclpy.shutdown()
    except:
        print(cl_red('Error: ') + "rclpy shutdown failed")


if __name__ == '__main__':
    main()
