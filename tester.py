""" Unit testing base class.
    
Author:
    Annaleah Ernst
"""

import rospy

from logger import Logger

class Tester():
    """
    A module designed as the base class for unit tests using ROS.
    
    Args:
        name (str): The name of the module under test.
        
    Attributes:
        logger (Logger): A custom logger for the tester.
        rate (rospy.Rate): Used to control the refresh rate of robot control loops.
        
    Note: When inheriting from the Tester class, its initialization sequence should be
        the first thing to run in the inherting class's __init__ function.
    """
    def __init__(self, name):
        # set module name
        self.__name__ = str(name) + "Tester"
        
        # initialize test node
        rospy.init_node(self.__name__, anonymous = False)
        
        # set up ctrl-C shutdown behavior
        rospy.on_shutdown(self.shutdown)
        
        # set global test refresh rate (100 Hz)
        self.rate = rospy.Rate(100)
    
        # set up test node logger
        self.logger = Logger(self.__name__)
        self.logger.info("hello world")

    def main(self):
        """ The main control loop.
        
        Note: This function must be overriden in the subclasses.
        """
        self.signal_shutdown("The main function in the Tester class must be overriden!")
    
    def run(self):
        """ Actually run the robot tests, etc.
        
        Note: This function should not be overridden!
        """
        # run the main control loop
        while not rospy.is_shutdown():
            self.main()
            self.rate.sleep()

    def shutdown(self):
        """ Stop all robot operations. 
        
        Note: This function may be overridden in the subclasses.
        """
        self.logger.info("goodbye world")

    def signal_shutdown(self, reason):
        """ Interrupt robot control loop.
        
        Note: This should not be overriden without good reason.
        
        Args:
            reason (str): A human readable explanation for why the test has ended.
        """
        self.logger.warn("Signalling shutdown: " + reason)
        rospy.signal_shutdown(reason)