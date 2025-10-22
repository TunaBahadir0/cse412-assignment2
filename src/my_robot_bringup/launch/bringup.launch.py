import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    # Diğer paketlerimizin yollarını bul
    pkg_my_robot_description = get_package_share_directory('my_robot_description')
    pkg_my_ball_chaser = get_package_share_directory('my_ball_chaser')

    # 1. Gazebo'yu Başlat (gazebo.launch.py dosyamızı çağırıyoruz)
    # Bu dosya Gazebo'yu, robot_state_publisher'ı ve robotu spawn etmeyi zaten yapıyor
    start_gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_my_robot_description, 'launch', 'gazebo.launch.py')
        )
    )

    # 2. Ball Chaser Düğümünü Başlat
    start_ball_chaser_node = Node(
        package='my_ball_chaser',
        executable='ball_chaser_node',
        output='screen'
    )

    # 3. RViz'i Başlat (Ödevde isteniyor [cite: 57])
    # Not: Grafik sürücüsü sorunumuz nedeniyle model görünmeyebilir,
    # ancak launch dosyasının bunu başlatması gerekiyor.
    start_rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    # 4. 'ros2 run tf2_tools view_frames' komutunu çalıştır (Ödevde isteniyor [cite: 58])
    # Bu, TF ağacının bir PDF'ini oluşturur
    run_view_frames_command = ExecuteProcess(
        cmd=['ros2', 'run', 'tf2_tools', 'view_frames', '--ros-args', '-r', '__ns:=/tf_frames'],
        output='screen'
    )

    return LaunchDescription([
        start_gazebo_launch,
        start_ball_chaser_node,
        start_rviz_node,
        run_view_frames_command
    ])
