from setuptools import find_packages, setup

package_name = 'full_name'

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
    maintainer='cerberus',
    maintainer_email='edikchermenin@gmail.com',
    description='Python client-server example',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'service = full_name.service_member_function:main',
            'client = full_name.client_member_function:main',
        ],
    },
)
