#include<chrono>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/int64.hpp"
#include <iostream>
#include <string>
class Node2 : public rclcpp :: Node
{
public:
    Node2():Node("string_subscriber")
    {
        string_subscriber_ = this->create_subscription<std_msgs::msg::String>("str_topic",10, std::bind(&Node2::timer_cb,this,std::placeholders::_1));
        int_publisher_ = this->create_publisher<std_msgs::msg::Int64>("int_topic",10);
    }
private:
    void timer_cb(const std_msgs :: msg::String ::SharedPtr msg)const
    {
        std::string rec_msg;
        int the_int = 0;
        char temp;
        int counter = 1;
        RCLCPP_INFO(this->get_logger(),msg->data.c_str());
        rec_msg = msg->data.c_str();

        std_msgs::msg::Int64 int_msg = std_msgs::msg::Int64();
        for(int i= rec_msg.size()-1; i>0; i-- )
        {   
            temp = rec_msg[i];
            if (temp == ' ') break;
            the_int += (int)(temp-'0') * counter;
            counter*=10;
        }

        int_msg.data = the_int;
        int_publisher_ ->publish(int_msg);

    }
    rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr int_publisher_;

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr string_subscriber_;
    

};

int main(int argc,char*argv[])
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Node2>());
    rclcpp::shutdown();

    return 0;
}