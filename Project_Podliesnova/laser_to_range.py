#!/usr/bin/env python
import rospy
import numpy
from sensor_msgs.msg import Range
from sensor_msgs.msg import LaserScan

pub_centre = rospy.Publisher('distance_to_obstacle/centre', Range, queue_size=1)
pub_right = rospy.Publisher('distance_to_obstacle/right', Range, queue_size=1)
pub_left = rospy.Publisher('distance_to_obstacle/left', Range, queue_size=1)

def callback(data):
    #print("Im in callback")
    ranges = data.ranges
    min_angle = data.angle_min
    max_angle = data.angle_max
    min_range = data.range_min
    max_range = data.range_max
    angle_per_dp = abs(max_angle - min_angle)/len(ranges)
    centre_min_list = []
    left_min_list = []
    right_min_list = []
    for rg in ranges:
        #print(rg)
        r_centre = Range()
        r_right = Range()
        r_left = Range()
        if int((abs(max_angle - min_angle)/2+0.2094395)/angle_per_dp)>ranges.index(rg)>int((abs(max_angle - min_angle)/2-0.2094395)/angle_per_dp):
            centre_min_list.append(rg)
        elif int((abs(max_angle - min_angle)/2+0.2094395+0.436332)/angle_per_dp)>ranges.index(rg)>int((abs(max_angle - min_angle)/2+0.2094395)/angle_per_dp):
            left_min_list.append(rg)
        elif int((abs(max_angle - min_angle)/2-0.2094395)/angle_per_dp)>ranges.index(rg)>int((abs(max_angle - min_angle)/2-0.2094395-0.436332)/angle_per_dp):
            right_min_list.append(rg)
    r_centre.header.stamp = rospy.Time.now()
    r_centre.header.frame_id = "centre"
    r_centre.radiation_type = 0
    r_centre.field_of_view = 0.436332
    r_centre.min_range = min_range
    r_centre.max_range = max_range
    r_centre.range = numpy.nanmin(centre_min_list)
    pub_centre.publish(r_centre)
    r_left.header.stamp = rospy.Time.now()
    r_left.header.frame_id = "left"
    r_left.radiation_type = 0
    r_left.field_of_view = 0.436332
    r_left.min_range = min_range
    r_left.max_range = max_range
    r_left.range = numpy.nanmin(left_min_list)
    pub_left.publish(r_left)
    r_right.header.stamp = rospy.Time.now()
    r_right.header.frame_id = "right"
    r_right.radiation_type = 0
    r_right.field_of_view = 0.436332
    r_right.min_range = min_range
    r_right.max_range = max_range
    r_right.range = numpy.nanmin(right_min_list)
    pub_right.publish(r_right)

def listener():
    rospy.init_node('laser_to_range', anonymous=True)
    type_of_laser = rospy.get_param('lidar_or_depthcam')
    rospy.Subscriber(type_of_laser, LaserScan, callback)
    #rospy.get_param('lidar_or_depthcam')
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException: pass
