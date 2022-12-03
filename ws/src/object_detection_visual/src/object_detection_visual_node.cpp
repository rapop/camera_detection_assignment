#include <object_detection_visual/object_detection_visual_node.h>

#include <string>
#include <memory>
#include <stdexcept>

#include <visualization_msgs/msg/marker.hpp>

using namespace std::chrono_literals;

namespace object_detection_visual {

object_detection_visual_node::object_detection_visual_node()
    : Node("object_detection_visual_test")
{
    _gz_node = std::make_shared<gz::transport::Node>();

    auto subscribed = _gz_node->Subscribe(_gz_boxes_3d_topic_name, &object_detection_visual_node::_on_boxes_3d_callback, this);
    
    if (!subscribed)
    {
      throw std::runtime_error("Failed to subscribe to gz topic : " + _gz_boxes_3d_topic_name);
    }

    const auto qos = rclcpp::QoS(1000);
    _marker_publisher = this->create_publisher<visualization_msgs::msg::Marker>(_marker_boxes_3d_topic_name, qos);
}

void object_detection_visual_node::_on_boxes_3d_callback(const gz::msgs::AnnotatedOriented3DBox_V& msg)
{
    const size_t nb_of_boxes = msg.annotated_box_size();

    for (size_t i = 0; i < nb_of_boxes; i++)
    {
        const gz::msgs::AnnotatedOriented3DBox annotated_box = msg.annotated_box(i);
        // std::cout << annotatedBox.DebugString() << std::endl;
   
        geometry_msgs::msg::Pose pose;
        pose.position.x = annotated_box.box().center().z() + 10.5;
        pose.position.y = -annotated_box.box().center().x();
        pose.position.z = annotated_box.box().center().y() + 0.9;
        pose.orientation.x = annotated_box.box().orientation().x();
        pose.orientation.y = annotated_box.box().orientation().y();
        pose.orientation.z = annotated_box.box().orientation().z();
        pose.orientation.w = annotated_box.box().orientation().w();

        std_msgs::msg::ColorRGBA colour;
        colour.a = 0.5; //transparency
        colour.r = 0;
        colour.g = 1;
        colour.b = 0;

        const std::string base_frame = "base_link";

        visualization_msgs::msg::Marker marker;

        marker.header.frame_id = base_frame;
        marker.header.stamp = this->now();
        marker.action = visualization_msgs::msg::Marker::ADD;
        marker.type = visualization_msgs::msg::Marker::CUBE;
        marker.pose = pose;
        marker.id = annotated_box.label();
        marker.scale.x = annotated_box.box().boxsize().x();
        marker.scale.y = annotated_box.box().boxsize().y();
        marker.scale.z = annotated_box.box().boxsize().z();
        marker.color = colour;
        marker.lifetime.sec = 1.0;

        RCLCPP_INFO(this->get_logger(), "Attempting to publish marker... ");
        RCLCPP_INFO(this->get_logger(), annotated_box.DebugString().c_str());
        _marker_publisher->publish(marker);
    }
}

} //namespace object_detection_visual

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<object_detection_visual::object_detection_visual_node>());
    rclcpp::shutdown();
    return 0;
}
