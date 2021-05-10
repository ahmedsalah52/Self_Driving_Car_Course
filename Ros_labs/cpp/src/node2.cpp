#include <chrono>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class Node2 : public rclcpp::Node
{
public:
    Node2():Node("string_subscriber")
    {
        string_subscriber_ = this->create_subscription<std_msgs::msg::String>("str_topic",rclcpp::SensorDataQoS(), std::bind(&Node2::timer_cb, this, std::placeholders::_1));
        
    }
private:
    void timer_cb(const std_msgs::msg::String::SharedPtr msg)const
    {
        RCLCPP_INFO(this->get_logger(),"I heard:  '%s' ",msg->data.c_str());
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr string_subscriber_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Node2>());
    rclcpp::shutdown();
    return 0;
}