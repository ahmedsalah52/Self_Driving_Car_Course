#include<chrono>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <iostream>
#include <string>
 
class Node1 : public rclcpp :: Node
{
public:

    
    Node1():Node("string_publisher")
    {
       

        string_publisher_ = this->create_publisher<std_msgs::msg::String>("str_topic",10);
        timer_ = this->create_wall_timer(std::chrono::milliseconds(500),std::bind(&Node1::timer_cb,this));
        
    }
private:
    int counter = 0 ;
    void timer_cb()
    {
        std_msgs::msg::String string_msg = std_msgs::msg::String();
        string_msg.data = ("Ahmed is publishing : "+ std::to_string(this->counter++));
        RCLCPP_INFO(this->get_logger(),string_msg.data);
        string_publisher_ ->publish(string_msg);
    }
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr string_publisher_;
    rclcpp::TimerBase::SharedPtr timer_;

};

int main(int argc,char*argv[])
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Node1>());
    rclcpp::shutdown();

    return 0;
}