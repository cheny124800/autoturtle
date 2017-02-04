""" Local navigation using robot_pose_ekf
    
Author:
    Annaleah Ernst
"""
import rospy
import tf

from geometry_msgs.msg import PoseWithCovarianceStamped, Point, Quaternion

from logger import Logger

class Navigation():
    """ Local navigation.
    
    Attributes:
        p (geometry_msgs.msg.Point): The position of the robot in the odometry frame according to
            the robot_pose_ekf package.
        q (geometry_msgs.msg.Quaternion): The orientation of the robot in the odometry frame
            according the the robot_pose_ekf package.
    """
    def __init__(self):
        self._logger = Logger("Navigation")

        self.p = None
        self.q = None
        rospy.Subscriber('/robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, self._ekfCallback)

    def _ekfCallback(self, data):
        self.p = data.pose.pose.position
        self.q = data.pose.pose.orientation
        self._logger.debug(tf.transformations.tf.transformations.euler_from_quaternion([self.q.x, self.q.y, self.q.z, self.q.w]))

if __name__ == "__main__":
    from tester import Tester

    class NavigationTest(Tester):
        def __init__(self):
            self.navigation = Navigation()
            Tester.__init__(self, "Navigation")

        def main(self):
            pass

    NavigationTest()