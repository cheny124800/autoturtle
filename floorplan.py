""" Fixed map
    
Author:
    Annaleah Ernst
"""
import tf

from copy import deepcopy
from geometry_msgs.msg import Point, Pose, Quaternion

class FloorPlan():
    """ A simple graph reprentation of a floor plan.
        
    Args:
        point_ids (set): Unique identifier for each waypoint in the graph.
        locations (dict): Point_ids mapped to tuples representing locations.
        neighbors (dict): Point_ids mapped to lists containing other point_ids representing 
            the current node's neighbors.
        landmarks (dict, optional): Map AprilTag landmark ids to their absolute pose on 
            the floorplan.
            
    Attributes:
        graph (dict of Waypoints): Represent the floorplan in an easy to parse way.
        landmarks (dict of Landmarks): Represent the precise pose of landmarks associated with
            their landmark id.
    """
    def __init__(self, point_ids, locations, neighbors, landmark_ids = None, landmark_positions = None, landmark_orientations = None):
    
        # construct graph out of waypoints
        self.graph = {}
        for point_id in point_ids:
            self.graph[point_id] = Waypoint(locations[point_id], neighbors[point_id])

        # construct landmark map
        self.landmarks = {}
        if landmark_ids is not None:
            for landmark_id in landmark_ids:
                self.landmarks[landmark_id] = Landmark(landmark_positions[landmark_id], landmark_orientations[landmark_id])

    def _dist2(self, point1, point2):
        """ Return the distance squared between two points. """
        return (point1.x - point2.x)**2 + (point1.y - point2.y)**2

    def _getClosestWaypoint(self, point):
        """ Return the closest waypoint to the given position. """
        return min(self.graph, key = lambda k: self._dist2(point, self.graph[k].location))

    def getShortestPath(self, cur_pose, destination):
        """ Compute the shortest path from the current position to the destination (Djikstra's). 
        
        Args:
            cur_pose (geometry_msg.msgs.Point): The current position of the robot with respect to the map origin.
            destination (geometry_msg.msgs.Point): The position of the desired destination with resepect to the 
                map origin.
        
        Returns: 
            A list of geometry_msg.msgs.Points representing the path on the map.
        """
        # get the waypoints closest to the start and end
        start = self._getClosestWaypoint(cur_pose)
        end = self._getClosestWaypoint(destination)

        # create vertex set, distance squared list and prev path
        Q = deepcopy(self.graph)
        prev = {}
        dist2 = {}
        for point in self.graph:
            prev[point] = None
            dist2[point] = float('inf')

        # begin our merry search
        dist2[start] = 0
        while Q:

            # pop the closest waypoint off the queue
            closest_id = min(Q, key = lambda k: dist2[k])
            closest = Q.pop(closest_id)

            # if we've made it to the destination, we're done
            if closest_id == end:
                break

            # update minimum path lengths:
            for neighbor in closest.neighbors:
                test_dist2 = dist2[closest_id] + self._dist2(self.graph[neighbor].location, closest.location)
                if test_dist2 < dist2[neighbor]:
                    dist2[neighbor] = test_dist2
                    prev[neighbor] = closest_id

        # back out the actual path
        crawler = end
        path = [destination]

        while True:
            # add the current point to the path at the beginning
            path.insert(0, self.graph[crawler].location)

            # we've reached our start position
            if prev[crawler] is None:
                return path

            crawler = prev[crawler]

class Landmark():
    """ A wrapper for constructing landmark information.
    
    Args:
        position (float tuple): Specify the waypoint's offset from the origin.
        angle (float): Specify the angle of rotation of the landmark in the xy plane;
            (how much has its perpendicular vector deviated from the y axis?).
            Generally between -pi and pi.
        
    Attributes:
        pose (geometry_msgs.msg.Pose): The location and orientation of the landmark.
    """
    def __init__(self, position, angle):
        # convert angle to quaternion
        q = tf.transformations.quaternion_from_euler([0,0,angle])
        
        # construct the landmark pose
        self.pose = Pose()
        self.pose.orientation = Quaternion(q[0], q[1], q[2], q[3])
        self.pose.position = Point(position[0], position[1], 0)

class Waypoint():
    """ ALl necessary waypoint information.
            
    Args:
        location (float tuple): Specify the waypoint's offset from the origin.
        neighbors (set): Specify the waypoint's neighbors in the graph as their ids.
            
    Attributes:
        location (geometry_msgs.msg.Point): Represent the waypoint's offset from the origin.
        neighbors (set): A set of unique point ids connected to the current waypoint
    """
    def __init__(self, location, neighbors):
        self.location = Point(location[0], location[1], 0)
        self.neighbors = set(neighbors)

if __name__ == "__main__":
    from math import pi
    
    point_ids = {'A', 'B', 'C', 'D', 'E', 'F'}
    locations = {'A': (2,4), 'B': (5,5), 'C':(5,1), 'D':(9,6), 'E':(2,-2), 'F':(6,-4)}
    neighbors = {'A': ['C', 'B'], 'B': ['A', 'C', 'D'], 'C': ['A', 'B', 'E'], 'D':['B'], 'E':['C'], 'F':['C']}
    landmarks = {10, 17}
    landmark_positions = [(0,0), (1,1)]
    landmark_orientations = [0, pi/2]

    myPlan = FloorPlan(point_ids, locations, neighbors, landmarks, landmark_positions, landmark_orientations)
    print(myPlan.landmarks)
    print(myplan.graph)
    print(myPlan.getShortestPath(Point(2,4,0), Point(9,6,0)))







