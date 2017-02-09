""" Safe motion.
    
Author:
    Annaleah Ernst
"""
from logger import Logger
from motion import Motion
from sensors import Sensors

class SafeMotion(Motion):
    """ Handle basic Turtlebot motion while being aware of safety issues.
    
    Attributes:
        turn_dir (int): 1 if turning left, -1 if turning right, None if no turn.
        turning (bool): True if the robot is turning, False otherwise.
        walking (bool): True if robot is moving linearly, False otherwise.
    """
    def __init__(self):
        Motion.__init__(self)
        self.sensors = Sensors()
        self.avoiding = True
        self._logger = Logger("SafeMotion")
    
    def _avoid(self, func, *args, **kwargs):
        """ Both be safe and premptive. """
        # if we see a cliff or get picked up, stop
        if self.sensors.cliff or self.sensors.wheeldrop:
            Motion.stop(self, now=True)
    
        # if we hit something, stop
        elif self.sensors.bump:
            if self.walking:
                Motion.stop_linear(self, now=True)
            else:
                self.avoiding = True
                Motion.turn(self, self.sensors.bumper > 0)
        
        # this means that we're avoiding nothing!
        elif self.avoiding:
            if self.walking or self.turning:
                Motion.stop(self)
            else:
                self.avoiding = False
        
        # otherwise, we keep going
        else:
            func(self, *args, **kwargs)

    def _safetyStop(self, func, *args, **kwargs):
        """ The generic safety wrapper for the Turtlebot. """
        # if we see a cliff or get picked up, stop
        if self.sensors.cliff or self.sensors.wheeldrop:
            Motion.stop(self, now=True)

        # if we hit something, stop
        elif self.sensors.bump:
            Motion.stop_linear(self, now=True)
        
        # otherwise, we keep going
        else:
            func(self, *args, **kwargs)

    def linear_stop(self, now=False):
        """ Stop robot's linear motion, immediately if necessary. """
        self._safetyStop(Motion.linear_stop, now)

    def rotational_stop(self, now=False):
        """ Stop the robot rotation, immediately if necessary. """
        self._safetyStop(Motion.rotational_stop, now)
    
    def stop(self, now=False):
        """ Stop the robot, immediately if necessary.
        
        Args:
            now (bool): Robot stops immediately if true, else decelerates.
        """
        self._safetyStop(Motion.stop, now)
    
    def turn(self, speed=1):
        """ Turn the Turtlebot in the desired direction.
            
        Args:
            direction (bool): Turn direction is left if True, right if False
            speed (float, optional): The percentage of the the maximum turn speed
                the robot will turn at.
        """
        self._avoid(Motion.turn, speed)

    def walk(self, speed=1):
        """ Move straight forward.
        
        Args:
            speed (float, optiona): The percentage of the the maximum linear speed
                the robot will move at.
        """
        self._avoid(Motion.walk, speed)

    def shutdown(self, rate):
        """ Bring the robot to a gentle stop. 
        
        Args:
            rate (rospy.Rate): The refresh rate of the enclosing module.
        """
        self._safetyStop(Motion.shutdown, rate)

if __name__ == "__main__":
    from tester import Tester
    from sensors import Sensors

    class SafeMotionTest(Tester):
        """ Run unit test for the motion class. """
        
        def __init__(self):
            # set up basic sensing
            self.motion = SafeMotion()
            
            Tester.__init__(self, "SafeMotion")

        def main(self):
            # running walk here should behave like wander in the motion module test
            self.motion.walk()

        def shutdown(self):
            self.motion.shutdown(self.rate)

    SafeMotionTest()