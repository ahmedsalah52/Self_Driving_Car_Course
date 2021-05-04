from setuptools import setup
import os 
from glob import glob
package_name = 'iti_lab3'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
                (os.path.join('share', package_name), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmed',
    maintainer_email='ahmed_salah1996@yahoo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ["node1 =iti_lab3.node1:main",  "node2 =iti_lab3.node2:main", "node3 =iti_lab3.node3:main"
        ],
    },
)
