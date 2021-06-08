#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "carkyo_msgs/msg/camera_emergency.hpp"
#include <pcl_conversions/pcl_conversions.h>
// Ransac includes
#include "filter_pcl/processPointClouds.h"
#include "processPointClouds.cpp"
#include<sstream>  

 
using namespace std;


class PointcloudFilter : public rclcpp::Node
{
  public:
    
   
    
    // a b c d e f
    // c, d up & down
    // e f forward (e = 0 is camera f = x as x is max required distance)

    PointcloudFilter()
    : Node("pcl_filter_node")
    {
      
         
            
     subscriber_ = this->create_subscription<sensor_msgs::msg::PointCloud2>("intel/cropped", 5, std::bind(&PointcloudFilter::subscribe_message, this, std::placeholders::_1));
     publisher_ = this->create_publisher<carkyo_msgs::msg::CameraEmergency>("emergency", 10);
    }

  private:
    float min_dist = 10000.0;
    bool flag = false;
    void subscribe_message(const sensor_msgs::msg::PointCloud2::SharedPtr message) const
    {
    
	RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "sub");
        std::string frame_id = (message->header.frame_id).c_str ();
        //RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "param:  %s  frame: %s", pcl_boundaries.c_str (), frame_id.c_str ());
        // Conversion to PCL
	      pcl::PCLPointCloud2 pcl_pc2;
	      pcl_conversions::toPCL(*message,pcl_pc2);
	      pcl::PointCloud<pcl::PointXYZ>::Ptr inputCloudI(new pcl::PointCloud<pcl::PointXYZ>);
	      pcl::fromPCLPointCloud2(pcl_pc2,*inputCloudI);
      	
      	
      	//std_msgs::msg::String string_msg = std_msgs::msg::String();
      	carkyo_msgs::msg::CameraEmergency Emergency_msg ;
        Emergency_msg = carkyo_msgs::msg::CameraEmergency();
        
        pcl::PointCloud<pcl::PointXYZ>::Ptr inputCloudII (new pcl::PointCloud<pcl::PointXYZ>);
        
        Emergency_msg.min_distance = 100;
        Emergency_msg.close_obstacle_detected = false;
        for (size_t i = 0; i < inputCloudI->points.size(); i++){
            float x = inputCloudI->points[i].x;
            float y = inputCloudI->points[i].y;
            float z = inputCloudI->points[i].z;
		
            // x is right and left , + is left
            // z is forward and back , + is forward (all data should be + , close obst should be 0:1m)
            // y is down and up , +ve is down, ground obst should be > 0.1
            //if (z < 1 &&  y < 0.1)    // Another way to filter without using processpointclouf file   
              Emergency_msg.close_obstacle_detected = true;
              if(z< (Emergency_msg.min_distance))
              {
              Emergency_msg.min_distance = z;
              }
              inputCloudII->push_back (pcl::PointXYZ (x, y, z));
        }



	
    publisher_->publish(Emergency_msg);
    }
    

    rclcpp::Node::SharedPtr nh_;
    

rclcpp::Publisher<carkyo_msgs::msg::CameraEmergency>::SharedPtr publisher_;

        
    rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscriber_;
};

int main(int argc, char * argv[])
{
  RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready");
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PointcloudFilter>());
  rclcpp::shutdown();
  return 0;
}
