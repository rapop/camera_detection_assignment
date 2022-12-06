#include <wheeled_robot_tf_broadcaster/wheeled_robot_tf_broadcaster_node.h>

#include <string>
#include <memory>
#include <stdexcept>

#include <geometry_msgs/msg/transform_stamped.hpp>
#include <tf2_ros/transform_broadcaster.h>

using namespace std::chrono_literals;

namespace wheeled_robot_tf_broadcaster {

wheeled_robot_tf_broadcaster_node::wheeled_robot_tf_broadcaster_node()
    : Node("wheeled_robot_tf_broadcaster_test")
{
    _gz_node = std::make_shared<gz::transport::Node>();

    auto subscribed = _gz_node->Subscribe(_gz_poses_topic_name, &wheeled_robot_tf_broadcaster_node::_on_poses_callback, this);
    
    if (!subscribed)
    {
      throw std::runtime_error("Failed to subscribe to gz topic : " + _gz_poses_topic_name);
    }

    _tf_broadcaster =
      std::make_unique<tf2_ros::TransformBroadcaster>(*this);
}

void wheeled_robot_tf_broadcaster_node::_on_poses_callback(const gz::msgs::Pose_V& msg)
{
    const size_t nb_of_objects = msg.pose_size();

    for (size_t i = 0; i < nb_of_objects; i++)
    {
        const gz::msgs::Pose object_pose = msg.pose(i);
        if (object_pose.name() == "wheeled_robot")
        {
            geometry_msgs::msg::TransformStamped t;

            t.header.stamp = this->get_clock()->now();
            t.header.frame_id = "world";
            t.child_frame_id = "wheeled_robot";

            t.transform.translation.x = object_pose.position().x();
            t.transform.translation.y = object_pose.position().y();
            t.transform.translation.z = object_pose.position().z();

            t.transform.rotation.x = object_pose.orientation().x();
            t.transform.rotation.y = object_pose.orientation().y();
            t.transform.rotation.z = object_pose.orientation().z();
            t.transform.rotation.w = object_pose.orientation().w();

            _tf_broadcaster->sendTransform(t);

            RCLCPP_INFO(this->get_logger(), "Sending transform for x: " + std::to_string(object_pose.position().x()));
        }
    }
}

} //namespace wheeled_robot_tf_broadcaster

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<wheeled_robot_tf_broadcaster::wheeled_robot_tf_broadcaster_node>());
    rclcpp::shutdown();
    return 0;
}
