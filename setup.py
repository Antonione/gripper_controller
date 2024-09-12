from setuptools import setup

package_name = 'gripper_controller'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/gripper_controller.launch.py']),  # Incluindo o arquivo de lançamento
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Antonione',
    maintainer_email='antonione@gmail.com',
    description='Pacote para controle da garra do manipulador via ROS2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gripper_controller = gripper_controller.gripper_controller:main',
        ],
    },
)
