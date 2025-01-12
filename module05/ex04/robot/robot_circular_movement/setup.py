from setuptools import find_packages, setup

package_name = 'robot_circular_movement'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='DancingCerberus',
    maintainer_email='edikchermenin@gmail.com',
    description='ex 5.4',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'circular_movement = robot_circular_movement.circular_movement:main',
        ],
    },
)
