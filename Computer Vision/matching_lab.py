
        
from numpy.lib.function_base import diff
import rclpy

from rclpy.node import Node 
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
from sensor_msgs.msg import Image
from cv_bridge import CvBridge 
#from std_srvs.srv import Empty
#from msgs.srv import FlagString
class my_client(Node):
    def __init__(self):
        super().__init__("control_node")
        print('hello')
        self.first_start = False
        self.img_ready = False
        self.current_img = np.zeros([240, 320, 3],dtype=np.uint8)
        self.prev_img = np.zeros([240, 320, 3],dtype=np.uint8)

        self.create_subscription(Image,"/intel_realsense_d435_depth/image_raw",self.sub_call_1,10) 
        self.create_timer(0.3,self.timer)
        self.bridge = CvBridge() 

    def sub_call_1(self,msg):
        
        self.current_img = self.bridge.imgmsg_to_cv2(msg,"rgb8")
        self.img_ready = True

    def timer(self):
        if not self.img_ready:
            return 
        if (not self.first_start):
            self.first_start = True
            
            self.prev_img = self.current_img  

            return
        img1 = self.current_img          # query image (large scene)
        img2 = self.prev_img   # train image (small object)

        ## Create SIFT object
        sift = cv2.xfeatures2d.SIFT_create()

        ## Create flann matcher
        FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
        flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        #matcher = cv2.FlannBasedMatcher_create()
        matcher = cv2.FlannBasedMatcher(flann_params, {})

        ## Detect and compute
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        kpts1, descs1 = sift.detectAndCompute(gray1,None)

        ## As up
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        kpts2, descs2 = sift.detectAndCompute(gray2,None)

        ## Ratio test
        matches = matcher.knnMatch(descs1, descs2, 2)
        matchesMask = [[0,0] for i in range(len(matches))]

        diff_x = []
        diff_y = [] 
        diff_x_right = []
        diff_x_left = []
        diff_x_down= []
        diff_x_up= []
        for i, (m1,m2) in enumerate(matches):
            if m1.distance < 0.7 * m2.distance:
                matchesMask[i] = [1,0]
                ## Notice: How to get the index
                pt1 = kpts1[m1.queryIdx].pt
                pt2 = kpts2[m1.trainIdx].pt
                #print(i, pt1,pt2 )
                
                
                #filter the matches to match the points in each region in the fist img with the same reagion in the second img
                #then append all the points in a list, the points in the left in a list , the points in the right in a list 
                #and so on for the points up and down 
                if ((pt2[0] > img1.shape[1]/2) and (pt1[0] > img1.shape[1]/2)) or ((pt2[0] < img1.shape[1]/2) and (pt1[0] < img1.shape[1]/2)):
                    if ((pt2[1] > img1.shape[0]/2) and (pt1[1] > img1.shape[0]/2)) or ((pt2[1] < img1.shape[0]/2) and (pt1[1] < img1.shape[0]/2)):
                        diff_x.append(pt2[0] - pt1[0])
                        diff_y.append(pt2[1] - pt1[1])

                        if pt2[0]>img1.shape[1]/2:
                            diff_x_right.append(pt2[0] - pt1[0])
                        else:
                            diff_x_left.append(pt2[0] - pt1[0])
                        
                        if pt2[1]>img1.shape[0]/2:
                            diff_x_down.append(pt2[1] - pt1[1])
                        else:
                            diff_x_up.append(pt2[1] - pt1[1])
                        

                        if i % 5 ==0:
                            ## Draw pairs in purple, to make sure the result is ok
                            cv2.circle(img1, (int(pt1[0]),int(pt1[1])), 5, (255,0,255), -1)
                            cv2.circle(img2, (int(pt2[0]),int(pt2[1])), 5, (255,0,255), -1)

        #diff_x = [kpts1[m1.queryIdx].pt for matches in matches] 
        #diff_y = [kpts2[m1.trainIdx].pt for matches in matches]
        

        ## Draw match in blue, error in red
        draw_params = dict(matchColor = (255, 0,0),
                        singlePointColor = (0,0,255),
                        matchesMask = matchesMask,
                        flags = 0)

        res = cv2.drawMatchesKnn(img1,kpts1,img2,kpts2,matches,None,**draw_params)

        if (len(diff_x_up) == 0)or(len(diff_x_down) == 0)or(len(diff_x_left) == 0)or(len(diff_x_right) == 0) or (len(diff_x) == 0) or (len(diff_y) == 0):
            return
        avg_x_right = sum(diff_x_right)/len(diff_x_right)
        avg_x_left = sum(diff_x_left)/len(diff_x_left)

        avg_x = sum(diff_x)/len(diff_x)
        avg_y = sum(diff_y)/len(diff_y)

        avg_x_up = sum(diff_x_up)/len(diff_x_up)
        avg_x_down = sum(diff_x_down)/len(diff_x_down)


        

        if avg_x < 0:

            start_point = (int(res.shape[1]*(3/4)), int(res.shape[0]/2)) 
            
            # End coordinate
            end_point = (int((res.shape[1]*(1/4))+avg_x), int((res.shape[0]/2)+avg_y))
        else:
            start_point = (int(res.shape[1]*(1/4)), int(res.shape[0]/2)) 
            
            # End coordinate
            end_point = (int((res.shape[1]*(3/4))+avg_x), int((res.shape[0]/2)+avg_y))
        # Green color in BGR 
        color = (0, 255, 0) 
        
        # Line thickness of 9 px 
        thickness = 9
        diff_all = (avg_x ** 2)+(avg_y ** 2)
        diff_all = diff_all ** (1/2)
        #print(diff_all)
        if abs(diff_all) > 10 :
            res = cv2.arrowedLine(res, start_point, end_point,color, thickness) 
        
        
        #print(avg_x_right)
        thres = 10

        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # org
        org = (50, 50)
        
        # fontScale
        fontScale = 1
        
        # Blue color in BGR
        color = (0, 255, 0)
        
        # Line thickness of 2 px
        thickness = 2
        
           
        if (avg_x_right > 0) and (avg_x_left < 0)and (avg_x_up < 0) and (avg_x_down > 0): 
            text = 'backward'

        else:
            text ='forward'

        
        thres = 2
        changes_x = abs(avg_x_right + avg_x_left)
        if ( changes_x > 1.5):
            res = cv2.putText(res, text, org, font, 
                            fontScale, color, thickness, cv2.LINE_AA)
        print(changes_x)
        self.prev_img = self.current_img  

        cv2.imshow("Result", res)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
                
        #print(diff_x)
        #print(diff_y)




         

def main(args = None):
    rclpy.init(args=None)
    node = my_client()
    rclpy.spin(node)

    cv2.destroyAllWindows()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
