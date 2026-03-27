#!/usr/bin/env python3

from nav_msgs.msg import OccupancyGrid, MapMetaData
from geometry_msgs.msg import Pose, Point
from std_msgs.msg import Header, ColorRGBA
from visualization_msgs.msg import Marker
from rclpy.node import Node
from rclpy import init as rclpy_init, spin, shutdown
import rclpy
import numpy as np


class SimpleMapPublisher(Node):
    def __init__(self):
        super().__init__("simple_map_publisher")

        self.map_pub = self.create_publisher(OccupancyGrid, "/map", 10)

        # 1. Параметры карты
        self.resolution = 0.1  # 10 см на клетку
        self.width = 80        # 8 м / 0.1 = 80
        self.height = 80
        self.origin_x = -4.0   # карта [-4, 4] × [-4, 4]
        self.origin_y = -4.0

        # 2. Создаём пустую карту: 0 = свободно, 100 = стены по краю
        grid = np.zeros((self.height, self.width), dtype=np.int8)

        # стены по краям (100 = занято)
        wall = 100
        grid[0:2, :] = wall   # нижняя стена
        grid[-2:, :] = wall   # верхняя стена
        grid[:, 0:2] = wall   # левая
        grid[:, -2:] = wall   # правая

        self.map_data = grid.flatten().tolist()

        # 3. Таймер: публикуем карту при старте
        self.create_timer(1.0, self.publish_map_once)
        self.published = False

    def publish_map_once(self):
        if self.published:
            return

        map_msg = OccupancyGrid()
        map_msg.header = Header()
        map_msg.header.stamp = self.get_clock().now().to_msg()
        map_msg.header.frame_id = "map"

        map_msg.info = MapMetaData()
        map_msg.info.resolution = self.resolution
        map_msg.info.width = self.width
        map_msg.info.height = self.height

        map_msg.info.origin = Pose()
        map_msg.info.origin.position.x = self.origin_x
        map_msg.info.origin.position.y = self.origin_y
        map_msg.info.origin.position.z = 0.0

        map_msg.data = self.map_data

        self.map_pub.publish(map_msg)
        self.get_logger().info("Published simple map on /map")

        self.published = True


def main(args=None):
    rclpy_init(args=args)
    node = SimpleMapPublisher()
    spin(node)
    node.destroy_node()
    shutdown()


if __name__ == "__main__":
    main()