#pragma once

#include <memory>
#include <string>

#include <rclcpp/rclcpp.hpp>
#include <visualization_msgs/msg/marker.hpp>
#include <gz/transport.hh>
#include <gz/msgs/annotated_oriented_3d_box_v.pb.h>

namespace object_detection_visual {
class object_detection_visual_node : public rclcpp::Node
{
  public:
    object_detection_visual_node();

  private:
    void _on_boxes_3d_callback(const gz::msgs::AnnotatedOriented3DBox_V& msg);
    rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr _marker_publisher;
    std::shared_ptr<gz::transport::Node> _gz_node;
    const std::string _gz_boxes_3d_topic_name = "/boxes_3d";
    const std::string _marker_boxes_3d_topic_name = "/marker";
};

} //namespace object_detection_visual