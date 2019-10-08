#!/usr/bin/env python 
import rosbag
import numpy as np
from sensor_msgs.msg import CompressedImage
import cv2



image_msg= CompressedImage()
bagout = rosbag.Bag('/home/bagout.bag', 'w')
bag = rosbag.Bag('/home/amod19-rh3-ex-record-Linus_Lingg.bag')
for topic, msg, t in bag.read_messages(topics=['/linuslingg/camera_node/image/compressed']):
     time = str(msg.header.stamp.secs) + "." + str(msg.header.stamp.nsecs) + " sec"
     image = msg.data
     image_np = cv2.imdecode(np.fromstring(msg.data, np.uint8), cv2.IMREAD_COLOR)

     cv2.putText(image_np, time, (0,40),  cv2.FONT_HERSHEY_SIMPLEX, 1,[255,0,0],1)
     #cv2.imwrite('/home/image.jpeg',image_np)
     image_str= np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
     
     image_msg.data = image_str
     image_msg.format = '.jpg'
     image_msg.header.stamp = msg.header.stamp

     bagout.write('/linuslingg/camera_node/image/compressed',image_msg, t)    
           
bag.close()
bagout.close()

#run commands to play bag:
#docker run -it -e ROS_MASTER_URI=http://192.168.1.79:11311/ -e ROS_IP=192.168.1.82 -v /home/linuslingg/bags2:/home --rm --net host duckietown/dt-ros-commons:daffy-amd64 /bin/bash
#other terminal
#dts start_gui_tools linuslingg --base_image duckietown/dt-core:daffy-amd64
